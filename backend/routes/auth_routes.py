from flask import Blueprint, request, jsonify

def create_auth_routes(mysql):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        cursor = mysql.connection.cursor()
        table_map = {
            "Admin": ("Mst_Admin", "Email"),
            "Faculty": ("Mst_Faculty", "F_Email"),
            "Student": ("Mst_Student", "S_Email")
        }

        table, email_col = table_map.get(role)
        if not table:
            return jsonify({"error": "Invalid role"}), 400

        query = f"SELECT * FROM {table} WHERE {email_col}=%s AND Password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            return jsonify({"status": "success", "role": role}), 200
        return jsonify({"status": "fail"}), 401

    return auth_bp
