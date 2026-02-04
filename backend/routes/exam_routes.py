from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback
import MySQLdb.cursors


def create_exam_routes(mysql):
    exam_bp = Blueprint('exam', __name__)

    # CREATE EXAM
    @exam_bp.route('/create', methods=['POST'])
    def create_exam():
        data = request.json

        exam_name = data.get('exam_name')
        exam_date = data.get('exam_date')
        exam_time = data.get('exam_time')
        duration = data.get('duration')
        total_questions = data.get('total_questions')
        max_marks = data.get('max_marks')
        faculty_email = data.get('faculty_email')

        if not all([
    exam_name, exam_date, exam_time,
    duration, total_questions, max_marks
]):

            return jsonify(success=False, message="Missing required fields"), 400

        try:
            exam_datetime = datetime.strptime(
                f"{exam_date} {exam_time}", "%Y-%m-%d %H:%M"
            )

            if exam_datetime < datetime.now():
                return jsonify(
                    success=False,
                    message="Exam date/time cannot be in the past"
                ), 400

            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO Entrance_Exam
                (Exam_Name, Exam_Date, Exam_Time, Duration_Minutes,
                 Total_Questions, Max_Marks, Faculty_Email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                exam_name, exam_date, exam_time,
                duration, total_questions, max_marks, faculty_email
            ))

            mysql.connection.commit()
            exam_id = cursor.lastrowid
            cursor.close()

            return jsonify(success=True, exam_id=exam_id)

        except Exception as e:
            print("❌ Create exam error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Database error"), 500

    # GET EXAMS (WITH APPLICANT COUNTS)
    @exam_bp.route('/get_exams/<faculty_email>', methods=['GET'])
    def get_exams(faculty_email):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("""
                SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time,
                       Duration_Minutes, Total_Questions, Max_Marks
                FROM Entrance_Exam
                WHERE Faculty_Email = %s
            """, (faculty_email,))
            exams = cursor.fetchall()

            exam_list = []

            for exam in exams:
                exam_id = exam["Exam_Id"]

                cursor.execute("""
                    SELECT COUNT(DISTINCT Applicant_Id) AS total
                    FROM applicant_exam_assign
                    WHERE Exam_Id = %s
                """, (exam_id,))
                total_applicants = cursor.fetchone()["total"]

                cursor.execute("""
                    SELECT COUNT(DISTINCT aa.Applicant_Id) AS attempted
                    FROM applicant_attempt aa
                    JOIN exam_paper ep
                      ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                    WHERE ep.Exam_Id = %s
                """, (exam_id,))
                attempted_applicants = cursor.fetchone()["attempted"]

                exam_list.append({
                    "Exam_Id": exam["Exam_Id"],
                    "Exam_Name": exam["Exam_Name"],
                    "Exam_Date": str(exam["Exam_Date"]),
                    "Exam_Time": str(exam["Exam_Time"]),
                    "Duration_Minutes": str(exam["Duration_Minutes"]),
                    "Total_Questions": exam["Total_Questions"],
                    "Max_Marks": exam["Max_Marks"],
                    "total_applicants": total_applicants,
                    "attempted_applicants": attempted_applicants
                })

            cursor.close()
            return jsonify(success=True, exams=exam_list)

        except Exception as e:
            print("❌ Get exams error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Server error"), 500

    # ✅ GET EXAM BY ID (FIXED)
    @exam_bp.route('/get_exam_by_id/<int:exam_id>', methods=['GET'])
    def get_exam_by_id(exam_id):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("""
                SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time, Duration_Minutes
                FROM Entrance_Exam
                WHERE Exam_Id = %s
            """, (exam_id,))

            exam = cursor.fetchone()
            cursor.close()

            print("DEBUG exam raw:", exam)

            if not exam:
                return jsonify(success=False, message="Exam not found"), 404

            # 🔥 Convert non-JSON-serializable fields
            exam["Exam_Date"] = str(exam["Exam_Date"])
            exam["Exam_Time"] = str(exam["Exam_Time"])
            exam["Duration_Minutes"] = str(exam["Duration_Minutes"])

            return jsonify(success=True, exam=exam)

        except Exception as e:
            print("❌ Get exam by id error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Server error"), 500

    # EXAM STATUS
    @exam_bp.route('/status/<int:exam_id>', methods=['GET'])
    def get_exam_status(exam_id):
        try:
            cursor = mysql.connection.cursor()

            cursor.execute("""
                SELECT COUNT(*) FROM entrance_question_bank
                WHERE Exam_Id = %s
            """, (exam_id,))
            qb_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM exam_paper
                WHERE Exam_Id = %s
            """, (exam_id,))
            qp_count = cursor.fetchone()[0]

            cursor.close()

            return jsonify(
                success=True,
                status={
                    "has_question_bank": qb_count > 0,
                    "has_question_paper": qp_count > 0
                }
            )

        except Exception as e:
            print("❌ Status error:", e)
            traceback.print_exc()
            return jsonify(success=False), 500

    # EXAM REMINDERS (DASHBOARD NOTIFICATION)
    #  EXAM REMINDERS (ADMIN + FACULTY)
    # =====================================================
    @exam_bp.route('/reminders', methods=['GET'])
    def exam_reminders():
        try:
            role = request.args.get("role")
            email = request.args.get("email")

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # -----------------------------
            # ADMIN → ALL EXAMS
            # -----------------------------
            if role == "Admin":
                cursor.execute("""
                    SELECT
                        Exam_Id,
                        Exam_Name,
                        Exam_Date,
                        Exam_Time,
                        Faculty_Email,
                        DATEDIFF(Exam_Date, CURDATE()) AS days_left
                    FROM Entrance_Exam
                    WHERE Exam_Date >= CURDATE()
                    ORDER BY Exam_Date ASC
                    LIMIT 10
                """)

            # -----------------------------
            # FACULTY → OWN EXAMS ONLY
            # -----------------------------
            elif role == "Faculty" and email:
                cursor.execute("""
                    SELECT
                        Exam_Id,
                        Exam_Name,
                        Exam_Date,
                        Exam_Time,
                        Faculty_Email,
                        DATEDIFF(Exam_Date, CURDATE()) AS days_left
                    FROM Entrance_Exam
                    WHERE Faculty_Email = %s
                      AND Exam_Date >= CURDATE()
                    ORDER BY Exam_Date ASC
                    LIMIT 5
                """, (email,))

            else:
                return jsonify(
                    success=False,
                    message="Invalid role or missing email"
                ), 400

            reminders = cursor.fetchall()
            cursor.close()

            # Convert date/time
            for exam in reminders:
                exam["Exam_Date"] = str(exam["Exam_Date"])
                exam["Exam_Time"] = str(exam["Exam_Time"])

            return jsonify(success=True, reminders=reminders)

        except Exception as e:
            print("❌ Exam reminder error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Server error"), 500

   
    return exam_bp
