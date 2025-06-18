from flask import Blueprint, request, jsonify

def create_auth_routes(mysql):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/login', methods=['POST'])
    def faculty_login():
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        cursor = mysql.connection.cursor()

        if role == "Faculty":
            cursor.execute("SELECT F_Name, Password FROM mst_faculty WHERE F_Email = %s", (email,))
            result = cursor.fetchone()
            if result and result[1] == password:
                return jsonify({
                    'status': 'success',
                    'name': result[0],
                    'email': email
                })

        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

    # ✅ Move this inside the function
    @auth_bp.route('/faculty-name/<email>', methods=['GET'])
    def get_faculty_name(email):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT F_Name FROM mst_faculty WHERE F_Email = %s", (email,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return jsonify({"success": True, "name": row[0]})
            return jsonify({"success": False, "message": "Faculty not found"}), 404
        except Exception as e:
            print("Error in get_faculty_name:", e)
            return jsonify({"success": False, "message": "Server error"}), 500

    return auth_bp
