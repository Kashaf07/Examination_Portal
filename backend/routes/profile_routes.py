from flask import Blueprint, request, jsonify, send_from_directory
import os
import jwt
from werkzeug.utils import secure_filename

SECRET_KEY = "SecretKeyKYKI786"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'profile_pics')

def get_current_user(req):
    auth = req.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ', 1)[1]
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            'email': data.get('email'),
            'role': data.get('active_role'),
            'user_id': data.get('user_id')
        }
    except Exception as e:
        print("Token decode error:", e)
        return None

def create_profile_routes(mysql):
    profile_bp = Blueprint('profile_routes', __name__)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @profile_bp.route('/upload-pic', methods=['POST', 'OPTIONS'])
    def upload_profile_pic():
        if request.method == 'OPTIONS':
            return '', 204

        try:
            current_user = get_current_user(request)
            if not current_user:
                print("upload-pic: Unauthorized - no valid token")
                return jsonify({'error': 'Unauthorized'}), 401

            email = current_user.get('email')
            role = current_user.get('role')
            print(f"upload-pic: user={email}, role={role}")

            if 'profile_pic' not in request.files:
                print("upload-pic: no file in request.files, keys:", list(request.files.keys()))
                return jsonify({'error': 'No file provided'}), 400

            file = request.files['profile_pic']
            filename = file.filename or 'profile.jpg'
            content_type = file.content_type or ''
            print(f"upload-pic: filename={filename}, content_type={content_type}")

            # Build safe filename from email
            safe_base = email.replace('@', '_at_').replace('.', '_').replace('+', '_')
            ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
            if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                return jsonify({'error': 'Only JPG, PNG, or WEBP images are allowed'}), 400
            safe_name = secure_filename(safe_base) + '.' + ext
            save_path = os.path.join(UPLOAD_FOLDER, safe_name)

            file.save(save_path)
            print(f"upload-pic: file saved to {save_path}")

            relative_path = f'profile_pics/{safe_name}'

            cursor = mysql.connection.cursor()
            if role == 'Admin':
                cursor.execute(
                    "UPDATE mst_admin SET Profile_Pic = %s WHERE Email = %s",
                    (relative_path, email)
                )
                print(f"upload-pic: updated mst_admin rows={cursor.rowcount}")
            elif role == 'Faculty':
                cursor.execute(
                    "UPDATE mst_faculty SET Profile_Pic = %s WHERE F_Email = %s",
                    (relative_path, email)
                )
                print(f"upload-pic: updated mst_faculty rows={cursor.rowcount}")
            else:
                cursor.close()
                return jsonify({'error': f'Role not supported: {role}'}), 400

            mysql.connection.commit()
            cursor.close()

            return jsonify({'success': True, 'profile_pic': relative_path}), 200

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print("upload-pic EXCEPTION:\n", tb)
            return jsonify({'error': str(e), 'traceback': tb}), 500

    @profile_bp.route('/get-pic', methods=['GET'])
    def get_profile_pic():
        current_user = get_current_user(request)

        # Fallback: accept email + role as query params (for when token is expired)
        if not current_user:
            email = request.args.get('email')
            role = request.args.get('role')
            if not email or not role:
                return jsonify({'profile_pic': None}), 200
        else:
            email = current_user.get('email')
            role = current_user.get('role')

        try:
            cursor = mysql.connection.cursor()
            if role == 'Admin':
                cursor.execute("SELECT Profile_Pic FROM mst_admin WHERE Email = %s", (email,))
            elif role == 'Faculty':
                cursor.execute("SELECT Profile_Pic FROM mst_faculty WHERE F_Email = %s", (email,))
            else:
                return jsonify({'profile_pic': None}), 200

            row = cursor.fetchone()
            cursor.close()
            pic = row[0] if row else None
            return jsonify({'profile_pic': pic}), 200
        except Exception as e:
            print("get-pic DB error:", e)
            return jsonify({'profile_pic': None}), 200

    @profile_bp.route('/pic-file/<path:filename>', methods=['GET'])
    def serve_profile_pic(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    @profile_bp.route('/delete-pic', methods=['DELETE', 'OPTIONS'])
    def delete_profile_pic():
        if request.method == 'OPTIONS':
            return '', 204

        current_user = get_current_user(request)
        if not current_user:
            return jsonify({'error': 'Unauthorized'}), 401

        email = current_user.get('email')
        role = current_user.get('role')

        try:
            cursor = mysql.connection.cursor()
            if role == 'Admin':
                cursor.execute("SELECT Profile_Pic FROM mst_admin WHERE Email = %s", (email,))
            elif role == 'Faculty':
                cursor.execute("SELECT Profile_Pic FROM mst_faculty WHERE F_Email = %s", (email,))
            else:
                return jsonify({'error': 'Role not supported'}), 400

            row = cursor.fetchone()
            if row and row[0]:
                # Delete file from disk
                file_path = os.path.join(os.path.dirname(UPLOAD_FOLDER), row[0])
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Clear from DB
            if role == 'Admin':
                cursor.execute("UPDATE mst_admin SET Profile_Pic = NULL WHERE Email = %s", (email,))
            elif role == 'Faculty':
                cursor.execute("UPDATE mst_faculty SET Profile_Pic = NULL WHERE F_Email = %s", (email,))

            mysql.connection.commit()
            cursor.close()
            return jsonify({'success': True}), 200
        except Exception as e:
            print("delete-pic error:", e)
            return jsonify({'error': str(e)}), 500

    return profile_bp
