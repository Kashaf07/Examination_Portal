from flask import Blueprint, request, jsonify
import MySQLdb.cursors

def create_view_responses_bp(mysql):
    view_responses_bp = Blueprint('view_responses', __name__)

    @view_responses_bp.route('/exam/can-view-responses', methods=['GET'])
    def can_view_responses():
        exam_id = request.args.get("exam_id")
        email = request.args.get("email")
        role = request.args.get("role")  # Admin / Faculty

        if not exam_id or not email or not role:
            return jsonify(success=False), 400

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 🔴 Admin → exam must exist
        if role == "Admin":
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s",
                (exam_id,)
            )

        # 🔵 Faculty → exam must belong to them
        else:
            cursor.execute(
                """
                SELECT 1
                FROM entrance_exam
                WHERE Exam_Id = %s
                AND Faculty_Email = %s
                """,
                (exam_id, email)
            )

        exam = cursor.fetchone()
        cursor.close()

        if not exam:
            return jsonify(success=False), 403

        return jsonify(success=True), 200

    @view_responses_bp.route('/attempts', methods=['GET'])
    def get_attempts():
        exam_id = request.args.get('exam_id')
        email = request.args.get('email')
        role = request.args.get('role')  # Admin / Faculty

        # 🔐 BASIC VALIDATION
        if not exam_id or not email or not role:
            return jsonify({
                "success": False,
                "message": "Unauthorized access"
            }), 403

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # 🔒 AUTHORIZATION CHECK (ANTI URL-TAMPERING)
            if role == "Admin":
                # Admin → exam must exist
                cursor.execute(
                    "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s",
                    (exam_id,)
                )
            else:
                # Faculty → exam must belong to this faculty
                cursor.execute(
                    """
                    SELECT 1
                    FROM entrance_exam
                    WHERE Exam_Id = %s
                    AND Faculty_Email = %s
                    """,
                    (exam_id, email)
                )

            if not cursor.fetchone():
                cursor.close()
                return jsonify({
                    "success": False,
                    "message": "You are not allowed to view this exam responses"
                }), 403

            # ✅ FETCH ATTEMPTS (AUTHORIZED)
            query = """
                SELECT 
                    aa.Attempt_Id,
                    aa.Applicant_Id,
                    aa.Student_Email, 
                    aa.Start_Time,
                    aa.End_Time,
                    aa.Marks_Obtained,
                    ep.Exam_Paper_Id,
                    ep.Title AS Exam_Paper_Title, 
                    ee.Exam_Id,
                    ee.Exam_Name,
                    ee.Max_Marks,
                    ag.Status
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN entrance_exam ee ON ep.Exam_Id = ee.Exam_Id
                LEFT JOIN auto_grading ag ON aa.Attempt_Id = ag.Attempt_Id
                WHERE ee.Exam_Id = %s
                ORDER BY ep.Exam_Paper_Id, aa.Start_Time DESC
            """

            cursor.execute(query, (exam_id,))
            rows = cursor.fetchall()
            cursor.close()

            # 🧹 DATA CLEANUP
            for row in rows:
                row['Start_Time'] = (
                    row['Start_Time'].strftime("%Y-%m-%d %H:%M:%S")
                    if row['Start_Time'] else None
                )
                row['End_Time'] = (
                    row['End_Time'].strftime("%Y-%m-%d %H:%M:%S")
                    if row['End_Time'] else None
                )
                row['Marks_Obtained'] = (
                    float(row['Marks_Obtained'])
                    if row['Marks_Obtained'] is not None else 0.0
                )

            return jsonify({
                "success": True,
                "attempts": rows
            }), 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                "success": False,
                "message": "Failed to load responses",
                "error": str(e)
            }), 500

    return view_responses_bp
