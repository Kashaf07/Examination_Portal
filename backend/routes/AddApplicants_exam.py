from flask import Blueprint, jsonify

def create_add_applicants_exam_bp(mysql):
    add_applicants_exam_bp = Blueprint('add_applicants_exam', __name__)

    @add_applicants_exam_bp.route('/applicants', methods=['GET'])
    def get_applicants():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM applicants")
            rows = cursor.fetchall()

            # Get column names
            column_names = [i[0] for i in cursor.description]

            # Convert to list of dicts
            applicants = [dict(zip(column_names, row)) for row in rows]

            return jsonify({'success': True, 'applicants': applicants})
        except Exception as e:
            print("Error loading applicants:", str(e))
            return jsonify({'success': False, 'message': 'Error loading applicants'})

    return add_applicants_exam_bp
