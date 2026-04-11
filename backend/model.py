from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users" #iska matlab hai ki ye table ka naam "users" hoga database me

    user_id = db.Column(db.Integer, primary_key=True)#primary key me auto increment hota hai automatically, isliye humne auto increment ka use nahi kiya hai
    name = db.Column(db.String(100), nullable=False)#name of HR or student
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # company , student, admin
    
    student = db.relationship("Student", backref="user", uselist=False)#uselist=False Matlab:1 user → 1 student profile
    company = db.relationship("Company", backref="user", uselist=False)
   
class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False,unique=True)
    roll_no = db.Column(db.String(50), nullable=False, unique=True)
    branch = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float)
    year_of_passing = db.Column(db.Integer)
    skills = db.Column(db.Text)
    resume = db.Column(db.String(255))
    
    applications = db.relationship("Application",backref="student",cascade="all, delete")#cascade="all, delete" ka matlab hai ki jab bhi student delete hoga to uske saare applications bhi delete ho jayenge automatically
    # relationship ka use humne isliye kiya hai taki hume baar baar join query na likhni pade jab hume student ke applications fetch karne ho, hum directly student.applications se uske applications fetch kar sakte hain
    #backref="student" ka matlab hai ki hum application se bhi student ko access kar sakte hain, jaise application.student se hume uska student mil jayega

class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False,unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(100))
    description = db.Column(db.Text)
    website = db.Column(db.String(255))  
    company_approved_status = db.Column(db.String(20), default="pending")#pending, approved, rejected
    
    
    drives = db.relationship("Drive",backref="company",cascade="all, delete")
   
    
class Drive(db.Model):
    __tablename__ = "drives"
    
    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey("companies.company_id"),nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    package = db.Column(db.String(50))
    location = db.Column(db.String(100))
    cgpa_criteria = db.Column(db.Float)
    application_deadline = db.Column(db.DateTime)
    drive_approved_status = db.Column(db.String(20), default="pending")#pending, approved, rejected
    
    
    applications = db.relationship("Application",backref="drive",cascade="all, delete")
    branches = db.relationship("DriveBranch",backref="drive",cascade="all, delete")

class DriveBranch(db.Model):
    __tablename__ = "drive_branches"
    
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer,db.ForeignKey("drives.drive_id"),nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    
class Application(db.Model):
    __tablename__ = "applications"

    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer,db.ForeignKey("students.student_id"),nullable=False)
    drive_id = db.Column(db.Integer,db.ForeignKey("drives.drive_id"),nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="applied")

    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)# ye constraint ensure karta hai ki ek student ek hi drive ke liye sirf ek baar apply kar sakta hai, agar koi student same drive ke liye multiple applications bhejne ki koshish karega to database error throw karega
    #composite unique constraint banane ke liye humne __table_args__ ka use kiya hai, jisme humne db.UniqueConstraint ka use karke student_id aur drive_id ko unique banaya hai, aur uska naam "unique_application" diya hai
    #iska matlab ye bilkul nahi hai ki student_id unique ho isme ya fir drive_id unique ho ,,iska matlab hai ki dono ka combination unique ho
