from flask import Blueprint, request, jsonify
from MySQLdb.cursors import DictCursor

def create_exam_result_routes(mysql):
    exam_result_bp = Blueprint('exam_result', __name__)

    @exam_result_bp.route('/exam/<int:exam_id>/results', methods=['GET'])
    def get_exam_results(exam_id):
        email = request.args.get('email')
        role = request.args.get('role')

        if not email or not role:
            return jsonify(success=False, message="Unauthorized"), 403

        try:
            cursor = mysql.connection.cursor(DictCursor)

            # 🔐 ROLE CHECK (Basic Example)
            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            query = """
                SELECT 
                    a.Attempt_Id,
                    a.Applicant_Id,
                    a.Student_Email,
                    a.Marks_Obtained,
                    a.Max_Marks,
                    a.Status
                FROM Trn_Attempts a
                WHERE a.Exam_Id = %s
                ORDER BY a.Marks_Obtained DESC
            """

            cursor.execute(query, (exam_id,))
            results = cursor.fetchall()

            return jsonify(success=True, results=results)

        except Exception as e:
            return jsonify(success=False, message=str(e)), 500

    return exam_result_bp