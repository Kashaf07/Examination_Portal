from flask import Blueprint, request, jsonify

def create_faculty_routes(mysql):
    faculty_bp = Blueprint('faculty_bp', __name__)

    @faculty_bp.route('/api/faculty/profile', methods=['GET'])
    def get_faculty_profile():
        email = request.args.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT F_Name FROM Mst_Faculty WHERE F_Email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return jsonify({'status': 'success', 'name': result[0]}), 200
            else:
                return jsonify({'status': 'fail', 'error': 'Faculty not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'error': str(e)}), 500
        finally:
            cursor.close()

    return faculty_bp
