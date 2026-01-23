from flask import Blueprint, request, jsonify
import pandas as pd
from datetime import datetime
import os
from werkzeug.utils import secure_filename


def create_add_students_bp(mysql):
    add_students_bp = Blueprint('add_students', __name__)
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # --------------------------------------------------
    # ADD SINGLE APPLICANT (MANUAL FORM)
    # --------------------------------------------------
    @add_students_bp.route('/applicants/add', methods=['POST'])
    def add_single_applicant():
        data = request.get_json()

        required = ['Full_Name', 'Email', 'Password', 'group_id']
        for field in required:
            if field not in data:
                return jsonify(success=False, message=f'{field} is required'), 400

        cursor = mysql.connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO applicants
                (Full_Name, Email, Password, Phone, DOB, Gender, Address, group_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['Full_Name'],
                data['Email'],
                data['Password'],          # ✅ PLAIN PASSWORD
                data.get('Phone'),
                data.get('DOB'),
                data.get('Gender'),
                data.get('Address'),
                data['group_id']
            ))

            mysql.connection.commit()

        except Exception as e:
            mysql.connection.rollback()
            return jsonify(success=False, message=str(e)), 500

        finally:
            cursor.close()

        return jsonify(success=True, message='Applicant added successfully'), 201

    # --------------------------------------------------
    # BULK UPLOAD APPLICANTS (EXCEL HAS group_id)
    # --------------------------------------------------
    @add_students_bp.route('/upload_students', methods=['POST'])
    def upload_students():
        if 'file' not in request.files:
            return jsonify(success=False, message='File missing'), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify(success=False, message='No file selected'), 400

        if not allowed_file(file.filename):
            return jsonify(success=False, message='Invalid file format'), 400

        filename = secure_filename(file.filename)
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, filename)
        file.save(path)

        try:
            df = pd.read_excel(path) if filename.endswith('.xlsx') else pd.read_csv(path)
        except Exception as e:
            return jsonify(success=False, message=f'Failed to read file: {str(e)}'), 400

        df.columns = [c.strip() for c in df.columns]

        required_columns = [
            'Full_Name', 'Email', 'Password',
            'Phone', 'DOB', 'Gender', 'Address', 'group_id'
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            return jsonify(success=False, message=f'Missing columns: {missing}'), 400

        cursor = mysql.connection.cursor()
        success_count = 0
        failed_rows = []

        for index, row in df.iterrows():
            try:
                dob_mysql = None
                if pd.notnull(row['DOB']):
                    dob_mysql = pd.to_datetime(row['DOB']).strftime('%Y-%m-%d')

                cursor.execute("""
                    INSERT INTO applicants
                    (Full_Name, Email, Password, Phone, DOB, Gender, Address, group_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['Full_Name'],
                    row['Email'],
                    str(row['Password']),   # ✅ PLAIN PASSWORD
                    row['Phone'],
                    dob_mysql,
                    row['Gender'],
                    row['Address'],
                    int(row['group_id'])
                ))

                success_count += 1

            except Exception as e:
                failed_rows.append({
                    'row': index + 2,
                    'error': str(e)
                })

        mysql.connection.commit()
        cursor.close()

        return jsonify(
            success=True,
            message='Applicants uploaded successfully',
            inserted=success_count,
            failed=len(failed_rows),
            errors=failed_rows
        ), 200

    return add_students_bp
