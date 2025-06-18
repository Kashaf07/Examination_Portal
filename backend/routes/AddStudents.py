from flask import Blueprint, request, jsonify
import pandas as pd
import mysql.connector
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
            password='your_db_password',
            database='your_db_name'
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
