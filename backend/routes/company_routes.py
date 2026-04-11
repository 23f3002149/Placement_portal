from flask import Blueprint, jsonify, request, current_app, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.security import generate_password_hash
from database import db
from model import User, Company, Drive, DriveBranch, Application, Student
from cache_utils import cache_get, cache_set, cache_delete
from backend_jobs.notifications import notify_student_status, notify_interview_schedule

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/register", methods=["POST"])
def register_company():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        name=name,
        password=hashed_password,
        role="company"
    )

    db.session.add(new_user)
    db.session.flush()

    new_company = Company(
        user_id=new_user.user_id,
        company_name=company_name
    )

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"success_msg": "Company registered successfully"})


@company_bp.route("/info", methods=["GET"])
@jwt_required()
def get_company_info():
    user_id = int(get_jwt_identity())
    cache_key = f"company_info_{user_id}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(cached)

    company = Company.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    result = {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "company_name": company.company_name,
        "industry": company.industry,
        "description": company.description,
        "website": company.website
    }

    cache_set(cache_key, result, ttl=600)
    return jsonify(result)


@company_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_company_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    company = Company.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    if "name" in data:
        user.name = data.get("name", user.name)
    if "email" in data:
        user.email = data.get("email", user.email)
    if "company_name" in data:
        company.company_name = data.get("company_name", company.company_name)
    if "industry" in data:
        company.industry = data.get("industry", company.industry)
    if "description" in data:
        company.description = data.get("description", company.description)
    if "website" in data:
        company.website = data.get("website", company.website)

    db.session.commit()
    cache_delete(f"company_info_{user_id}")

    return jsonify({"msg": "Company profile updated successfully"})


@company_bp.route("/drives", methods=["POST"])
@jwt_required()
def create_drive():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user.role != "company":
        return jsonify({"msg": "Only company allowed"}), 403

    data = request.get_json()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    if company.company_approved_status != "approved":
        return jsonify({"msg": "Company not approved yet"}), 403

    job_title = data.get("job_title")
    job_description = data.get("job_description")
    package = data.get("package")
    location = data.get("location")
    cgpa_criteria = data.get("cgpa_criteria")
    application_deadline = data.get("application_deadline")
    branches = data.get("branches", [])

    try:
        deadline = datetime.strptime(application_deadline, "%Y-%m-%d")
    except:
        return jsonify({"msg": "Invalid date format"}), 400

    new_drive = Drive(
        company_id=company.company_id,
        job_title=job_title,
        job_description=job_description,
        package=package,
        location=location,
        cgpa_criteria=cgpa_criteria,
        application_deadline=deadline,
        drive_approved_status="pending"
    )

    db.session.add(new_drive)
    db.session.flush()

    for branch in branches:
        db.session.add(DriveBranch(
            drive_id=new_drive.drive_id,
            branch=branch
        ))

    db.session.commit()
    return jsonify({"msg": "Drive created successfully"})


@company_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_company_applications():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "company":
        return jsonify({"msg": "Only company can view applications"}), 403

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    drives = Drive.query.filter_by(company_id=company.company_id).all()
    result = []
    for drive in drives:
        applications = Application.query.filter_by(drive_id=drive.drive_id).all()
        for app in applications:
            student = Student.query.get(app.student_id)
            student_user = User.query.get(student.user_id)
            result.append({
                "application_id": app.application_id,
                "drive_id": drive.drive_id,
                "job_title": drive.job_title,
                "student_name": student_user.name,
                "student_email": student_user.email,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "applied_date": app.applied_date.strftime("%Y-%m-%d") if app.applied_date else None,
                "status": app.status,
                "resume_url": f"http://127.0.0.1:5000/resume/{student.resume}" if student.resume else None
            })

    return jsonify(result)


@company_bp.route("/application/<int:app_id>/reject", methods=["PUT"])
@jwt_required()
def reject_applied(app_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "company":
        return jsonify({"msg": "Only company allowed"}), 403

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    application.status = "rejected"
    db.session.commit()

    student = Student.query.get(application.student_id)
    student_user = User.query.get(student.user_id)
    drive = Drive.query.get(application.drive_id)
    notify_student_status(current_app.config, student_user, drive, "rejected")

    return jsonify({"msg": "Application rejected"})


@company_bp.route("/application/<int:app_id>/shortlist", methods=["PUT"])
@jwt_required()
def shortlist_application(app_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "company":
        return jsonify({"msg": "Only company allowed"}), 403

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    application.status = "shortlisted"
    db.session.commit()

    student = Student.query.get(application.student_id)
    student_user = User.query.get(student.user_id)
    drive = Drive.query.get(application.drive_id)
    notify_student_status(current_app.config, student_user, drive, "shortlisted")

    return jsonify({"msg": "Student shortlisted"})


@company_bp.route("/application/<int:app_id>/final", methods=["PUT"])
@jwt_required()
def final_decision(app_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "company":
        return jsonify({"msg": "Only company allowed"}), 403

    data = request.get_json()
    decision = data.get("status")
    if decision not in ["selected", "rejected"]:
        return jsonify({"msg": "Invalid decision"}), 400

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    if application.status != "shortlisted":
        return jsonify({"msg": "Only shortlisted students can be finalized"}), 400

    application.status = decision
    db.session.commit()

    student = Student.query.get(application.student_id)
    student_user = User.query.get(student.user_id)
    drive = Drive.query.get(application.drive_id)
    notify_student_status(current_app.config, student_user, drive, decision)

    return jsonify({"msg": f"Student {decision}"})


@company_bp.route("/application/<int:app_id>/interview", methods=["POST"])
@jwt_required()
def schedule_interview(app_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "company":
        return jsonify({"msg": "Only company allowed"}), 403

    data = request.get_json()
    interview_time_str = data.get("interview_time")

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    if application.status != "shortlisted":
        return jsonify({"msg": "Only shortlisted students can be scheduled"}), 400

    try:
        interview_dt = datetime.fromisoformat(interview_time_str)
    except Exception:
        return jsonify({"msg": "Invalid datetime format. Use ISO format."}), 400

    student = Student.query.get(application.student_id)
    student_user = User.query.get(student.user_id)
    drive = Drive.query.get(application.drive_id)
    notify_interview_schedule(current_app.config, student_user, drive, interview_dt)

    return jsonify({"msg": "Interview scheduled and emails queued"})


@company_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_company_dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "company":
        return jsonify({"msg": "Only company can access this"}), 403

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    all_drives = Drive.query.filter_by(company_id=company.company_id).all()
    total_applications = 0
    selected_candidates = 0
    pending_review = 0
    active_drives_count = 0
    drives_data = []

    for drive in all_drives:
        drive_apps = Application.query.filter_by(drive_id=drive.drive_id).all()
        app_count = len(drive_apps)
        selected = len([a for a in drive_apps if a.status == "selected"])
        pending = len([a for a in drive_apps if a.status == "applied"])

        total_applications += app_count
        selected_candidates += selected
        pending_review += pending

        if drive.drive_approved_status == "approved":
            active_drives_count += 1

        drives_data.append({
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "status": drive.drive_approved_status,
            "application_count": app_count,
            "application_deadline": drive.application_deadline.strftime("%Y-%m-%d") if drive.application_deadline else None,
            "location": drive.location,
            "package": drive.package
        })

    drives_data.reverse()

    return jsonify({
        "stats": {
            "active_drives": active_drives_count,
            "total_applications": total_applications,
            "selected_candidates": selected_candidates,
            "pending_review": pending_review
        },
        "drives": drives_data
    })


@company_bp.route("/report/monthly", methods=["GET"])
@jwt_required()
def company_monthly_report():
    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    drives = Drive.query.filter_by(company_id=company.company_id).all()
    drive_ids = [d.drive_id for d in drives]
    applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all()

    csv_data = "Application ID,Student Name,Roll No,Branch,CGPA,Drive Title,Status,Applied Date\n"
    for app in applications:
        student = Student.query.get(app.student_id)
        drive = Drive.query.get(app.drive_id)
        csv_data += f"{app.application_id},{student.user.name if student else 'N/A'},{student.roll_no if student else 'N/A'},{student.branch if student else 'N/A'},{student.cgpa if student else 'N/A'},{drive.job_title if drive else 'N/A'},{app.status},{app.applied_date}\n"

    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=company_monthly_report.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
