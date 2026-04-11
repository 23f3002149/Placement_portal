import os
from flask import Blueprint, jsonify, request, current_app, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.security import generate_password_hash
from database import db
from model import User, Student, Drive, DriveBranch, Application, Company
from cache_utils import cache_get, cache_set, cache_delete
from backend_jobs.notifications import notify_admin_application, notify_student_application

student_bp = Blueprint("student", __name__)


@student_bp.route("/students/register", methods=["POST"])
def register_student():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    roll_no = data.get("roll_no")
    branch = data.get("branch")

    hashed_password = generate_password_hash(password)

    existing_student = User.query.filter_by(email=email).first()

    if existing_student:
        return jsonify({"message": "Student with this email already exists"}), 400

    try:
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="student"
        )

        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.user_id,
            roll_no=roll_no,
            branch=branch
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({"message": "Student registered successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400


@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    })


@student_bp.route("/student/info", methods=["GET"])
@jwt_required()
def get_student_info():
    user_id = int(get_jwt_identity())
    cache_key = f"student_info_{user_id}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(cached)

    student = Student.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    result = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "roll_no": student.roll_no,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "year_of_passing": student.year_of_passing,
        "skills": student.skills,
        "resume_url": f"http://127.0.0.1:5000/resume/{student.resume}" if student.resume else None
    }
    cache_set(cache_key, result, ttl=600)

    return jsonify(result)


@student_bp.route("/student/profile", methods=["PUT"])
@jwt_required()
def update_student_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    student = Student.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    if "name" in data:
        user.name = data.get("name", user.name)
    if "email" in data:
        user.email = data.get("email", user.email)
    if "branch" in data:
        student.branch = data.get("branch", student.branch)
    if "roll_no" in data:
        student.roll_no = data.get("roll_no", student.roll_no)
    if "cgpa" in data:
        student.cgpa = data.get("cgpa", student.cgpa)
    if "year_of_passing" in data:
        student.year_of_passing = data.get("year_of_passing", student.year_of_passing)
    if "skills" in data:
        student.skills = data.get("skills", student.skills)

    db.session.commit()
    cache_delete(f"student_info_{user_id}")

    return jsonify({"msg": "Profile updated successfully"})


@student_bp.route("/student/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_to_drive(drive_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "student":
        return jsonify({"msg": "Only students can apply"}), 403

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"msg": "Drive not found"}), 404

    if drive.drive_approved_status != "approved":
        return jsonify({"msg": "Drive not approved yet"}), 403

    if datetime.utcnow() > drive.application_deadline:
        return jsonify({"msg": "Application deadline passed"}), 400

    existing_application = Application.query.filter_by(
        student_id=student.student_id,
        drive_id=drive_id
    ).first()

    if existing_application:
        return jsonify({"msg": "Already applied"}), 400

    allowed_branches = DriveBranch.query.filter_by(drive_id=drive_id).all()
    allowed_branch_list = [b.branch for b in allowed_branches]

    if student.branch not in allowed_branch_list:
        return jsonify({"msg": "Not eligible for this drive"}), 403

    new_application = Application(
        student_id=student.student_id,
        drive_id=drive_id
    )
    db.session.add(new_application)
    db.session.commit()

    notify_admin_application(current_app.config, student, drive)
    notify_student_application(current_app.config, student.user, drive)

    return jsonify({"msg": "Applied successfully"})


@student_bp.route("/student/drives", methods=["GET"])
@jwt_required()
def get_student_drives():
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    drives = Drive.query.filter_by(drive_approved_status="approved").all()
    result = []
    for drive in drives:
        if drive.application_deadline and datetime.utcnow() > drive.application_deadline:
            continue

        allowed_branches = DriveBranch.query.filter_by(drive_id=drive.drive_id).all()
        branch_list = [b.branch for b in allowed_branches]

        if student.branch not in branch_list:
            continue

        if drive.cgpa_criteria and student.cgpa and student.cgpa < drive.cgpa_criteria:
            continue

        existing = Application.query.filter_by(
            student_id=student.student_id,
            drive_id=drive.drive_id
        ).first()

        company = Company.query.get(drive.company_id)

        result.append({
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "package": drive.package,
            "location": drive.location,
            "cgpa_criteria": drive.cgpa_criteria,
            "application_deadline": drive.application_deadline.strftime("%Y-%m-%d") if drive.application_deadline else None,
            "drive_approved_status": drive.drive_approved_status,
            "company_name": company.company_name if company else "Unknown",
            "branches": branch_list,
            "already_applied": existing is not None
        })

    return jsonify({
        "drives": result,
        "student": {
            "name": user.name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "year_of_passing": student.year_of_passing
        }
    })


@student_bp.route("/student/applications", methods=["GET"])
@jwt_required()
def get_student_applications():
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    applications = Application.query.filter_by(student_id=student.student_id).all()
    result = []
    for app in applications:
        drive = Drive.query.get(app.drive_id)
        company = Company.query.get(drive.company_id) if drive else None
        result.append({
            "application_id": app.application_id,
            "status": app.status,
            "applied_date": app.applied_date.strftime("%Y-%m-%d") if app.applied_date else None,
            "job_title": drive.job_title if drive else "N/A",
            "package": drive.package if drive else None,
            "location": drive.location if drive else None,
            "company_name": company.company_name if company else "Unknown"
        })

    return jsonify(result)


@student_bp.route("/student/dashboard", methods=["GET"])
@jwt_required()
def get_student_dashboard():
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    all_apps = Application.query.filter_by(student_id=student.student_id).all()
    stats = {
        "total": len(all_apps),
        "applied": len([a for a in all_apps if a.status == "applied"]),
        "shortlisted": len([a for a in all_apps if a.status == "shortlisted"]),
        "selected": len([a for a in all_apps if a.status == "selected"]),
        "cgpa": student.cgpa
    }

    recent_apps_raw = (
        Application.query
        .filter_by(student_id=student.student_id)
        .order_by(Application.application_id.desc())
        .limit(3).all()
    )
    recent_apps = []
    for app in recent_apps_raw:
        drive = Drive.query.get(app.drive_id)
        company = Company.query.get(drive.company_id) if drive else None
        recent_apps.append({
            "application_id": app.application_id,
            "job_title": drive.job_title if drive else "N/A",
            "company_name": company.company_name if company else "Unknown",
            "applied_date": app.applied_date.strftime("%Y-%m-%d") if app.applied_date else None,
            "status": app.status
        })

    approved_drives = Drive.query.filter_by(drive_approved_status="approved").all()
    upcoming = []
    for drive in approved_drives:
        if drive.application_deadline and datetime.utcnow() > drive.application_deadline:
            continue
        branches = DriveBranch.query.filter_by(drive_id=drive.drive_id).all()
        branch_list = [b.branch for b in branches]
        if student.branch not in branch_list:
            continue
        if drive.cgpa_criteria and student.cgpa and student.cgpa < drive.cgpa_criteria:
            continue
        already = Application.query.filter_by(
            student_id=student.student_id, drive_id=drive.drive_id
        ).first()
        if already:
            continue
        company = Company.query.get(drive.company_id)
        upcoming.append({
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "company_name": company.company_name if company else "Unknown",
            "application_deadline": drive.application_deadline.strftime("%Y-%m-%d") if drive.application_deadline else None
        })
        if len(upcoming) >= 3:
            break

    return jsonify({
        "stats": stats,
        "recent_applications": recent_apps,
        "upcoming_drives": upcoming
    })


@student_bp.route("/student/resume", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    if 'resume' not in request.files:
        return jsonify({"msg": "Koi file nahi mili"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"msg": "File select nahi ki"}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"msg": "Sirf PDF allowed hai"}), 400

    filename = f"student_{student.student_id}_resume.pdf"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    student.resume = filename
    db.session.commit()
    cache_delete(f"student_info_{user_id}", "admin_students")

    return jsonify({
        "msg": "Resume upload successful!",
        "resume_url": f"http://127.0.0.1:5000/resume/{filename}"
    })


@student_bp.route("/student/report", methods=["GET"])
@jwt_required()
def student_report():
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    applications = Application.query.filter_by(student_id=student.student_id).all()
    csv_data = "Application ID,Drive Title,Company,Status,Applied Date\n"
    for app in applications:
        drive = Drive.query.get(app.drive_id)
        company_name = drive.company.company_name if drive and drive.company else "N/A"
        csv_data += f"{app.application_id},{drive.job_title if drive else 'N/A'},{company_name},{app.status},{app.applied_date}\n"

    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=student_applications.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
