def create_auth_routes(mysql):
    from flask import Blueprint, request, jsonify

    auth_routes = Blueprint('auth_routes', __name__)

    @auth_routes.route('/login', methods=['POST'])
    def faculty_login():
        data = request.json
        email = data.get("email")
        password = data.get("password")

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT Faculty_Id, F_Name FROM Mst_Faculty WHERE F_Email = %s AND Password = %s", (email, password))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return jsonify({"status": "success", "faculty_id": result[0], "name": result[1]})
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return auth_routes
