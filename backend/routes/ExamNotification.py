from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from flask_mail import Message

exam_notify_bp = Blueprint("exam_notify_bp", __name__)

# ==========================================================
# 📧 EXISTING: SEND EMAIL TO APPLICANTS (UNCHANGED)
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
    return jsonify({"success": True})


# ==========================================================
# 🔔 FACULTY 10-MINUTE REMINDER (FINAL FIXED VERSION)
# ==========================================================
def notify_faculty_internal():
    try:
        mysql = current_app.config["MYSQL"]
        mail = current_app.extensions["mail"]

        cur = mysql.connection.cursor()

        now = datetime.now()
        window_end = now + timedelta(minutes=1)

        cur.execute("""
            SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time, Faculty_Email
            FROM entrance_exam
            WHERE notify_10min = 0
        """)
        exams = cur.fetchall()

        for exam_id, name, exam_date, exam_time, faculty_email in exams:

            # ✅ FIX: normalize Exam_Time
            if isinstance(exam_time, timedelta):
                total_seconds = int(exam_time.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                exam_time = datetime.strptime(f"{hours}:{minutes}", "%H:%M").time()

            elif isinstance(exam_time, str):
                exam_time = datetime.strptime(exam_time, "%H:%M:%S").time()

            # ✅ SAFE datetime creation
            exam_datetime = datetime.combine(exam_date, exam_time)
            reminder_time = exam_datetime - timedelta(minutes=10)

        diff_seconds = (exam_datetime - now).total_seconds()
        if 0 <= diff_seconds <= 600:  # within 10 minutes

                # 📧 EMAIL
                msg = Message(
                    subject=f"⏰ Exam Reminder: {name}",
                    recipients=[faculty_email],
                    body=f"""
Hello,

This is a reminder that your exam "{name}" will start at {exam_time.strftime('%H:%M')}.

Please be ready.

Regards,
Examination Portal
"""
                )
                mail.send(msg)

                # 🔔 DASHBOARD NOTIFICATION
                cur.execute("""
                    INSERT INTO notification (Title, Message, Target_Role)
                    VALUES (%s, %s, 'Faculty')
                """, (
                    "Exam Reminder",
                    f'Exam "{name}" will start in 10 minutes.'
                ))

                # ✅ MARK SENT
                cur.execute("""
                    UPDATE entrance_exam
                    SET notify_10min = 1
                    WHERE Exam_Id = %s
                """, (exam_id,))

                mysql.connection.commit()

    except Exception as e:
        print("❌ Faculty scheduler error:", e)


# expose function to scheduler
exam_notify_bp.notify_faculty_internal = notify_faculty_internal


# ==========================================================
# 🔁 OPTIONAL: MANUAL TEST ENDPOINT
# ==========================================================
@exam_notify_bp.route("/api/notify/faculty-exams", methods=["GET"])
def manual_trigger():
    notify_faculty_internal()
    return jsonify({"success": True})
