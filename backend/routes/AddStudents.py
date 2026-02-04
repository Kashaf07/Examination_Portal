from flask import Blueprint, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename


def create_add_students_bp(mysql):
    add_students_bp = Blueprint('add_students', __name__)
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # --------------------------------------------------
    # ADD SINGLE APPLICANT
    # --------------------------------------------------
    @add_students_bp.route('/applicants/add', methods=['POST'])
    def add_single_applicant():
        data = request.get_json()
        required = ['Full_Name', 'Email', 'Password', 'group_id']

        for field in required:
            if not data.get(field):
                return jsonify(
                    success=False,
                    message=f"{field.replace('_', ' ')} is required",
                    field=field
                ), 400

        cursor = mysql.connection.cursor()

        try:
            # ✅ DUPLICATE CHECK (EMAIL + GROUP)
            cursor.execute("""
                SELECT 1 FROM applicants
                WHERE Email = %s AND group_id = %s
            """, (data['Email'], data['group_id']))

            if cursor.fetchone():
                return jsonify(
                    success=False,
                    message="This email already exists in the selected group",
                    field="Email"
                ), 400

            # ✅ SAFE DOB HANDLING
            dob_value = data['DOB'] if data.get('DOB') else None

            cursor.execute("""
                INSERT INTO applicants
                (Full_Name, Email, Password, Phone, DOB, Gender, Address, group_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['Full_Name'],
                data['Email'],
                data['Password'],      # ⚠️ hash later
                data.get('Phone'),
                dob_value,              # ✅ FIXED
                data.get('Gender'),
                data.get('Address'),
                data['group_id']
            ))

            mysql.connection.commit()

            return jsonify(success=True, message="Applicant added successfully"), 201

        except Exception:
            mysql.connection.rollback()
            return jsonify(
                success=False,
                message="Invalid date of birth. Please select a valid date.",
                field="DOB"
            ), 400

        finally:
            cursor.close()

    # --------------------------------------------------
    # BULK UPLOAD
    # --------------------------------------------------
    @add_students_bp.route('/upload_students', methods=['POST'])
    def upload_students():
        if 'file' not in request.files:
            return jsonify(success=False, message='File missing'), 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify(success=False, message='Invalid file'), 400

        filename = secure_filename(file.filename)
        path = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(path)

        df = pd.read_excel(path) if filename.endswith('.xlsx') else pd.read_csv(path)
        df.columns = [c.strip() for c in df.columns]

        cursor = mysql.connection.cursor()
        success_count, failed_rows = 0, []

        for idx, row in df.iterrows():
            try:
                cursor.execute("""
                    SELECT 1 FROM applicants
                    WHERE Email = %s AND group_id = %s
                """, (row['Email'], int(row['group_id'])))

                if cursor.fetchone():
                    failed_rows.append({
                        "row": idx + 2,
                        "error": "Duplicate email in same group"
                    })
                    continue

                dob = None
                if pd.notnull(row['DOB']):
                    dob = pd.to_datetime(row['DOB']).strftime('%Y-%m-%d')

                cursor.execute("""
                    INSERT INTO applicants
                    (Full_Name, Email, Password, Phone, DOB, Gender, Address, group_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['Full_Name'],
                    row['Email'],
                    str(row['Password']),
                    row['Phone'],
                    dob,
                    row['Gender'],
                    row['Address'],
                    int(row['group_id'])
                ))

                success_count += 1

            except Exception as e:
                failed_rows.append({"row": idx + 2, "error": str(e)})

        mysql.connection.commit()
        cursor.close()

        return jsonify(
            success=True,
            inserted=success_count,
            failed=len(failed_rows),
            errors=failed_rows
        ), 200

    return add_students_bp
