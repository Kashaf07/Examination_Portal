from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from flask_mail import Message
import MySQLdb.cursors

exam_notify_bp = Blueprint("exam_notify_bp", __name__)

# ==========================================================
# 📧 SEND EMAIL TO APPLICANTS
# ==========================================================
@exam_notify_bp.route("/api/send_exam_notification", methods=["POST"])
def send_exam_notification():
    mysql = current_app.config["MYSQL"]
    data = request.get_json()
    exam_id = data.get("exam_id")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT Exam_Name, Exam_Date, Exam_Time
        FROM entrance_exam
        WHERE Exam_Id = %s
    """, (exam_id,))
    exam = cur.fetchone()

    if not exam:
        cur.close()
        return jsonify({"error": "Exam not found"}), 404

    exam_name, exam_date, exam_time = exam

    cur.execute("SELECT Email, Full_Name FROM applicants")
    students = cur.fetchall()

    for email, name in students:
        msg = Message(
            subject=f"Exam Notification - {exam_name}",
            recipients=[email],
            body=f"""
Dear {name},

Your exam "{exam_name}" is scheduled on {exam_date} at {exam_time}.

Best of luck!
"""
        )
        current_app.extensions["mail"].send(msg)

    cur.close()
    return jsonify(success=True)


# ==========================================================
# 🔔 FACULTY 10-MINUTE REMINDER (DB-SUPPORTED)
# ==========================================================
def notify_faculty_internal():
    mysql = current_app.config["MYSQL"]
    mail = current_app.extensions["mail"]

    try:
        cur = mysql.connection.cursor()
        now = datetime.now()

        cur.execute("""
            SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time, Faculty_Email
            FROM entrance_exam
            WHERE notify_10min = 0
        """)
        exams = cur.fetchall()

        for exam_id, name, exam_date, exam_time, faculty_email in exams:

            # Normalize Exam_Time
            if isinstance(exam_time, timedelta):
                total_seconds = int(exam_time.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                exam_time = datetime.strptime(f"{hours}:{minutes}", "%H:%M").time()

            elif isinstance(exam_time, str):
                exam_time = datetime.strptime(exam_time, "%H:%M:%S").time()

            exam_datetime = datetime.combine(exam_date, exam_time)
            diff_seconds = (exam_datetime - now).total_seconds()

            # within 10 minutes
            if 0 <= diff_seconds <= 600:

                # 📧 EMAIL TO FACULTY
                msg = Message(
                    subject=f"⏰ Exam Reminder: {name}",
                    recipients=[faculty_email],
                    body=f"""
Hello,

This is a reminder that your exam "{name}" will start at {exam_time.strftime('%H:%M')}.

Regards,
Examination Portal
"""
                )
                mail.send(msg)

                # 🔔 DASHBOARD NOTIFICATION (WITH EXAM + FACULTY INFO)
                cur.execute("""
    INSERT INTO notification
    (Title, Message, Target_Role, Exam_Id, Faculty_Email)
    VALUES (%s, %s, 'Faculty', %s, %s)
""", (
    "Exam Reminder",
    f'Exam "{name}" will start in 10 minutes.',
    exam_id,
    faculty_email
))

                # Mark reminder sent
                cur.execute("""
                    UPDATE entrance_exam
                    SET notify_10min = 1
                    WHERE Exam_Id = %s
                """, (exam_id,))

                mysql.connection.commit()

        cur.close()

    except Exception as e:
        print("❌ Faculty scheduler error:", e)


# expose function to scheduler
exam_notify_bp.notify_faculty_internal = notify_faculty_internal


# ==========================================================
# 🔔 ADMIN – GET ALL FACULTY NOTIFICATIONS (WITH FACULTY NAME)
# ==========================================================
@exam_notify_bp.route("/api/admin/notifications", methods=["GET"])
def get_admin_notifications():
    mysql = current_app.config["MYSQL"]
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT
            e.Exam_Id,
            e.Exam_Name,
            e.Exam_Date,
            e.Exam_Time,
            f.F_Name AS Faculty_Name
        FROM entrance_exam e
        JOIN mst_faculty f
            ON e.Faculty_Email = f.F_Email
        WHERE
            STR_TO_DATE(
                CONCAT(e.Exam_Date, ' ', e.Exam_Time),
                '%Y-%m-%d %H:%i:%s'
            ) > NOW()
        ORDER BY
            STR_TO_DATE(
                CONCAT(e.Exam_Date, ' ', e.Exam_Time),
                '%Y-%m-%d %H:%i:%s'
            ) ASC
    """)

    rows = cur.fetchall()
    cur.close()

    # ✅ FIX: convert timedelta to string
    reminders = []
    for r in rows:
        exam_time = r["Exam_Time"]

        if isinstance(exam_time, timedelta):
            total_seconds = int(exam_time.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            exam_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        reminders.append({
            "Exam_Id": r["Exam_Id"],
            "Exam_Name": r["Exam_Name"],
            "Exam_Date": r["Exam_Date"].strftime("%Y-%m-%d"),
            "Exam_Time": exam_time,
            "Faculty_Name": r["Faculty_Name"]
        })

    return jsonify(success=True, reminders=reminders)

# ==========================================================
# 🔁 MANUAL TEST ENDPOINT
# ==========================================================
@exam_notify_bp.route("/api/notify/faculty-exams", methods=["GET"])
def manual_trigger():
    notify_faculty_internal()
    return jsonify(success=True)
