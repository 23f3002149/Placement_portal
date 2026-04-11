from flask import Flask ,jsonify,request,send_from_directory,make_response
from database import db
from model import *
from werkzeug.security import generate_password_hash, check_password_hash# ye ek mathematical function hai jo password ko hash karne ke liye use hota hai, isse hum apne users ke passwords ko securely store kar sakte hain database me, jab bhi user login karega to hum check_password_hash function ka use karke uske input password ko hash karke database me stored hash se compare karenge, agar dono match karte hain to user ko authenticate kar denge
from flask_jwt_extended import JWTManager , create_access_token , get_jwt_identity , jwt_required# ye ek extension hai flask ke liye jo JSON Web Tokens (JWT) ko handle karta hai, isse hum apne APIs ko secure kar sakte hain, jab bhi user login karega to hum usko ek JWT token generate karke denge, aur jab bhi user koi protected API ko access karega to us token ko verify karenge, agar token valid hai to user ko access de denge, nahi to access deny kar denge
from flask_cors import CORS
from datetime import datetime
import os , json
from dotenv import load_dotenv
from backend_jobs.celery_app import celery_app
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from routes.student_routes import student_bp
from cache_utils import cache_get, cache_set, cache_delete

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Celery config
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
celery_app.conf.update(app.config)
# Resume upload folder configure karo
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'instance', 'resumes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'# ye configuration setting hai jo SQLAlchemy ko batati hai ki hum kis database ka use kar rahe hain, is case me hum SQLite database ka use kar rahe hain jiska naam placement.db hai, agar hum MySQL ya PostgreSQL ka use karna chahte hain to hume is URI ko accordingly change karna hoga, jaise MySQL ke liye mysql+pymysql://username:password@localhost/dbname aur PostgreSQL ke liye postgresql://username:password@localhost/dbname
app.config["JWT_SECRET_KEY"] = "placement-super-secret"# ye secret key hai jo JWT tokens ko sign karne ke liye use hoti hai, isse hum apne tokens ko secure kar sakte hain, is key ko kisi ke sath share nahi karna chahiye, aur production environment me isse aur bhi strong rakhna chahiye

# Load SMTP config from environment variables
app.config["SMTP_HOST"] = os.getenv("SMTP_HOST")
app.config["SMTP_USER"] = os.getenv("SMTP_USER")
app.config["SMTP_PASS"] = os.getenv("SMTP_PASS")
app.config["SMTP_PORT"] = os.getenv("SMTP_PORT", "587")
app.config["ADMIN_EMAIL"] = os.getenv("ADMIN_EMAIL")

db.init_app(app)# ye line SQLAlchemy ko Flask app ke sath initialize karne ke liye use hoti hai, isse hum apne Flask app me database operations perform kar sakte hain

jwt = JWTManager(app)# ye line JWTManager ko Flask app ke sath initialize karne ke liye use hoti hai, isse hum apne Flask app me JWT tokens ko handle kar sakte hain, jaise token generate karna, token verify karna, etc.


app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)




# APIs for our placement portal


#login Page ko kholne ka api
@app.route("/")
def home():
    return "Placement Portal API"




@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]
    role=data["role"] #  get role from request

    user = User.query.filter_by(email=email, role=role).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid password"}), 401

    access_token = create_access_token(identity=user.user_id)

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "role": user.role 
    })



#Password changing API(Common for All Users)
@app.route("/change_password", methods=["POST"])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    # User Validation
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Validation
    if not old_password or not new_password:
        return jsonify({"msg": "All fields are required"}), 400

    # Verify old password
    if not check_password_hash(user.password, old_password):
        return jsonify({"msg": "Old password is incorrect"}), 401

    # Update password
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({
        "msg": "Password changed successfully",
        "role": user.role
    }), 200



# Resume APIs 
# Resume file serve karne ki API (download/view)
@app.route("/resume/<filename>", methods=["GET"])
# @jwt_required()
def serve_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)#agar kisi aur port pe run karna hai to app.run(debug=True, port=5001) isse app 5001 port pe run hoga, default 5000 hota hai