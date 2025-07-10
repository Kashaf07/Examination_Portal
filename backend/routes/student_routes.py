from flask import Blueprint, request, jsonify
from datetime import datetime

def create_student_routes(mysql):
    student_routes = Blueprint('student_routes', __name__)

    # 🔹 Existing: Get next upcoming exam
    @student_routes.route('/exam', methods=['GET'])
    def get_exam_data():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM entrance_exam WHERE Exam_Date >= CURDATE() ORDER BY Exam_Date ASC LIMIT 1")
            exam = cur.fetchone()

            if not exam:
                return jsonify({"message": "No upcoming exam found"}), 404

            exam_id = exam[0]

            cur.execute("""
                        SELECT q.Question_Id, q.Exam_Id, q.Question_Type, q.Question_Text, 
                        q.Option_A, q.Option_B, q.Option_C, q.Option_D
                        FROM entrance_question_bank q   
                        JOIN exam_paper_questions epq ON q.Question_Id = epq.Question_Id
                        JOIN exam_paper ep ON epq.Exam_Paper_Id = ep.Exam_Paper_Id    
                        WHERE ep.Exam_Id = %s
                        """, (exam_id,))
            questions = cur.fetchall()
            print("🧪 Query result:", exam_id)

            cur.execute("SELECT * FROM exam_paper WHERE Exam_Id = %s", (exam_id,))
            exam_paper = cur.fetchone()

            if not exam_paper:
                cur.execute("""
                    INSERT INTO exam_paper (Exam_Id, Title, Total_Marks, Duration_Minutes)
                    VALUES (%s, %s, %s, %s)
                """, (exam_id, exam[1], exam[6], exam[4]))
                mysql.connection.commit()
                exam_paper_id = cur.lastrowid
            else:
                exam_paper_id = exam_paper[0]

            cur.close()

            return jsonify({
                "exam": {
                    "Exam_Id": exam[0],
                    "Exam_Paper_Id": exam_paper_id,
                    "Exam_Name": exam[1],
                    "Exam_Date": str(exam[2]),
                    "Exam_Time": str(exam[3]),
                    "Duration_Minutes": exam[4],
                    "Total_Questions": exam[5],
                    "Max_Marks": exam[6],
                    "Faculty_Email": exam[7],
                },
                "questions": [
                    {
                        "Question_Id": q[0],
                        "Question_Type": q[2],
                        "Question_Text": q[3],
                        "Option_A": q[4],
                        "Option_B": q[5],
                        "Option_C": q[6],
                        "Option_D": q[7]
                    } for q in questions
                ]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # 🔹 NEW: Fetch exam data using specific Exam_Id
    @student_routes.route('/exam/<int:exam_id>', methods=['GET'])
    def get_exam_by_id(exam_id):
        try:
            cur = mysql.connection.cursor()
            
            print("🔍 Exam ID received:", exam_id)
            cur.execute("SELECT * FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            exam = cur.fetchone()
            print("🧪 Query result:", exam)

            if not exam:
                return jsonify({"message": "Invalid Exam ID"}), 404

            # ✅ Fetch ONLY selected questions
            cur.execute("""
                        SELECT q.Question_Id, q.Exam_Id, q.Question_Type, q.Question_Text, 
                        q.Option_A, q.Option_B, q.Option_C, q.Option_D
                        FROM entrance_question_bank q   
                        JOIN exam_paper_questions epq ON q.Question_Id = epq.Question_Id
                        JOIN exam_paper ep ON epq.Exam_Paper_Id = ep.Exam_Paper_Id    
                        WHERE ep.Exam_Id = %s
                        """, (exam_id,))
            questions = cur.fetchall()
        

            cur.execute("SELECT * FROM exam_paper WHERE Exam_Id = %s", (exam_id,))
            exam_paper = cur.fetchone()

            if not exam_paper:
                cur.execute("""
                    INSERT INTO exam_paper (Exam_Id, Title, Total_Marks, Duration_Minutes)
                    VALUES (%s, %s, %s, %s)
                """, (exam_id, exam[1], exam[6], exam[4]))
                mysql.connection.commit()
                exam_paper_id = cur.lastrowid
            else:
                exam_paper_id = exam_paper[0]

            cur.close()

            return jsonify({
                "exam": {
                    "Exam_Id": exam[0],
                    "Exam_Paper_Id": exam_paper_id,
                    "Exam_Name": exam[1],
                    "Exam_Date": str(exam[2]),
                    "Exam_Time": str(exam[3]),
                    "Duration_Minutes": exam[4],
                    "Total_Questions": exam[5],
                    "Max_Marks": exam[6],
                    "Faculty_Email": exam[7],
                },
                "questions": [
                    {
                        "Question_Id": q[0],
                        "Question_Type": q[2],
                        "Question_Text": q[3],
                        "Option_A": q[4],
                        "Option_B": q[5],
                        "Option_C": q[6],
                        "Option_D": q[7]
                    } for q in questions
                ]
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # 🔹 Submit answers and create attempt
    @student_routes.route('/submit', methods=['POST'])
    def submit_answers():
        try:
            data = request.json
            applicant_id = data['applicant_id']
            exam_paper_id = data['exam_paper_id']
            answers = data['answers']

            cur = mysql.connection.cursor()

            start_time = datetime.now()
            end_time = datetime.now()
            status = "Submitted"

            cur.execute("""
                INSERT INTO applicant_attempt (Applicant_Id, Exam_Paper_Id, Start_Time, End_Time, Status)
                VALUES (%s, %s, %s, %s, %s)
            """, (applicant_id, exam_paper_id, start_time, end_time, status))

            attempt_id = cur.lastrowid
            total_marks = 0

            for ans in answers:
                question_id = ans['question_id']
                selected_option = ans['selected_option']
                cur.execute("""
                    SELECT Question_Type, Correct_Answer, Marks,
                        Option_A, Option_B, Option_C, Option_D
                    FROM entrance_question_bank
                    WHERE Question_Id = %s
                """, (question_id,))

                row = cur.fetchone()
  
                if not row:
                    continue
                q_type, correct_answer, marks, opt_a, opt_b, opt_c, opt_d = row
  
                # Convert option if needed
                option_map = {'A': opt_a, 'B': opt_b, 'C': opt_c, 'D': opt_d}
  
                if q_type in ('MCQ', 'TF'):
                    selected_text = option_map.get(selected_option, "")
                    is_correct = selected_text.strip().lower() == correct_answer.strip().lower()
                elif q_type in ('Fill', 'OneWord'):
                    selected_text = selected_option # User typed input
                    is_correct = selected_text.strip().lower() == correct_answer.strip().lower()
                else:
                    is_correct = False
  
                # Add marks if correct
                if is_correct:
                    total_marks += marks
                # Store selected option and answer
                cur.execute("""
                    INSERT INTO applicant_answers (Attempt_Id, Question_Id, Selected_Option_Id, Answer_Text)
                    VALUES (%s, %s, %s, %s)
                """, (
                    attempt_id,
                    question_id,
                    selected_option if q_type in ('MCQ', 'TF') else None,
                    selected_text if q_type in ('MCQ', 'TF') else selected_option
                ))

            # Update total marks
            cur.execute("""
                UPDATE applicant_attempt SET Marks_Obtained = %s WHERE Attempt_Id = %s
            """, (total_marks, attempt_id))


            # Auto grading logic
            cur.execute("SELECT Total_Marks FROM exam_paper WHERE Exam_Paper_Id = %s", (exam_paper_id,))
            total_possible_marks = cur.fetchone()[0]
            grading_status = "Fail"
            if total_possible_marks > 0:
                percentage = (total_marks / total_possible_marks) * 100
                grading_status = "Pass" if percentage >= 40 else "Fail"
 
            cur.execute("""
                INSERT INTO auto_grading (Attempt_Id, Total_Score, Status)
                VALUES (%s, %s, %s)
            """, (attempt_id, total_marks, grading_status))
            mysql.connection.commit()
            cur.close()
 
            return jsonify({"message": "Answers submitted successfully", "Attempt_Id": attempt_id})
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": str(e)}), 500



    # 🔹 View all attempts of a student
    @student_routes.route('/attempts/<int:applicant_id>', methods=['GET'])
    def get_attempts(applicant_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT aa.Attempt_Id, aa.Start_Time, aa.End_Time, aa.Status, 
                       ep.Title, ee.Exam_Name
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN entrance_exam ee ON ep.Exam_Id = ee.Exam_Id
                WHERE aa.Applicant_Id = %s
                ORDER BY aa.Start_Time DESC
            """, (applicant_id,))
            attempts = cur.fetchall()
            cur.close()

            return jsonify({
                "attempts": [{
                    "Attempt_Id": a[0],
                    "Start_Time": str(a[1]),
                    "End_Time": str(a[2]),
                    "Status": a[3],
                    "Paper_Title": a[4],
                    "Exam_Name": a[5]
                } for a in attempts],
                "total_attempts": len(attempts)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return student_routes


