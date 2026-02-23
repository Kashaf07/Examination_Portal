from flask import Blueprint, jsonify, request
import MySQLdb.cursors

def create_view_answers_bp(mysql):
    view_answers_bp = Blueprint('view_answers', __name__)

    @view_answers_bp.route('/api/answers/<int:attempt_id>', methods=['GET'])
    def get_answers(attempt_id):
        try:
            email = request.args.get("email")
            role = request.args.get("role")

            if not email or not role:
                return jsonify({
                    "success": False,
                    "error": "Missing authentication details"
                }), 403

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # ===============================
            # 🔐 AUTHORIZATION CHECK
            # ===============================

            # 1️⃣ Get Exam_Id related to this attempt
            cursor.execute("""
                SELECT ee.Exam_Id
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN entrance_exam ee ON ep.Exam_Id = ee.Exam_Id
                WHERE aa.Attempt_Id = %s
            """, (attempt_id,))

            exam_data = cursor.fetchone()

            if not exam_data:
                cursor.close()
                return jsonify({
                    "success": False,
                    "error": "Attempt not found"
                }), 404

            exam_id = exam_data["Exam_Id"]

            # 2️⃣ If Faculty → Check if assigned to this exam
            if role == "Faculty":
                cursor.execute("""
                    SELECT 1
                    FROM faculty_exam_assignment
                    WHERE Exam_Id = %s AND Faculty_Email = %s
                """, (exam_id, email))

                authorized = cursor.fetchone()

                if not authorized:
                    cursor.close()
                    return jsonify({
                        "success": False,
                        "error": "Unauthorized Access"
                    }), 403

            # 3️⃣ If Admin → allow automatically
            # (You can also add extra admin check here if needed)

            # ===============================
            # 📄 FETCH ANSWERS
            # ===============================

            cursor.execute("""
                SELECT 
                    aa.Answer_Id,
                    aa.Attempt_Id,
                    aa.Question_Id,
                    aa.Selected_Option_Id,
                    aa.Answer_Text,
                    qb.Question_Type,
                    qb.Question_Text,
                    qb.Option_A,
                    qb.Option_B,
                    qb.Option_C,
                    qb.Option_D,
                    qb.Correct_Answer
                FROM applicant_answers aa
                JOIN entrance_question_bank qb
                    ON aa.Question_Id = qb.Question_Id
                WHERE aa.Attempt_Id = %s
                ORDER BY aa.Answer_Id
            """, (attempt_id,))

            answers = cursor.fetchall()
            cursor.close()

            return jsonify({
                "success": True,
                "answers": answers
            }), 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    return view_answers_bp