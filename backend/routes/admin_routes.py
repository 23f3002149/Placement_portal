from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from database import db
from model import Company, Drive, Application, User, Student, DriveBranch
from cache_utils import cache_get, cache_set, cache_delete

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("", methods=["POST"])
def create_admin():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        name=name,
        password=hashed_password,
        role="admin"
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Admin created successfully"})


@admin_bp.route("/company/<int:company_id>/status", methods=["PUT"])
@jwt_required()
def update_company_status(company_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    status = data.get("status")
    if status not in ["approved", "rejected", "blacklisted"]:
        return jsonify({"msg": "Invalid status. Allowed: approved, rejected, blacklisted"}), 400

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    company.company_approved_status = status
    db.session.commit()
    cache_delete("admin_companies")

    return jsonify({"msg": f"Company {status} successfully"})


@admin_bp.route("/drive/<int:drive_id>/status", methods=["PUT"])
@jwt_required()
def update_drive_status(drive_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    status = data.get("status")
    if status not in ["approved", "rejected"]:
        return jsonify({"msg": "Invalid status"}), 400

    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"msg": "Drive not found"}), 404

    drive.drive_approved_status = status
    db.session.commit()

    return jsonify({"msg": f"Drive {status} successfully"})


@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def get_all_companies():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    cached = cache_get("admin_companies")
    if cached:
        return jsonify(cached)

    companies = Company.query.all()
    result = []
    for company in companies:
        hr_user = User.query.get(company.user_id)
        result.append({
            "company_id": company.company_id,
            "company_name": company.company_name,
            "name": hr_user.name,
            "email": hr_user.email,
            "industry": company.industry,
            "description": company.description,
            "website": company.website,
            "company_approved_status": company.company_approved_status
        })

    cache_set("admin_companies", result, ttl=300)
    return jsonify(result)


@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def get_all_students():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    cached = cache_get("admin_students")
    if cached:
        return jsonify(cached)

    students = Student.query.all()
    result = []
    for student in students:
        student_user = User.query.get(student.user_id)
        result.append({
            "student_id": student.student_id,
            "name": student_user.name,
            "email": student_user.email,
            "roll_no": student.roll_no,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "year_of_passing": student.year_of_passing,
            "skills": student.skills,
            "resume_url": f"http://127.0.0.1:5000/resume/{student.resume}" if student.resume else None
        })

    cache_set("admin_students", result, ttl=300)
    return jsonify(result)


@admin_bp.route("/drives", methods=["GET"])
@jwt_required()
def get_all_drives():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    drives = Drive.query.all()
    result = []
    for drive in drives:
        company = Company.query.get(drive.company_id)
        branches = DriveBranch.query.filter_by(drive_id=drive.drive_id).all()
        branch_list = [b.branch for b in branches]
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
            "branches": branch_list
        })

    return jsonify(result)


@admin_bp.route("/report", methods=["GET"])
@jwt_required()
def get_placement_report():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    all_students = Student.query.all()
    total_students = len(all_students)

    all_companies = Company.query.all()
    company_stats = {
        "total": len(all_companies),
        "approved": len([c for c in all_companies if c.company_approved_status == "approved"]),
        "pending": len([c for c in all_companies if c.company_approved_status == "pending"]),
        "rejected": len([c for c in all_companies if c.company_approved_status == "rejected"])
    }

    all_drives = Drive.query.all()
    drive_stats = {
        "total": len(all_drives),
        "approved": len([d for d in all_drives if d.drive_approved_status == "approved"]),
        "pending": len([d for d in all_drives if d.drive_approved_status == "pending"]),
        "rejected": len([d for d in all_drives if d.drive_approved_status == "rejected"])
    }

    all_apps = Application.query.all()
    app_stats = {
        "total": len(all_apps),
        "applied": len([a for a in all_apps if a.status == "applied"]),
        "shortlisted": len([a for a in all_apps if a.status == "shortlisted"]),
        "selected": len([a for a in all_apps if a.status == "selected"]),
        "rejected": len([a for a in all_apps if a.status == "rejected"])
    }

    placement_rate = round((app_stats["selected"] / total_students * 100), 1) if total_students > 0 else 0
    branches_seen = list(set([s.branch for s in all_students if s.branch]))
    branch_stats = []
    for branch in branches_seen:
        branch_students = [s for s in all_students if s.branch == branch]
        branch_student_ids = [s.student_id for s in branch_students]
        selected_in_branch = len([
            a for a in all_apps if a.student_id in branch_student_ids and a.status == "selected"
        ])
        branch_stats.append({
            "branch": branch,
            "total_students": len(branch_students),
            "selected": selected_in_branch,
        })
    branch_stats.sort(key=lambda x: x["total_students"], reverse=True)

    top_companies = []
    for company in all_companies:
        drives = Drive.query.filter_by(company_id=company.company_id).all()
        drive_ids = [d.drive_id for d in drives]
        company_apps = [a for a in all_apps if a.drive_id in drive_ids]
        selected = len([a for a in company_apps if a.status == "selected"])
        top_companies.append({
            "company_name": company.company_name,
            "total_drives": len(drives),
            "total_applications": len(company_apps),
            "selected": selected
        })
    top_companies.sort(key=lambda x: (x["selected"], x["total_applications"]), reverse=True)
    top_companies = top_companies[:5]

    return jsonify({
        "students": {"total": total_students},
        "companies": company_stats,
        "drives": drive_stats,
        "applications": app_stats,
        "placement_rate": placement_rate,
        "branch_stats": branch_stats,
        "top_companies": top_companies
    })


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_admin_dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"msg": "Unauthorized"}), 403

    total_students = Student.query.count()
    total_companies = Company.query.count()
    active_drives = Drive.query.filter_by(drive_approved_status="approved").count()
    selected_count = Application.query.filter_by(status="selected").count()
    placement_rate = round((selected_count / total_students * 100), 1) if total_students > 0 else 0

    recent_companies_raw = Company.query.order_by(Company.company_id.desc()).limit(5).all()
    recent_companies = []
    for c in recent_companies_raw:
        hr = User.query.get(c.user_id)
        recent_companies.append({
            "company_id": c.company_id,
            "company_name": c.company_name,
            "status": c.company_approved_status,
            "hr_name": hr.name if hr else ""
        })

    recent_drives_raw = Drive.query.order_by(Drive.drive_id.desc()).limit(5).all()
    recent_drives = []
    for d in recent_drives_raw:
        company = Company.query.get(d.company_id)
        app_count = Application.query.filter_by(drive_id=d.drive_id).count()
        recent_drives.append({
            "drive_id": d.drive_id,
            "job_title": d.job_title,
            "company_name": company.company_name if company else "Unknown",
            "status": d.drive_approved_status,
            "application_count": app_count
        })

    return jsonify({
        "stats": {
            "total_companies": total_companies,
            "total_students": total_students,
            "active_drives": active_drives,
            "placement_rate": placement_rate
        },
        "recent_companies": recent_companies,
        "recent_drives": recent_drives
    })
