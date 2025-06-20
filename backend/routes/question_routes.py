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
            
    @question_bp.route('/questions/bank/<int:exam_id>', methods=['GET'])
    def get_question_bank(exam_id):
        conn = mysql.connection
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM entrance_question_bank WHERE Exam_Id = %s", (exam_id,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]
            return jsonify(results), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()


    @question_bp.route('/questions/paper/<int:exam_id>', methods=['GET'])
    def get_exam_paper_questions(exam_id):
        conn = mysql.connection
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT q.*
                FROM entrance_question_bank q
                JOIN exam_paper_questions epq ON q.Question_Id = epq.Question_Id
                JOIN exam_paper ep ON epq.Exam_Paper_Id = ep.Exam_Paper_Id
                WHERE ep.Exam_Id = %s
            """, (exam_id,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]
            return jsonify(results), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()


    @question_bp.route('/questions/paper/add', methods=['POST'])
    def add_question_to_paper():
        data = request.json
        exam_paper_id = data['exam_paper_id']
        question_id = data['question_id']

        conn = mysql.connection
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO exam_paper_questions (Exam_Paper_Id, Question_Id)
                VALUES (%s, %s)
            """, (exam_paper_id, question_id))
            conn.commit()
            return jsonify({'message': 'Question added to paper'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()


    @question_bp.route('/questions/paper/delete', methods=['POST'])
    def delete_question_from_paper():
        data = request.json
        exam_paper_id = data['exam_paper_id']
        question_id = data['question_id']

        conn = mysql.connection
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM exam_paper_questions
                WHERE Exam_Paper_Id = %s AND Question_Id = %s
            """, (exam_paper_id, question_id))
            conn.commit()
            return jsonify({'message': 'Question removed from paper'}), 200
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()


    @question_bp.route('/questions/paper/randomize/<int:exam_id>', methods=['POST'])
    def randomize_questions_for_paper(exam_id):
        data = request.json
        limit = data.get('limit', 10)

        conn = mysql.connection
        cursor = conn.cursor()
        try:
            # Get the paper ID for the exam
            cursor.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s", (exam_id,))
            paper = cursor.fetchone()
            if not paper:
                return jsonify({'error': 'No paper found for this exam'}), 404
            paper_id = paper[0]

            # Get N random questions from bank
            cursor.execute("""
                SELECT Question_Id FROM entrance_question_bank
                WHERE Exam_Id = %s
                ORDER BY RAND()
                LIMIT %s
            """, (exam_id, limit))
            questions = cursor.fetchall()

            for q in questions:
                cursor.execute("""
                    INSERT IGNORE INTO exam_paper_questions (Exam_Paper_Id, Question_Id)
                    VALUES (%s, %s)
                """, (paper_id, q[0]))

            conn.commit()
            return jsonify({'message': f'{len(questions)} questions randomized and added'}), 200
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            
            
    @question_bp.route('/questions/<int:exam_id>', methods=['GET'])
    def get_questions_by_exam(exam_id):
        conn = mysql.connection
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT Question_Id, Question_Text, Marks
                FROM entrance_question_bank
                WHERE Exam_Id = %s
            """, (exam_id,))
            result = cursor.fetchall()

            questions = [
                {
                    'question_id': row[0],
                    'text': row[1],
                    'marks': row[2]
                } for row in result
            ]

            return jsonify(questions), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()

    return question_bp
