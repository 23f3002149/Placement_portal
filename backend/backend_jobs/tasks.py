import smtplib
import csv
import io
from email.message import EmailMessage
from datetime import datetime
from .celery_app import celery_app

@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, smtp_host, smtp_user, smtp_pass, admin_email, smtp_port, from_email, to_email, subject, body):
    """Send email via SMTP with retry logic"""
    try:
        # Ensure subject and body are strings
        subject = str(subject) if subject is not None else "No Subject"
        body = str(body) if body is not None else "No Body"
        from_email = str(from_email) if from_email else "noreply@placement.local"
        to_email = str(to_email) if to_email else "admin@placement.local"
        
        msg = EmailMessage()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            print(f"[email] sent to {to_email}")
            return {"status": "success", "to": to_email}
    except Exception as exc:
        print(f"[email] failed: {exc}")
        # Retry after 60 seconds, max 3 retries
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def notify_admin_application_task(app_config, student_roll_no, student_name, student_branch, drive_job_title, company_name):
    """Send email to admin when student applies"""
    subject = f"New application: {student_roll_no} -> {drive_job_title}"
    body = (
        f"Student: {student_name} (roll {student_roll_no})\n"
        f"Branch: {student_branch}\n"
        f"Drive: {drive_job_title} at {company_name}\n"
        f"Applied on: {datetime.utcnow().isoformat()} UTC\n"
    )
    
    send_email_task.delay(
        app_config.get("SMTP_HOST"),
        app_config.get("SMTP_USER"),
        app_config.get("SMTP_PASS"),
        app_config.get("ADMIN_EMAIL"),
        app_config.get("SMTP_PORT", 587),
        app_config.get("SMTP_USER"),
        app_config.get("ADMIN_EMAIL"),
        subject,
        body
    )


@celery_app.task
def notify_student_status_task(app_config, student_email, student_name, drive_job_title, company_name, status):
    """Send status update email to student"""
    subject = f"Your application status: {status.title()} - {drive_job_title}"
    body = (
        f"Hi {student_name},\n\n"
        f"Your application for '{drive_job_title}' at {company_name} is now '{status}'.\n\n"
        f"Thank you,\nPlacement Cell"
    )
    
    send_email_task.delay(
        app_config.get("SMTP_HOST"),
        app_config.get("SMTP_USER"),
        app_config.get("SMTP_PASS"),
        app_config.get("ADMIN_EMAIL"),
        app_config.get("SMTP_PORT", 587),
        app_config.get("SMTP_USER"),
        student_email,
        subject,
        body
    )


@celery_app.task
def notify_student_application_task(app_config, student_email, student_name, drive_job_title, company_name):
    """Send application confirmation email to student"""
    subject = f"Application Confirmation: {drive_job_title}"
    body = (
        f"Hi {student_name},\n\n"
        f"Thank you for applying to '{drive_job_title}' at {company_name}.\n\n"
        f"Your application has been successfully submitted. You will receive updates "
        f"regarding your application status via email.\n\n"
        f"Best of luck!\nPlacement Cell"
    )
    
    send_email_task.delay(
        app_config.get("SMTP_HOST"),
        app_config.get("SMTP_USER"),
        app_config.get("SMTP_PASS"),
        app_config.get("ADMIN_EMAIL"),
        app_config.get("SMTP_PORT", 587),
        app_config.get("SMTP_USER"),
        student_email,
        subject,
        body
    )


def _parse_interview_datetime(interview_dt):
    if isinstance(interview_dt, str):
        try:
            return datetime.fromisoformat(interview_dt)
        except ValueError:
            return datetime.strptime(interview_dt, "%Y-%m-%d %H:%M:%S")
    return interview_dt


@celery_app.task
def notify_interview_schedule_task(app_config, student_email, student_name, drive_job_title, company_name, interview_dt):
    """Send interview scheduled email to student"""
    interview_dt = _parse_interview_datetime(interview_dt)
    subject = f"Interview scheduled: {drive_job_title}"
    body = (
        f"Hi {student_name},\n\n"
        f"Your interview for '{drive_job_title}' at {company_name} is scheduled on "
        f"{interview_dt.strftime('%Y-%m-%d %H:%M UTC')}.\n\n"
        f"Good luck!\nPlacement Cell"
    )
    
    send_email_task.delay(
        app_config.get("SMTP_HOST"),
        app_config.get("SMTP_USER"),
        app_config.get("SMTP_PASS"),
        app_config.get("ADMIN_EMAIL"),
        app_config.get("SMTP_PORT", 587),
        app_config.get("SMTP_USER"),
        student_email,
        subject,
        body
    )
    
    # Schedule reminder after 2 minutes
    send_interview_reminder_task.apply_async(
        args=[app_config, student_email, student_name, drive_job_title, company_name, interview_dt.isoformat()],
        countdown=120
    )


@celery_app.task
def send_interview_reminder_task(app_config, student_email, student_name, drive_job_title, company_name, interview_dt):
    """Send interview reminder email (2 minutes after initial email)"""
    interview_dt = _parse_interview_datetime(interview_dt)
    subject = f"Reminder: Interview scheduled - {drive_job_title}"
    body = (
        f"Hi {student_name},\n\n"
        f"Reminder: your interview for '{drive_job_title}' is scheduled at "
        f"{interview_dt.strftime('%Y-%m-%d %H:%M UTC')}.\n\n"
        f"See you on time.\nPlacement Cell"
    )
    
    send_email_task.delay(
        app_config.get("SMTP_HOST"),
        app_config.get("SMTP_USER"),
        app_config.get("SMTP_PASS"),
        app_config.get("ADMIN_EMAIL"),
        app_config.get("SMTP_PORT", 587),
        app_config.get("SMTP_USER"),
        student_email,
        subject,
        body
    )


@celery_app.task
def export_student_applications_csv_task(student_id):
    """Export student applications as CSV"""
    try:
        # Lazy import to avoid circular dependency
        from database import db
        from model import Student, Application, Drive, Company
        
        student = Student.query.get(student_id)
        if not student:
            return {"status": "error", "message": "Student not found"}
        
        applications = Application.query.filter_by(student_id=student_id).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Application ID', 'Job Title', 'Company', 'Status', 'Applied Date'])
        
        for app in applications:
            drive = Drive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id)
            writer.writerow([
                app.application_id,
                drive.job_title,
                company.company_name if company else 'Unknown',
                app.status,
                app.applied_date.strftime("%Y-%m-%d") if app.applied_date else ''
            ])
        
        return {"status": "success", "csv": output.getvalue()}
    except Exception as e:
        print(f"[csv-export] failed: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task
def export_company_monthly_report_task(company_id):
    """Export company monthly report as CSV"""
    try:
        # Lazy import to avoid circular dependency
        from database import db
        from model import User, Student, Application, Drive, Company
        
        company = Company.query.get(company_id)
        if not company:
            return {"status": "error", "message": "Company not found"}
        
        drives = Drive.query.filter_by(company_id=company_id).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Application ID', 'Student Name', 'Job Title', 'Status', 'Applied Date'])
        
        for drive in drives:
            applications = Application.query.filter_by(drive_id=drive.drive_id).all()
            for app in applications:
                student = Student.query.get(app.student_id)
                student_user = User.query.get(student.user_id)
                writer.writerow([
                    app.application_id,
                    student_user.name if student_user else 'Unknown',
                    drive.job_title,
                    app.status,
                    app.applied_date.strftime("%Y-%m-%d") if app.applied_date else ''
                ])
        
        return {"status": "success", "csv": output.getvalue()}
    except Exception as e:
        print(f"[report-export] failed: {e}")
        return {"status": "error", "message": str(e)}
