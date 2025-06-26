from flask import Blueprint, jsonify

def create_admin_routes(mysql):
    admin_bp = Blueprint('admin_routes', __name__)

    @admin_bp.route('/uploaded-files', methods=['GET'])
    def view_uploaded_files():
        try:
            cursor = mysql.connection.cursor()
            query = """
                SELECT File_ID, Uploaded_By, Role, File_Name, File_Path, Upload_Date 
                FROM file_uploads 
                ORDER BY Upload_Date DESC
            """
            cursor.execute(query)
            files = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in files]
            cursor.close()
            return jsonify(result), 200
        except Exception as e:
            print("Admin file view error:", e)
            return jsonify({"error": "Unable to fetch files"}), 500

    return admin_bp
