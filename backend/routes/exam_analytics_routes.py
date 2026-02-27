from flask import Blueprint, request, jsonify
from MySQLdb.cursors import DictCursor

def create_exam_analytics_routes(mysql):
    exam_analytics_bp = Blueprint('exam_analytics', __name__)

    def is_authorized(cursor, exam_id, email, role):
        if role == 'Admin':
            cursor.execute("SELECT 1 FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
        else:
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s AND Faculty_Email = %s",
                (exam_id, email)
            )
        return cursor.fetchone() is not None

    # ── GET GROUPS FOR THIS EXAM ───────────────────────────────────────────
    @exam_analytics_bp.route('/api/analytics/<int:exam_id>/groups', methods=['GET'])
    def get_exam_groups(exam_id):
        email = request.args.get('email')
        role  = request.args.get('role')

        if not email or not role:
            return jsonify(success=False, message="Unauthorized"), 403

        try:
            cursor = mysql.connection.cursor(DictCursor)

            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            if not is_authorized(cursor, exam_id, email, role):
                return jsonify(success=False, message="Unauthorized"), 403

            # Groups that have at least one applicant assigned to this exam
            cursor.execute("""
                SELECT DISTINCT
                    ag.group_id   AS Group_Id,
                    ag.group_name AS Group_Name
                FROM applicant_groups ag
                JOIN applicants a ON a.group_id = ag.group_id
                JOIN applicant_exam_assign aea ON aea.Applicant_Id = a.Applicant_Id
                WHERE aea.Exam_Id = %s
                  AND ag.group_name != '__UNASSIGNED__'
                ORDER BY ag.group_name
            """, (exam_id,))

            groups = cursor.fetchall()
            cursor.close()
            return jsonify(success=True, groups=groups)

        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify(success=False, message=str(e)), 500

    return exam_analytics_bp