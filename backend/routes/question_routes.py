import csv
import io
from flask import Blueprint, request, jsonify

def create_question_routes(mysql):
    question_bp = Blueprint('questions', __name__)

    @question_bp.route('/add', methods=['POST'])
    def add_question():
        data = request.json
        conn = mysql.connection
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO entrance_question_bank
            (Exam_Id, Question_Type, Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer, Marks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                data['exam_id'],
                data['question_type'],
                data['question_text'],
                data.get('option_a'),
                data.get('option_b'),
                data.get('option_c'),
                data.get('option_d'),
                data['correct_answer'],
                data.get('marks', 1)
            ))

            conn.commit()
            return jsonify({'message': 'Question added successfully'}), 201

        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            
            
    @question_bp.route('/upload-csv', methods=['POST'])
    def upload_csv():
        if 'file' not in request.files:
            return jsonify({'error': 'CSV file is required'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        exam_id = request.form.get('exam_id')
        if not exam_id:
            return jsonify({'error': 'Missing exam_id in form data'}), 400

        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)

        conn = mysql.connection
        cursor = conn.cursor()

        try:
            header = next(csv_input)
            for row in csv_input:
                if not row or all(cell.strip() == "" for cell in row):
                    continue  # skip empty rows

                if len(row) < 7:
                    return jsonify({'error': f'Invalid row: {row}. Expected at least 7 columns.'}), 400

                question_type, question_text, option_a, option_b, option_c, option_d, correct_answer, *rest = row
                marks = rest[0] if rest else 1  # default marks to 1
                
                try:
                    marks = int(marks)
                except ValueError:
                    return jsonify({'error': f'Invalid marks value: {marks}. Must be an integer.'}), 400

                
                cursor.execute("""
                    INSERT INTO entrance_question_bank 
                    (Exam_Id, Question_Type, Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer, Marks)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (exam_id, question_type, question_text, option_a, option_b, option_c, option_d, correct_answer, marks))

            conn.commit()
            return jsonify({'message': 'Questions uploaded successfully'}), 201

        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            
    @question_bp.route('/exams', methods=['GET'])
    def get_exams():
        conn = mysql.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT Exam_Id, Exam_Name FROM Entrance_Exam")
            exams = cursor.fetchall()
            exam_list = [{'Exam_Id': e[0], 'Exam_Name': e[1]} for e in exams]
            return jsonify(exam_list), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()


    return question_bp
