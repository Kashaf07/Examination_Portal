from flask import Blueprint, request, jsonify
from MySQLdb.cursors import DictCursor

def create_exam_result_routes(mysql):
    exam_result_bp = Blueprint('exam_result', __name__)

    def is_exam_authorized(cursor, exam_id, email, role):
        if role == "Admin":
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s",
                (exam_id,)
            )
        else:
            cursor.execute(
                """
                SELECT 1 FROM entrance_exam
                WHERE Exam_Id = %s AND Faculty_Email = %s
                """,
                (exam_id, email)
            )
        return cursor.fetchone() is not None

    @exam_result_bp.route('/exam/<int:exam_id>/results', methods=['GET'])
    def get_exam_results(exam_id):

        email = request.args.get('email')
        role = request.args.get('role')

        if not email or not role:
            return jsonify(success=False, message="Missing authentication"), 400

        try:
            cursor = mysql.connection.cursor(DictCursor)

            # 🔐 Proper Role Validation
            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            if not is_exam_authorized(cursor, exam_id, email, role):
                return jsonify(success=False, message="Unauthorized Access"), 403

            # 📘 Get Exam Info
            cursor.execute("""
                SELECT Exam_Name, Exam_Date, Exam_Time
                FROM entrance_exam
                WHERE Exam_Id = %s
            """, (exam_id,))
            exam = cursor.fetchone()

            if not exam:
                return jsonify(success=False, message="Exam not found"), 404

            # 📊 Get Student Results
            cursor.execute("""
                SELECT 
                    a.Applicant_Id,
                    ap.Full_Name AS Student_Name,
                    a.Marks_Obtained
                FROM applicant_attempt a
                JOIN exam_paper ep ON ep.Exam_Paper_Id = a.Exam_Paper_Id
                JOIN applicants ap ON ap.Applicant_Id = a.Applicant_Id
                WHERE ep.Exam_Id = %s
                AND a.Status = 'Submitted'
                ORDER BY a.Applicant_Id ASC
            """, (exam_id,))

            results = cursor.fetchall()

            return jsonify(
                success=True,
                exam_name=exam["Exam_Name"],
                exam_date=exam["Exam_Date"].strftime('%Y-%m-%d') if exam["Exam_Date"] else None,
                exam_time=str(exam["Exam_Time"]) if exam["Exam_Time"] else None,
                results=results
            )

        except Exception as e:
            return jsonify(success=False, message=str(e)), 500

    return exam_result_bp