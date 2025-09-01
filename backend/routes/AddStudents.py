from flask import Blueprint, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename

def create_add_students_bp(mysql):
    add_students_bp = Blueprint('add_students', __name__)
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @add_students_bp.route('/upload_students', methods=['POST'])
    def upload_students():
        file = request.files.get('file')
        exam_id = request.form.get('exam_id')
        uploaded_by = request.form.get('email')
        role = request.form.get('role')

        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid or missing file'}), 400

        try:
            filename = secure_filename(file.filename)
            upload_dir = os.path.join('uploads', 'students')
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = os.path.join(upload_dir, filename)
            file.save(upload_path)

            # Read file into DataFrame
            if filename.endswith('.csv'):
                df = pd.read_csv(upload_path)
            else:
                df = pd.read_excel(upload_path)

            required_columns = ['Full_Name', 'Email', 'Password', 'Phone', 'DOB', 'Gender', 'Address']
            if not all(col in df.columns for col in required_columns):
                return jsonify({'error': 'Missing required columns in uploaded file'}), 400

            cursor = mysql.connection.cursor()
            inserted, skipped = 0, 0
            error_rows = []

            for idx, row in df.iterrows():
                try:
                    # Try parsing DOB to correct MySQL format
                    dob = row['DOB']
                    # Try common formats and fallback
                    # If already in yyyy-mm-dd, leave it, else convert
                    try:
                        dob_converted = pd.to_datetime(dob, dayfirst=True).strftime('%Y-%m-%d')
                    except Exception:
                        dob_converted = dob  # Might raise error, caught below
                    cursor.execute("""
                        INSERT INTO applicants (Full_Name, Email, Password, Phone, DOB, Gender, Address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        row['Full_Name'],
                        row['Email'],
                        row['Password'],
                        row['Phone'],
                        dob_converted,
                        row['Gender'],
                        row['Address']
                    ))
                    inserted += 1
                except Exception as e:
                    skipped += 1
                    error_rows.append({
                        "row": int(idx),
                        "email": row.get("Email"),
                        "error": str(e)
                    })

            # Log the upload in file_uploads table
            cursor.execute("""
                INSERT INTO file_uploads (Uploaded_By, Role, File_Name, File_Path)
                VALUES (%s, %s, %s, %s)
            """, (uploaded_by, role, filename, upload_path))

            mysql.connection.commit()
            cursor.close()
            return jsonify({
                'message': 'Students uploaded and logged successfully',
                'inserted': inserted,
                'skipped': skipped,
                'errors': error_rows
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return add_students_bp
