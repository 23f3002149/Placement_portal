"""
Notification wrapper functions that delegate to Celery tasks
"""
from backend_jobs.tasks import (
    notify_admin_application_task, 
    notify_student_status_task,
    notify_student_application_task,
    notify_interview_schedule_task
)


def _extract_config(app_config):
    """Extract only JSON-serializable config values"""
    return {
        "SMTP_HOST": str(app_config.get("SMTP_HOST", "")),
        "SMTP_USER": str(app_config.get("SMTP_USER", "")),
        "SMTP_PASS": str(app_config.get("SMTP_PASS", "")),
        "SMTP_PORT": str(app_config.get("SMTP_PORT", "587")),
        "ADMIN_EMAIL": str(app_config.get("ADMIN_EMAIL", ""))
    }


def notify_admin_application(app_config, student, drive):
    """Queue email notification for admin when student applies"""
    company_name = drive.company.company_name if drive.company else 'Company'
    config_dict = _extract_config(app_config)
    notify_admin_application_task.delay(
        config_dict,
        student.roll_no,
        student.user.name,
        student.branch,
        drive.job_title,
        company_name
    )


def notify_student_status(app_config, student_user, drive, status):
    """Queue status update email to student"""
    company_name = drive.company.company_name if drive.company else 'the company'
    config_dict = _extract_config(app_config)
    notify_student_status_task.delay(
        config_dict,
        student_user.email,
        student_user.name,
        drive.job_title,
        company_name,
        status
    )


def notify_student_application(app_config, student_user, drive):
    """Queue application confirmation email to student"""
    company_name = drive.company.company_name if drive.company else 'the company'
    config_dict = _extract_config(app_config)
    notify_student_application_task.delay(
        config_dict,
        student_user.email,
        student_user.name,
        drive.job_title,
        company_name
    )


def notify_interview_schedule(app_config, student_user, drive, interview_dt):
    """Queue interview scheduled email to student"""
    company_name = drive.company.company_name if drive.company else 'the company'
    config_dict = _extract_config(app_config)
    notify_interview_schedule_task.delay(
        config_dict,
        student_user.email,
        student_user.name,
        drive.job_title,
        company_name,
        interview_dt.isoformat() if hasattr(interview_dt, 'isoformat') else str(interview_dt)
    )