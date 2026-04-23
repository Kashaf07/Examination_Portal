from arrow import now
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
                    'role': data['active_role'],
                    'user_id': data.get('user_id')
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

        cursor = mysql.connection.cursor()

        roles = []
        user_name = None
        student_id = None
        selected_role = None
        password_matched = False

        # ---- CHECK FACULTY ----
        cursor.execute("SELECT F_Name, F_Email, Password, Is_Active FROM mst_faculty WHERE F_Email=%s",(email,))
        faculty = cursor.fetchone()

        if faculty:
            f_name, f_email, f_pass, is_active = faculty
            roles.append("Faculty")

            # 🚫 Faculty exists but is DISABLED
            if is_active == 0:
                return jsonify({
                    "status": "fail",
                    "message": "Your faculty account is disabled. Please contact the administrator."
                }), 403

            # ✅ Faculty is active → check password
            if f_pass == password:
                password_matched = True
                selected_role = "Faculty"
                user_name = f_name


        # ---- CHECK ADMIN ----
        cursor.execute("SELECT Name, Email, Password, Is_Active FROM mst_admin WHERE Email=%s", (email,))
        admin = cursor.fetchone()

        if admin:
            a_name, a_email, a_pass, is_active = admin
            roles.append("Admin")

            # 🚫 Admin exists but is DISABLED
            if is_active == 0:
                return jsonify({
                    "status": "fail",
                    "message": "Your admin account is disabled. Please contact the system administrator."
                }), 403

            # ✅ Admin active → check password
            if a_pass == password:
                password_matched = True
                selected_role = "Admin"
                user_name = a_name

        # ---- CHECK STUDENT ----
        cursor.execute("""
            SELECT Full_Name, Email, Password, Applicant_Id, Is_Active
            FROM applicants
            WHERE Email=%s
        """, (email,))
        student = cursor.fetchone()

        if student:
            s_name, s_email, s_pass, sid, is_active = student
            roles.append("Student")

            # 🚫 Student exists but is DISABLED
            if is_active == 0:
                return jsonify({
                    "status": "fail",
                    "message": "Your student account is disabled. Please contact the administrator."
                }), 403

            # ✅ Student active → check password
            if s_pass == password:
                password_matched = True
                selected_role = "Student"
                user_name = s_name
                student_id = sid

        # ===== NO PASSWORD MATCHED =====
        if not password_matched:
            return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

        # Determine User_Id properly
        user_id = None

        if selected_role == "Student":
            user_id = student_id

        elif selected_role == "Faculty":
            cursor.execute("SELECT Faculty_Id FROM mst_faculty WHERE F_Email=%s", (email,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]

        elif selected_role == "Admin":
            cursor.execute("SELECT Admin_Id FROM mst_admin WHERE Email=%s", (email,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]

        # Insert into login_log with User_Id
        cursor.execute("""
            INSERT INTO login_log (User_Email, User_Id, Role, Login_Time)
            VALUES (%s, %s, %s, CONVERT_TZ(NOW(), '+00:00', '+05:30'))
        """, (email, user_id, selected_role))

        mysql.connection.commit()

        # Create JWT
        token = jwt.encode({
            "email": email,
            "user_id": user_id,
            "roles": roles,
            "active_role": selected_role,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=1)
        }, SECRET_KEY, algorithm="HS256")

        response = {
            "status": "success",
            "token": token,
            "roles": roles,
            "active_role": selected_role,
            "name": user_name,
            "email": email,
        }

        if selected_role == "Student":
             response["applicant_id"] = student_id

        return jsonify(response), 200
            
    @auth_bp.route('/logout', methods=['POST'])
    @token_required
    def logout(current_user):

        try:
            user_id = current_user.get("user_id")
            role = current_user.get("role")

            if not user_id or not role:
                return jsonify({'success': False, 'message': 'Invalid user data'}), 400

            cursor = mysql.connection.cursor()

            cursor.execute("""
                UPDATE login_log
                SET Logout_Time = %s
                WHERE Log_ID = (
                    SELECT Log_ID FROM (
                        SELECT Log_ID
                        FROM login_log
                        WHERE User_Id = %s
                        AND Role = %s
                        AND Logout_Time IS NULL
                        ORDER BY Log_ID DESC
                        LIMIT 1
                    ) AS sub
                )
            """, (datetime.now(), user_id, role))

            mysql.connection.commit()
            cursor.close()

            return jsonify({'success': True, 'message': 'Logout time recorded'})

        except Exception as e:
            print("Logout error:", e)
            return jsonify({'success': False, 'message': 'Logout failed'}), 500 
    @auth_bp.route('/verify-token', methods=['GET'])
    @token_required
    def verify_token(current_user):
        return jsonify({
            'status': 'valid',
            'user': current_user
        }), 200

    return auth_bp