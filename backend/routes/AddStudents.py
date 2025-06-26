from flask import Blueprint, request, jsonify
import pandas as pd
import mysql.connector
import os
from werkzeug.utils import secure_filename

add_students_bp = Blueprint('add_students', __name__)

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_students_bp.route('/add_students', methods=['POST'])
def add_students():
    file = request.files.get('file')
    exam_id = request.form.get('exam_id')  # optional exam linkage

    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid or missing file'}), 400

    try:
        # Read Excel or CSV file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)


        required_columns = ['Full_Name', 'Email', 'Password', 'Phone', 'DOB', 'Gender', 'Address']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in uploaded file'}), 400
        
        

        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='manager',
            database='entrance_database'
        )
        cursor = connection.cursor()

        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO applicants (Full_Name, Email, Password, Phone, DOB, Gender, Address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['Full_Name'],
                    row['Email'],
                    row['Password'],
                    row['Phone'],
                    row['DOB'],
                    row['Gender'],
                    row['Address']
                ))

                # OPTIONAL: Insert into exam_applicants/exam_student mapping table
                # if exam_id:
                #     applicant_id = cursor.lastrowid
                #     cursor.execute("INSERT INTO exam_applicants (exam_id, applicant_id) VALUES (%s, %s)", (exam_id, applicant_id))

            except mysql.connector.errors.IntegrityError:
                continue  # Skip duplicate emails

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Students uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@add_students_bp.route('/upload_students', methods=['POST'])
def upload_students():
    file = request.files.get('file')
    exam_id = request.form.get('exam_id')
    uploaded_by = request.form.get('email')
    role = request.form.get('role')

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join('uploads/students', filename)

    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    file.save(upload_path)

    # TODO: Process student data from Excel/CSV and insert into DB here...

    # 🔄 Insert into file_uploads
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO file_uploads (Uploaded_By, Role, File_Name, File_Path)
        VALUES (%s, %s, %s, %s)
    """, (uploaded_by, role, filename, upload_path))
    mysql.connection.commit()

    return jsonify({'message': 'Students uploaded and logged successfully'}), 200

