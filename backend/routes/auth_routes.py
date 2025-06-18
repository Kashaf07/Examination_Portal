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

        # Map of table name and email column for each role
        table_map = {
            "Admin": ("Mst_Admin", "Email", "Name"),     # assuming Name column for Admin
            "Faculty": ("Mst_Faculty", "F_Email", "F_Name"),
            "Student": ("Applicants", "Email", "Full_Name")  # assuming Full_Name column for Student
        }

        # Role validation
        if role not in table_map:
            return jsonify({"error": "Invalid role"}), 400

        table, email_col, name_col = table_map[role]

        # Query the table for the given role
        query = f"SELECT {name_col}, {email_col}, Password FROM {table} WHERE {email_col}=%s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            name_from_db, email_from_db, password_from_db = result
            if password_from_db == password:
                return jsonify({
                    'status': 'success',
                    'role': role,
                    'name': name_from_db,
                    'email': email_from_db
                }), 200

        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

    # Additional endpoint to get faculty name by email
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
