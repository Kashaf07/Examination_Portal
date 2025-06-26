from flask import Blueprint, request, jsonify
from MySQLdb.cursors import DictCursor  
import random

def create_exam_paper_routes(mysql):
    exam_paper_bp = Blueprint('exam_paper', __name__)

    @exam_paper_bp.route('/questionbank/all/<int:exam_id>', methods=['GET'])
    def get_all_questions(exam_id):
        print(f"➡️ Fetching questions for Exam ID: {exam_id}")
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("SELECT * FROM entrance_question_bank WHERE Exam_Id = %s", (exam_id,))
        return jsonify(cur.fetchall())
    
    @exam_paper_bp.route('/api/exam/details/<int:exam_id>', methods=['GET'])
    def get_exam_details(exam_id):
        print(f"📥 Getting exam details for Exam ID: {exam_id}")
        try:
            cursor = mysql.connection.cursor(DictCursor)
            cursor.execute("SELECT Exam_Name, Max_Marks AS Total_Marks FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            row = cursor.fetchone()
            print("📤 Query Result:", row)
            if row:
                return jsonify({
                    'exam_name': row['Exam_Name'],
                    'total_marks': row['Total_Marks']
                    })
            else:
                return jsonify({'error': 'Exam not found'}), 404
        except Exception as e:
            print("❌ Exception:", str(e))
            return jsonify({'error': str(e)}), 500



    @exam_paper_bp.route('/save-question-paper', methods=['POST'])
    def save_question_paper():
        data = request.get_json()
        exam_id = data.get('exam_id')
        question_ids = data.get('questions', [])

        print(f"➡️ Received exam_id: {exam_id}")
        print(f"➡️ Received questions: {question_ids}")

        conn = mysql.connection
        cur = conn.cursor()

        try:
            # 🟡 Fetch Exam Info from entrance_exam
            cur.execute("SELECT Exam_Name, Duration_Minutes, Max_Marks FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            exam_info = cur.fetchone()

            if not exam_info:
                return jsonify({'error': 'Exam not found in entrance_exam'}), 404

            exam_name, duration, max_marks = exam_info
            print(f"📘 Fetched exam info: {exam_name}, {duration} min, {max_marks} marks")

            # 🟢 Check if paper exists
            cur.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s ORDER BY Created_At DESC LIMIT 1", (exam_id,))
            paper = cur.fetchone()

            if not paper:
                print("📄 No existing paper found. Creating one...")
                cur.execute("""
                    INSERT INTO exam_paper (Exam_Id, Title, Total_Marks, Duration_Minutes)
                    VALUES (%s, %s, %s, %s)
                """, (exam_id, exam_name, max_marks, duration))
                conn.commit()
                exam_paper_id = cur.lastrowid
            else:
                exam_paper_id = paper[0]
                print(f"📄 Existing paper found with ID: {exam_paper_id}")

            # 🧹 Clear previous questions
            cur.execute("DELETE FROM exam_paper_questions WHERE Exam_Paper_Id = %s", (exam_paper_id,))

            # 📝 Insert new questions
            for qid in question_ids:
                cur.execute("INSERT INTO exam_paper_questions (Exam_Paper_Id, Question_Id) VALUES (%s, %s)", (exam_paper_id, qid))

            conn.commit()
            return jsonify({'message': '✅ Question paper saved successfully!'}), 200

        except Exception as e:
            conn.rollback()
            print("❌ Error occurred:", e)
            return jsonify({'error': 'Failed to save question paper'}), 500
        
    @exam_paper_bp.route('/randomize/<int:exam_id>', methods=['POST'])
    def randomize_questions(exam_id):
        print(f"🎲 Randomizing questions for Exam ID: {exam_id}")
        cur = mysql.connection.cursor(DictCursor)

        # Get paper ID (create one if it doesn’t exist)
        cur.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s ORDER BY Created_At DESC LIMIT 1", (exam_id,))
        paper = cur.fetchone()

        if not paper:
            # Fetch title, duration, and max_marks from entrance_exam
            cur.execute("SELECT Exam_Name, Duration_Minutes, Max_Marks, Total_Questions FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            exam_info = cur.fetchone()

            if not exam_info:
                return jsonify({'error': 'Exam info not found'}), 404

            cur.execute("INSERT INTO exam_paper (Exam_Id, Title, Duration_Minutes, Total_Marks) VALUES (%s, %s, %s, %s)",
                        (exam_id, exam_info['Exam_Name'], exam_info['Duration_Minutes'], exam_info['Max_Marks']))
            mysql.connection.commit()
            paper_id = cur.lastrowid
            total_questions = exam_info['Total_Questions']
        else:
            paper_id = paper['Exam_Paper_Id']
            cur.execute("SELECT Total_Questions FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            total_questions = cur.fetchone()['Total_Questions']

        # Clear existing
        cur.execute("DELETE FROM exam_paper_questions WHERE Exam_Paper_Id = %s", (paper_id,))

        # Randomly select questions
        cur.execute("""
            SELECT * FROM entrance_question_bank
            WHERE Exam_Id = %s
            ORDER BY RAND() LIMIT %s
        """, (exam_id, total_questions))

        selected = cur.fetchall()

        for q in selected:
            cur.execute("INSERT INTO exam_paper_questions (Exam_Paper_Id, Question_Id) VALUES (%s, %s)",
                        (paper_id, q['Question_Id']))

        mysql.connection.commit()
        return jsonify(selected)


    return exam_paper_bp
