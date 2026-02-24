import io
import os
import csv
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

def create_question_routes(mysql):
    question_bp = Blueprint('questions', __name__)
    def is_exam_authorized(cursor, exam_id, email, role):
        if role == "Admin":
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s",
                (exam_id,)
            )
        else:
            cursor.execute(
                """
                SELECT 1
                FROM entrance_exam
                WHERE Exam_Id = %s
                AND Faculty_Email = %s
                """,
                (exam_id, email)
            )

        return cursor.fetchone() is not None

    @question_bp.route('/add', methods=['POST'])
    def add_question():
        data = request.json
        exam_id = data.get("exam_id")
        email = data.get("email")
        role = data.get("role")
        
        conn = mysql.connection
        cursor = conn.cursor()

        if not exam_id or not email or not role:
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400      
        # 🔐 AUTHORIZATION CHECK
        if not is_exam_authorized(cursor, exam_id, email, role):
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Unauthorized Access"
            }), 403

        # Validation for MCQ - correct answer must be present in options
        if data['question_type'] == 'MCQ':
            correct = str(data.get('correct_answer', '')).strip()
            options = [
                str(data.get('option_a', '')).strip(),
                str(data.get('option_b', '')).strip(),
                str(data.get('option_c', '')).strip(),
                str(data.get('option_d', '')).strip(),
            ]
            if correct not in options:
                cursor.close()
                return jsonify({'error': 'Correct answer must be one of the MCQ options.'}), 400

        # General validation for missing correct answer
        if not str(data.get('correct_answer', '')).strip():
            cursor.close()
            return jsonify({'error': 'Please enter the correct answer for this question.'}), 400

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
        file = request.files.get('file')
        exam_id = request.form.get('exam_id')
        uploaded_by = request.form.get('email')
        role = request.form.get('role')

        if not file or file.filename == '':
            return jsonify({'error': 'CSV file is required'}), 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join('uploads/question_banks', filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)

        # Read contents BEFORE saving
        content = file.read().decode("UTF8")
        file.stream.seek(0)
        file.save(upload_path)

        # Log upload
        cursor = mysql.connection.cursor()
        
        if not is_exam_authorized(cursor, exam_id, uploaded_by, role):
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Unauthorized Access"
            }), 403
            
        cursor.execute("""
            INSERT INTO file_uploads (Uploaded_By, Role, File_Name, File_Path)
            VALUES (%s, %s, %s, %s)
        """, (uploaded_by, role, filename, upload_path))
        mysql.connection.commit()

        stream = io.StringIO(content, newline=None)
        csv_input = csv.reader(stream)

        conn = mysql.connection
        cursor = conn.cursor()

        rows_to_insert = []
        errors = []

        try:
            header = next(csv_input)
            for i, row in enumerate(csv_input, start=2):  # start=2 to account for header line
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                if len(row) < 7:
                    errors.append(f'Row {i}: Expected at least 7 columns.')
                    continue

                question_type, question_text, option_a, option_b, option_c, option_d, correct_answer, *rest = row

                if not str(correct_answer).strip():
                    errors.append(f'Row {i}: Please enter the correct answer for this question.')
                    continue

                marks = rest[0] if rest else 1
                try:
                    marks = int(marks)
                except ValueError:
                    errors.append(f'Row {i}: Invalid marks value ({marks}). Must be an integer.')
                    continue

                # MCQ check
                if question_type.strip() == 'MCQ':
                    candidate_options = [
                        str(option_a).strip(),
                        str(option_b).strip(),
                        str(option_c).strip(),
                        str(option_d).strip(),
                    ]
                    if str(correct_answer).strip() not in candidate_options:
                        errors.append(f'Row {i}: MCQ correct answer must match an option.')
                        continue

                rows_to_insert.append((exam_id, question_type, question_text, option_a, option_b, option_c, option_d, correct_answer, marks))

            if errors:
                # Do not insert anything if errors
                return jsonify({'error': 'CSV validation failed.', 'details': errors}), 400

            for row in rows_to_insert:
                cursor.execute("""
                    INSERT INTO entrance_question_bank 
                    (Exam_Id, Question_Type, Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer, Marks)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, row)

            conn.commit()
            return jsonify({'message': 'Question Bank uploaded and logged successfully'}), 200

        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

    @question_bp.route('/exams', methods=['GET'])
    def get_exams():
        email = request.args.get("email")
        role = request.args.get("role")

        conn = mysql.connection
        cursor = conn.cursor()

        try:
            if role == "Admin":
                cursor.execute("SELECT Exam_Id, Exam_Name FROM entrance_exam")
            else:
                cursor.execute("""
                    SELECT Exam_Id, Exam_Name
                    FROM entrance_exam
                    WHERE Faculty_Email = %s
                """, (email,))

            exams = cursor.fetchall()

            exam_list = [
                {'Exam_Id': e[0], 'Exam_Name': e[1]}
                for e in exams
            ]

            return jsonify(success=True, exams=exam_list), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()
    @question_bp.route('/questions/bank/<int:exam_id>', methods=['GET'])
    def get_question_bank(exam_id):
        email = request.args.get("email")
        role = request.args.get("role")
        conn = mysql.connection
        cursor = conn.cursor()
        
        if not is_exam_authorized(cursor, exam_id, email, role):
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Unauthorized Access"
            }), 403 
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

    @question_bp.route('/questionbank/all/<int:exam_id>', methods=['GET'])
    def get_all_questions_for_exam(exam_id):
        email = request.args.get("email")
        role = request.args.get("role")
        conn = mysql.connection
        cursor = conn.cursor()
        
        if not is_exam_authorized(cursor, exam_id, email, role):
            return jsonify({
                "success": False,
                "message": "Unauthorized Access"
            }), 403
        try:
            cursor.execute("""
                SELECT Question_Id, Question_Text, Marks 
                FROM entrance_question_bank 
                WHERE Exam_Id = %s
            """, (exam_id,))
            rows = cursor.fetchall()
            questions = [{'Question_Id': row[0], 'Question_Text': row[1], 'Marks': row[2]} for row in rows]
            return jsonify(questions), 200        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

    @question_bp.route('/paper/<int:exam_id>', methods=['GET'])
    def get_exam_paper_questions(exam_id):
        email = request.args.get("email")
        role = request.args.get("role")

        if not email or not role:
            return jsonify({
                "success": False,
                "message": "Missing authentication details"
            }), 400

        conn = mysql.connection
        cursor = conn.cursor()

        try:
            # 🔐 Authorization Check
            if not is_exam_authorized(cursor, exam_id, email, role):
                return jsonify({
                    "success": False,
                    "message": "Unauthorized Access"
                }), 403

            # ✅ Fetch Paper Questions
            cursor.execute("""
                SELECT q.*
                FROM entrance_question_bank q
                JOIN exam_paper_questions epq 
                    ON q.Question_Id = epq.Question_Id
                JOIN exam_paper ep 
                    ON epq.Exam_Paper_Id = ep.Exam_Paper_Id
                WHERE ep.Exam_Id = %s
            """, (exam_id,))

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

            return jsonify({
                "success": True,
                "questions": results
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

        finally:
            cursor.close()

    @question_bp.route('/questions/paper/add', methods=['POST'])
    def add_question_to_paper():
        data = request.json

        exam_paper_id = data.get('exam_paper_id')
        question_id = data.get('question_id')
        email = data.get("email")   # ⚠️ better to send in body
        role = data.get("role")

        if not exam_paper_id or not question_id or not email or not role:
            return jsonify({
                "success": False,
                "message": "Missing required data"
            }), 400

        conn = mysql.connection
        cursor = conn.cursor()

        try:
            # 🔎 Step 1: Get Exam_Id from exam_paper
            cursor.execute(
                "SELECT Exam_Id FROM exam_paper WHERE Exam_Paper_Id = %s",
                (exam_paper_id,)
            )
            row = cursor.fetchone()

            if not row:
                return jsonify({
                    "success": False,
                    "message": "Invalid Exam Paper"
                }), 404

            exam_id = row[0]

            # 🔐 Step 2: Authorization Check
            if not is_exam_authorized(cursor, exam_id, email, role):
                return jsonify({
                    "success": False,
                    "message": "Unauthorized Access"
                }), 403

            # ✅ Step 3: Insert Question into Paper
            cursor.execute("""
                INSERT INTO exam_paper_questions 
                (Exam_Paper_Id, Question_Id)
                VALUES (%s, %s)
            """, (exam_paper_id, question_id))

            conn.commit()

            return jsonify({
                "success": True,
                "message": "Question added to paper"
            }), 201

        except Exception as e:
            conn.rollback()
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

        finally:
            cursor.close()

    @question_bp.route('/questions/paper/delete', methods=['POST'])
    def delete_question_from_paper():
        data = request.json

        exam_paper_id = data.get('exam_paper_id')
        question_id = data.get('question_id')
        email = data.get("email")
        role = data.get("role")

        if not exam_paper_id or not question_id or not email or not role:
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        conn = mysql.connection
        cursor = conn.cursor()

        try:
            # 🔎 Step 1: Get Exam_Id from exam_paper
            cursor.execute("""
                SELECT Exam_Id 
                FROM exam_paper 
                WHERE Exam_Paper_Id = %s
            """, (exam_paper_id,))

            row = cursor.fetchone()

            if not row:
                return jsonify({
                    "success": False,
                    "message": "Invalid exam paper"
                }), 404

            exam_id = row[0]

            # 🔐 Step 2: Authorization Check
            if not is_exam_authorized(cursor, exam_id, email, role):
                return jsonify({
                    "success": False,
                    "message": "Unauthorized Access"
                }), 403

            # 🗑 Step 3: Delete Question
            cursor.execute("""
                DELETE FROM exam_paper_questions
                WHERE Exam_Paper_Id = %s AND Question_Id = %s
            """, (exam_paper_id, question_id))

            conn.commit()

            return jsonify({
                "success": True,
                "message": "Question removed from paper"
            }), 200

        except Exception as e:
            conn.rollback()
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

        finally:
            cursor.close()

    @question_bp.route('/questions/paper/randomize/<int:exam_id>', methods=['POST'])
    def randomize_questions_for_paper(exam_id):
        data = request.json
        limit = data.get('limit', 10)
        email = request.args.get("email")
        role = request.args.get("role")
        conn = mysql.connection
        cursor = conn.cursor()
        
        if not email or not role:
            return jsonify({
                "success": False,
                "message": "Missing authentication details"
            }), 400
        
        if not is_exam_authorized(cursor, exam_id, email, role):
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Unauthorized Access"
            }), 403 
            
        try:
            cursor.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s", (exam_id,))
            paper = cursor.fetchone()
            if not paper:
                return jsonify({'error': 'No paper found for this exam'}), 404
            paper_id = paper[0]
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
        email = request.args.get("email")
        role = request.args.get("role")
        conn = mysql.connection
        cursor = conn.cursor()
        
        if not is_exam_authorized(cursor, exam_id, email, role):
            cursor.close()
            return jsonify({
                "success": False,
                "message": "Unauthorized Access"
            }), 403 
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
