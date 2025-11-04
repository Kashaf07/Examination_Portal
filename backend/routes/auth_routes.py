from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import jwt
from functools import wraps

SECRET_KEY = "SecretKeyKYKI786"

def create_auth_routes(mysql):
    auth_bp = Blueprint('auth', __name__)
    
    # ---------- JWT TOKEN VERIFICATION DECORATOR ----------
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # Tokens are expected in Authorization header as: Bearer <token>
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_user = {
                    'email': data['email'],
                    'role': data['role']
                }
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expired! Please login again.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(current_user, *args, **kwargs)
        return decorated

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        cursor = mysql.connection.cursor()

        # Map of table name and email column for each role
        table_map = {
            "Admin": ("Mst_Admin", "Email", "Name"),
            "Faculty": ("Mst_Faculty", "F_Email", "F_Name"),
            "Student": ("Applicants", "Email", "Full_Name")
        }

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
                
                # ✅ Explicitly insert login time as NOW
                login_time = datetime.now()
                insert_log_query = """
                    INSERT INTO login_log (User_Email, Role, Login_Time)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_log_query, (email_from_db, role, login_time))
                mysql.connection.commit()
                
                # ✅ Generate JWT token (valid 2 hours)
                token = jwt.encode({
                    'email': email_from_db,
                    'role': role,
                    'exp': datetime.now(timezone.utc) + timedelta(hours=2)
                }, SECRET_KEY, algorithm="HS256")

                if role == "Student":
                    # Fetch student ID
                    cursor.execute("SELECT Applicant_Id FROM Applicants WHERE Email = %s", (email,))
                    student_row = cursor.fetchone()
                    student_id = student_row[0] if student_row else None

                    return jsonify({
                        'status': 'success',
                        'token': token,
                        'role': role,
                        'id': student_id,
                        'name': name_from_db,
                        'email': email_from_db,
                        'login_time': login_time.strftime('%Y-%m-%d %H:%M:%S')
                    }), 200

                return jsonify({
                    'status': 'success',
                    'token': token,
                    'role': role,
                    'name': name_from_db,
                    'email': email_from_db,
                    'login_time': login_time.strftime('%Y-%m-%d %H:%M:%S')
                }), 200

        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

    @auth_bp.route('/logout', methods=['POST'])
    def logout():
        data = request.json
        email = data.get('email')
        role = data.get('role')

        try:
            cursor = mysql.connection.cursor()
            # ✅ Update only latest login record for this user
            update_query = """
            UPDATE login_log
    SET Logout_Time = %s
    WHERE Log_ID = (
        SELECT Log_ID FROM (
            SELECT Log_ID
            FROM login_log
            WHERE User_Email = %s AND Role = %s
            ORDER BY Log_ID DESC
            LIMIT 1
        ) AS sub
    )
"""
            cursor.execute(update_query, (datetime.now(), email, role))
            mysql.connection.commit()
            return jsonify({'success': True, 'message': 'Logout time recorded'})
        except Exception as e:
            print("Error in logout route:", e)
            return jsonify({'success': False, 'message': 'Logout logging failed'}), 500
        
        # ---------- SAMPLE PROTECTED ROUTE ----------
    @auth_bp.route('/verify-token', methods=['GET'])
    @token_required
    def verify_token(current_user):
        return jsonify({
            'status': 'valid',
            'user': current_user
        }), 200

    return auth_bp