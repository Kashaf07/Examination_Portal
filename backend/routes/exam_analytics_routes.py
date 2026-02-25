from flask import Blueprint, request, jsonify
from MySQLdb.cursors import DictCursor

def create_exam_analytics_routes(mysql):
    exam_analytics_bp = Blueprint('exam_analytics', __name__)

    @exam_analytics_bp.route('/exam/<int:exam_id>/analytics', methods=['GET'])
    def get_exam_analytics(exam_id):
        email = request.args.get('email')
        role = request.args.get('role')

        if not email or not role:
            return jsonify(success=False, message="Unauthorized"), 403

        try:
            cursor = mysql.connection.cursor(DictCursor)

            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            # 🔹 Total Attempts
            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM Trn_Attempts
                WHERE Exam_Id = %s
            """, (exam_id,))
            total = cursor.fetchone()['total']

            # 🔹 Pass Count
            cursor.execute("""
                SELECT COUNT(*) AS pass_count
                FROM Trn_Attempts
                WHERE Exam_Id = %s AND Status = 'Pass'
            """, (exam_id,))
            pass_count = cursor.fetchone()['pass_count']

            # 🔹 Fail Count
            cursor.execute("""
                SELECT COUNT(*) AS fail_count
                FROM Trn_Attempts
                WHERE Exam_Id = %s AND Status = 'Fail'
            """, (exam_id,))
            fail_count = cursor.fetchone()['fail_count']

            # 🔹 Average Marks
            cursor.execute("""
                SELECT AVG(Marks_Obtained) AS avg_marks
                FROM Trn_Attempts
                WHERE Exam_Id = %s
            """, (exam_id,))
            avg_marks = cursor.fetchone()['avg_marks']

            return jsonify(success=True, analytics={
                "total": total,
                "pass": pass_count,
                "fail": fail_count,
                "average": round(avg_marks, 2) if avg_marks else 0
            })

        except Exception as e:
            return jsonify(success=False, message=str(e)), 500

    return exam_analytics_bp