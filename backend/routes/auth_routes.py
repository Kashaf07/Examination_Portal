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
                    'role': data['active_role']
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
        cursor.execute("SELECT Name, Email, Password FROM mst_admin WHERE Email=%s", (email,))
        admin = cursor.fetchone()

        if admin:
            a_name, a_email, a_pass = admin
            roles.append("Admin")    # add role even if password doesn't match
            if a_pass == password:
                password_matched = True
                selected_role = "Admin"
                user_name = a_name

        # ---- CHECK STUDENT ----
        cursor.execute("SELECT Full_Name, Email, Password, Applicant_Id FROM applicants WHERE Email=%s", (email,))
        student = cursor.fetchone()

        if student:
            s_name, s_email, s_pass, sid = student
            roles.append("Student")
            if s_pass == password:
                password_matched = True
                selected_role = "Student"
                user_name = s_name
                student_id = sid

        # ===== NO PASSWORD MATCHED =====
        if not password_matched:
            return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

        # ===== LOGIN SUCCESS =====
        # Save login time
        login_time = datetime.now()
        cursor.execute("""
            INSERT INTO login_log (User_Email, Role, Login_Time)
            VALUES (%s, %s, %s)
        """, (email, selected_role, login_time))
        mysql.connection.commit()

        # Create JWT
        token = jwt.encode({
            "email": email,
            "roles": roles,
            "active_role": selected_role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        response = {
            "status": "success",
            "token": token,
            "roles": roles,
            "active_role": selected_role,
            "name": user_name,
            "email": email,
            "login_time": login_time.strftime("%Y-%m-%d %H:%M:%S")
        }

        if selected_role == "Student":
             response["applicant_id"] = student_id

        return jsonify(response), 200
        
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