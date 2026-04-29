from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail
from db_config import init_mysql
import os, atexit
from groq import Groq
import json
from dotenv import load_dotenv

load_dotenv()

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
from routes.exam_result_routes import create_exam_result_routes
from routes.exam_analytics_routes import create_exam_analytics_routes
from routes.profile_routes import create_profile_routes
from routes.keystroke_routes import create_keystroke_routes

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

# ---------------- GROQ CLIENT FOR AI GENERATION ----------------
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- MAIL CONFIG ----------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "examinationportal2025@gmail.com"
app.config["MAIL_PASSWORD"] = "zwdp rwro piku dwib"   # App password
app.config["MAIL_DEFAULT_SENDER"] = ("Examination Portal", "examinationportal2025@gmail.com")

mail = Mail(app)

# ---------------- REGISTER BLUEPRINTS ----------------
app.register_blueprint(create_auth_routes(mysql), url_prefix="/api/auth")
app.register_blueprint(create_question_routes(mysql), url_prefix="/api/questions")
app.register_blueprint(create_exam_routes(mysql), url_prefix="/api/exam")
app.register_blueprint(create_add_students_bp(mysql), url_prefix="/api")

app.register_blueprint(create_faculty_routes(mysql), url_prefix="/api/faculty")
app.register_blueprint(create_view_responses_bp(mysql), url_prefix="/api")
app.register_blueprint(create_faculty_groups_routes(mysql), url_prefix="/api")
app.register_blueprint(create_exam_result_routes(mysql), url_prefix="/api")
app.register_blueprint(create_exam_analytics_routes(mysql))

# 🔔 FACULTY NOTIFICATION BLUEPRINT
app.register_blueprint(exam_notify_bp)

exam_paper_bp = create_exam_paper_routes(mysql)
app.register_blueprint(exam_paper_bp, url_prefix="/api/paper")

# ✅ STUDENT EMAIL ROUTES (UNCHANGED)
app.register_blueprint(create_send_email_routes(mysql))

# 🔥 REGISTER WITH DIFFERENT URL PREFIXES TO AVOID CONFLICTS
# Exam applicants: /api/exam-groups/<id>/applicants  
app.register_blueprint(create_add_applicants_exam_bp(mysql), url_prefix="/api/exam-groups")

# Group management: /api/groups/<id>/applicants
app.register_blueprint(group_bp, url_prefix="/api/groups")

app.register_blueprint(create_assign_routes(mysql))
app.register_blueprint(create_applicants_bp(mysql))
app.register_blueprint(create_assigned_applicants_routes(mysql))
app.register_blueprint(create_view_answers_bp(mysql))
app.register_blueprint(create_admin_routes(mysql), url_prefix="/api/admin")

student_bp = create_student_routes(mysql)
app.register_blueprint(student_bp, url_prefix="/api/student")

app.register_blueprint(create_profile_routes(mysql), url_prefix="/api/profile")
app.register_blueprint(create_keystroke_routes(mysql), url_prefix="/api/keystroke")

# ---------------- AI QUESTION GENERATION ROUTES ----------------
@app.route("/generate-paper", methods=["POST"])
def generate_paper():
    try:
        data = request.get_json()
        subject = data.get("subject")
        topics = data.get("topics")
        num_questions = data.get("num_questions")
        difficulty = data.get("difficulty")
        question_type = data.get("question_type")

        if not all([subject, topics, num_questions, difficulty, question_type]):
            return jsonify({"error": "Missing required fields"}), 400

        prompt = f"""
        Generate {num_questions} {difficulty} level {question_type} questions for subject "{subject}".
        Topics: {topics}
        Rules:
        - MCQ → include 4 options in array
        - Fill → blank type
        - One word → short answer
        - True/False → include answer
        - Descriptive → detailed answer
        Return ONLY valid JSON array:
        [{{"question":"...","options":["A","B","C","D"],"answer":"...","difficulty":"{difficulty}"}}]
        """

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return only JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return jsonify(json.loads(raw))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/questions/add-generated", methods=["POST"])
def add_generated_questions():
    try:
        data = request.get_json()
        exam_id = data.get("exam_id")
        questions = data.get("questions")
        email = data.get("email")
        role = data.get("role")

        if not all([exam_id, questions, email, role]):
            return jsonify({"error": "Missing required fields"}), 400

        conn = mysql.connection
        cursor = conn.cursor()

        # Authorization check
        if role == "Admin":
            cursor.execute("SELECT 1 FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
        else:
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s AND Faculty_Email = %s",
                (exam_id, email)
            )

        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Unauthorized Access"}), 403

        # Insert questions
        for q in questions:
            question_text = q.get("question")
            options = q.get("options", [])
            answer = q.get("answer")
            difficulty = q.get("difficulty", "Medium")
            question_type = q.get("question_type", "MCQ")

            option_a = options[0] if len(options) > 0 else None
            option_b = options[1] if len(options) > 1 else None
            option_c = options[2] if len(options) > 2 else None
            option_d = options[3] if len(options) > 3 else None

            cursor.execute("""
                INSERT INTO entrance_question_bank
                (Exam_Id, Question_Type, Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer, Marks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (exam_id, question_type, question_text, option_a, option_b, option_c, option_d, answer, 1))

        conn.commit()
        cursor.close()

        return jsonify({"message": f"{len(questions)} questions added successfully."})

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({"error": str(e)}), 500

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
    app.run(host="0.0.0.0", port=5000, debug=True)