from flask import Blueprint, request, jsonify
from datetime import datetime

def create_exam_routes(mysql):
    exam_bp = Blueprint('exam', __name__)

    @exam_bp.route('/create', methods=['POST'])
    def create_exam():
        data = request.json
        exam_name = data.get('exam_name')
        exam_date = data.get('exam_date')      # format: YYYY-MM-DD
        exam_time = data.get('exam_time')      # format: HH:MM
        duration = data.get('duration')        # integer
        total_questions = data.get('total_questions')
        max_marks = data.get('max_marks')
        faculty_email = data.get('faculty_email')

        # Validate required fields
        if not all([exam_name, exam_date, exam_time, duration, total_questions, max_marks, faculty_email]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        try:
            # Combine exam date and time to check if it's in the past
            exam_datetime_str = f"{exam_date} {exam_time}"
            exam_datetime = datetime.strptime(exam_datetime_str, "%Y-%m-%d %H:%M")
            current_datetime = datetime.now()

            if exam_datetime < current_datetime:
                return jsonify({'success': False, 'message': 'Exam date/time cannot be in the past'}), 400

            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO Entrance_Exam 
                (Exam_Name, Exam_Date, Exam_Time, Duration_Minutes, Total_Questions, Max_Marks, Faculty_Email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (exam_name, exam_date, exam_time, duration, total_questions, max_marks, faculty_email))
            mysql.connection.commit()

            exam_id = cursor.lastrowid  # Get the auto-incremented ID
            cursor.close()

            return jsonify({
                'success': True,
                'message': f'Exam created successfully with ID: {exam_id}',
                'exam_id': exam_id
            })

        except Exception as e:
            print("DB error:", e)
            return jsonify({'success': False, 'message': 'Database error'}), 500

    @exam_bp.route('/get_exams/<faculty_email>', methods=['GET'])
    def get_exams(faculty_email):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time, Duration_Minutes,
                       Total_Questions, Max_Marks
                FROM Entrance_Exam
                WHERE Faculty_Email = %s
            """, (faculty_email,))
            exams = cursor.fetchall()
            cursor.close()

            exam_list = []
            for row in exams:
                exam_list.append({
                    'Exam_Id': row[0],
                    'Exam_Name': row[1],
                    'Exam_Date': str(row[2]),
                    'Exam_Time': str(row[3]),
                    'Duration_Minutes': row[4],
                    'Total_Questions': row[5],
                    'Max_Marks': row[6]
                })

            return jsonify({'success': True, 'exams': exam_list})
        except Exception as e:
            print("Error fetching exams:", e)
            return jsonify({'success': False, 'message': 'Server error'}), 500

    return exam_bp
