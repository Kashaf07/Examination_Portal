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

            # ==================================================
            # 🔐 AUTHORIZATION CHECK
            # ==================================================

            # 1️⃣ Get Exam + Faculty info for this attempt
            cursor.execute("""
                SELECT ee.Exam_Id, ee.Faculty_Email
                FROM applicant_attempt aa
                JOIN exam_paper ep 
                    ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN Entrance_Exam ee 
                    ON ep.Exam_Id = ee.Exam_Id
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
            faculty_email_db = (exam_data["Faculty_Email"] or "").strip().lower()
            user_email = email.strip().lower()

            # 2️⃣ Admin → Always allowed
            if role.lower() == "admin":
                pass

            # 3️⃣ Faculty → Only if own exam
            elif role.lower() == "faculty":
                if faculty_email_db != user_email:
                    cursor.close()
                    return jsonify({
                        "success": False,
                        "error": "Unauthorized Access"
                    }), 403

            # 4️⃣ Any other role → deny
            else:
                cursor.close()
                return jsonify({
                    "success": False,
                    "error": "Unauthorized Access"
                }), 403

            # ==================================================
            # 📄 FETCH ANSWERS
            # ==================================================

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