from flask import Blueprint, request, jsonify

def create_exam_paper_routes(mysql):
    exam_paper_bp = Blueprint('exam_paper', __name__)

    @exam_paper_bp.route('/api/questionbank/all/<int:exam_id>', methods=['GET'])
    def get_all_questions(exam_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM entrance_question_bank WHERE Exam_Id = %s", (exam_id,))
        return jsonify([dict(row) for row in cur.fetchall()])

    @exam_paper_bp.route('/api/paper/questions/<int:exam_id>', methods=['GET'])
    def get_selected_questions(exam_id):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT b.Question_Id, b.Question_Text, b.Marks
            FROM exam_paper_questions AS epq
            JOIN entrance_question_bank AS b ON epq.Question_Id = b.Question_Id
            WHERE epq.Exam_Paper_Id = %s
        """, (exam_id,))
        return jsonify([dict(row) for row in cur.fetchall()])

    @exam_paper_bp.route('/api/paper/add', methods=['POST'])
    def add_to_paper():
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute("INSERT IGNORE INTO exam_paper_questions (Exam_Paper_Id, Question_Id) VALUES (%s, %s)", 
                    (data['exam_id'], data['question_id']))
        mysql.connection.commit()
        return jsonify({'message': 'Question added'})

    @exam_paper_bp.route('/api/paper/delete/<int:exam_id>/<int:question_id>', methods=['DELETE'])
    def delete_from_paper(exam_id, question_id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM exam_paper_questions WHERE Exam_Paper_Id = %s AND Question_Id = %s", 
                    (exam_id, question_id))
        mysql.connection.commit()
        return jsonify({'message': 'Question removed'})

    @exam_paper_bp.route('/api/paper/randomize/<int:exam_id>', methods=['POST'])
    def randomize_questions(exam_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT Total_Questions FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
        total_qs = cur.fetchone()
        if not total_qs:
            return jsonify({'error': 'Exam not found'}), 404

        total = total_qs['Total_Questions']
        cur.execute("DELETE FROM exam_paper_questions WHERE Exam_Paper_Id = %s", (exam_id,))
        cur.execute("""
            SELECT Question_Id FROM entrance_question_bank 
            WHERE Exam_Id = %s ORDER BY RAND() LIMIT %s
        """, (exam_id, total))
        selected = cur.fetchall()
        for row in selected:
            cur.execute("INSERT INTO exam_paper_questions (Exam_Paper_Id, Question_Id) VALUES (%s, %s)",
                        (exam_id, row['Question_Id']))
        mysql.connection.commit()
        return jsonify({'message': f'{len(selected)} questions randomized'})

    return exam_paper_bp
