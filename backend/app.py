from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from db_config import init_mysql
import os, atexit

# 🔔 Scheduler
from apscheduler.schedulers.background import BackgroundScheduler

# ---------------- ROUTE IMPORTS ----------------
from routes.auth_routes import create_auth_routes
from routes.question_routes import create_question_routes
from routes.exam_routes import create_exam_routes
from routes.admin_routes import create_admin_routes

# 🔔 FACULTY NOTIFICATION (FACTORY STYLE)
from routes.ExamNotification import exam_notify_bp


from routes.applicants import create_applicants_bp
from routes.AddApplicants_exam import create_add_applicants_exam_bp
from routes.assign_applicants import create_assign_routes

# ✅ STUDENT EMAIL (DO NOT REMOVE)
from routes.send_exam_email import create_send_email_routes

from routes.assigned_applicants_routes import create_assigned_applicants_routes
from routes.exam_paper_routes import create_exam_paper_routes
from routes.student_routes import create_student_routes
from routes.AddStudents import create_add_students_bp
from routes.faculty_routes import create_faculty_routes
from routes.ViewResponses import create_view_responses_bp
from routes.ViewAnswers import create_view_answers_bp
from routes.faculty_groups import create_faculty_groups_routes
from routes.groups_routes import group_bp

# ---------------- APP ----------------
app = Flask(__name__)

# ---------------- CORS ----------------
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# ---------------- MYSQL ----------------
mysql = init_mysql(app)
app.config["MYSQL"] = mysql

# ---------------- MAIL CONFIG ----------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "examinationportal2025@gmail.com"
app.config["MAIL_PASSWORD"] = "zwdp rwro piku dwib"   # App password
app.config["MAIL_DEFAULT_SENDER"] = "izmashaikh7681@gmail.com"

mail = Mail(app)

# ---------------- REGISTER BLUEPRINTS ----------------
app.register_blueprint(create_auth_routes(mysql), url_prefix="/api/auth")
app.register_blueprint(create_question_routes(mysql), url_prefix="/api/questions")
app.register_blueprint(create_exam_routes(mysql), url_prefix="/api/exam")
app.register_blueprint(create_add_students_bp(mysql), url_prefix="/api")

app.register_blueprint(create_faculty_routes(mysql), url_prefix="/api/faculty")
app.register_blueprint(create_view_responses_bp(mysql), url_prefix="/responses")
app.register_blueprint(create_faculty_groups_routes(mysql), url_prefix="/api/faculty-groups")

# 🔔 FACULTY NOTIFICATION BLUEPRINT
app.register_blueprint(exam_notify_bp)

exam_paper_bp = create_exam_paper_routes(mysql)
app.register_blueprint(exam_paper_bp, url_prefix="/api/paper")

# ✅ STUDENT EMAIL ROUTES (UNCHANGED)
app.register_blueprint(create_send_email_routes(mysql))

app.register_blueprint(create_add_applicants_exam_bp(mysql), url_prefix="/api")
app.register_blueprint(create_assign_routes(mysql))
app.register_blueprint(create_applicants_bp(mysql))
app.register_blueprint(create_assigned_applicants_routes(mysql))
app.register_blueprint(create_view_answers_bp(mysql))
app.register_blueprint(create_admin_routes(mysql), url_prefix="/api/admin")
app.register_blueprint(group_bp, url_prefix="/api/groups")

student_bp = create_student_routes(mysql)
app.register_blueprint(student_bp, url_prefix="/api/student")

# ---------------- 🔔 SCHEDULER (SAFE + CONTEXT AWARE) ----------------
scheduler = BackgroundScheduler()

def faculty_notification_job():
    """
    Wrapper to ensure Flask app context exists
    """
    with app.app_context():
        exam_notify_bp.notify_faculty_internal()

scheduler.add_job(
    func=faculty_notification_job,
    trigger="interval",
    minutes=1,
    id="faculty_exam_10min_reminder",
    replace_existing=True
)

# Prevent duplicate scheduler (Flask reload fix)
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler.start()

atexit.register(lambda: scheduler.shutdown())

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
