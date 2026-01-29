from datetime import datetime, timedelta
from flask import current_app

def faculty_10min_scheduler(mysql, mail):
    try:
        with current_app.app_context():
            cur = mysql.connection.cursor()

            cur.execute("""
                SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time, Faculty_Email
                FROM entrance_exam
                WHERE notify_10min = 0
            """)
            exams = cur.fetchall()

            now = datetime.now()

            for exam in exams:
                exam_id, name, date, time, faculty_email = exam

                exam_datetime = datetime.combine(date, time)

                if exam_datetime - timedelta(minutes=10) <= now < exam_datetime:
                    # 🔔 INSERT DASHBOARD NOTIFICATION
                    cur.execute("""
                        INSERT INTO notification (Title, Message, Target_Role)
                        VALUES (%s, %s, 'FACULTY')
                    """, (
                        "Exam Reminder",
                        f"Your exam '{name}' will start in 10 minutes."
                    ))

                    # ✉️ SEND EMAIL
                    msg = mail.send_message(
                        subject=f"Exam Reminder: {name}",
                        recipients=[faculty_email],
                        body=f"Your exam '{name}' will start in 10 minutes."
                    )

                    # ✅ UPDATE FLAG
                    cur.execute("""
                        UPDATE entrance_exam
                        SET notify_10min = 1
                        WHERE Exam_Id = %s
                    """, (exam_id,))

                    mysql.connection.commit()

    except Exception as e:
        print("❌ Faculty scheduler error:", e)
