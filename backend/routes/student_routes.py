from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

def create_student_routes(mysql):
    student_routes = Blueprint('student_routes', __name__)

    # Helper function to check if exam_time is timedelta and convert to time
    def get_exam_datetime(exam_date, exam_time):
        # Handle datetime.time or timedelta objects
        if isinstance(exam_time, timedelta):
            # Convert timedelta to time object for datetime.combine
            return datetime.combine(exam_date, (datetime.min + exam_time).time())
        else:
            return datetime.combine(exam_date, exam_time)

    # Get next upcoming exam
    @student_routes.route('/exam', methods=['GET'])
    def get_exam_data():
        try:
            cur = mysql.connection.cursor()
            
            # Get the next upcoming exam
            cur.execute("""
                SELECT Exam_Id, Exam_Name, Exam_Date, Exam_Time, Duration_Minutes, 
                       Total_Questions, Max_Marks, Faculty_Email
                FROM entrance_exam 
                WHERE Exam_Date >= CURDATE()
                ORDER BY Exam_Date, Exam_Time 
                LIMIT 1
            """)
            exam = cur.fetchone()

            if not exam:
                return jsonify({"message": "No upcoming exam found"}), 404

            exam_id = exam[0]

            # Get questions for this exam
            cur.execute("""
                SELECT q.Question_Id, q.Exam_Id, q.Question_Type, q.Question_Text, 
                       q.Option_A, q.Option_B, q.Option_C, q.Option_D
                FROM entrance_question_bank q   
                JOIN exam_paper_questions epq ON q.Question_Id = epq.Question_Id
                JOIN exam_paper ep ON epq.Exam_Paper_Id = ep.Exam_Paper_Id    
                WHERE ep.Exam_Id = %s
            """, (exam_id,))
            questions = cur.fetchall()

            # Get or create exam paper
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

    # Start exam attempt
    @student_routes.route('/start-exam', methods=['POST'])
    def start_exam_attempt():
        try:
            data = request.json
            applicant_id = data.get('applicant_id')
            exam_id = data.get('exam_id')
            
            if not applicant_id or not exam_id:
                return jsonify({"message": "Applicant ID and Exam ID are required"}), 400
            
            cur = mysql.connection.cursor()
            
            # Get student email
            cur.execute("SELECT Email FROM applicants WHERE Applicant_Id = %s", (applicant_id,))
            applicant_result = cur.fetchone()
            
            if not applicant_result:
                cur.close()
                return jsonify({"error": "Applicant not found"}), 404
            
            student_email = applicant_result[0]
            
            # Get exam paper ID
            cur.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s", (exam_id,))
            exam_paper_result = cur.fetchone()
            
            if not exam_paper_result:
                # Attempt to create exam paper if it doesn't exist (robustness)
                cur.execute("""
                    SELECT Exam_Name, Duration_Minutes, Max_Marks FROM entrance_exam WHERE Exam_Id = %s
                """, (exam_id,))
                exam_details = cur.fetchone()
                if exam_details:
                    cur.execute("""
                        INSERT INTO exam_paper (Exam_Id, Title, Total_Marks, Duration_Minutes)
                        VALUES (%s, %s, %s, %s)
                    """, (exam_id, exam_details[0], exam_details[2], exam_details[1]))
                    mysql.connection.commit()
                    exam_paper_id = cur.lastrowid
                else:
                    cur.close()
                    return jsonify({"error": "Exam paper or Exam not found"}), 404
            else:
                exam_paper_id = exam_paper_result[0]
            
            # Check if attempt already exists and is not restricted/submitted
            cur.execute("""
                SELECT aa.Attempt_Id, aa.Status FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                WHERE aa.Applicant_Id = %s AND ep.Exam_Id = %s
                ORDER BY aa.Start_Time DESC LIMIT 1
            """, (applicant_id, exam_id))
            
            existing_attempt = cur.fetchone()
            if existing_attempt and existing_attempt[1] in ('Submitted', 'Restricted'):
                cur.close()
                return jsonify({
                    "message": "Attempt already completed/restricted",
                    "attempt_id": existing_attempt[0],
                    "status": existing_attempt[1]
                }), 409
            
            if existing_attempt and existing_attempt[1] == 'In Progress':
                 cur.close()
                 return jsonify({
                    "message": "Attempt already in progress",
                    "attempt_id": existing_attempt[0]
                }), 200 # OK to continue
            
            # Create new attempt
            start_time = datetime.now()
            cur.execute("""
                INSERT INTO applicant_attempt (Applicant_Id, Student_Email, Exam_Paper_Id, Start_Time, Status)
                VALUES (%s, %s, %s, %s, %s)
            """, (applicant_id, student_email, exam_paper_id, start_time, "In Progress"))
            
            attempt_id = cur.lastrowid
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                "message": "Exam attempt started successfully",
                "attempt_id": attempt_id,
                "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": str(e)}), 500

    # Fetch exam data using specific Exam_Id WITH 10-MINUTE LIMIT
    @student_routes.route('/exam/<int:exam_id>', methods=['POST'])
    def get_exam_by_id(exam_id):
        try:
            data = request.json
            applicant_id = data.get('applicant_id')
            
            if not applicant_id:
                return jsonify({"message": "Applicant ID is required"}), 400
            
            cur = mysql.connection.cursor()
            
            # Check if exam exists
            cur.execute("SELECT * FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            exam = cur.fetchone()

            if not exam:
                cur.close()
                return jsonify({"message": "Invalid Exam ID"}), 404

            # Time validation
            exam_date = exam[2]
            exam_time = exam[3]
            duration_minutes = exam[4]
            
            exam_datetime = get_exam_datetime(exam_date, exam_time)
            exam_end_entry_window = exam_datetime + timedelta(minutes=10)
            current_time = datetime.now()
            
            if current_time < exam_datetime:
                cur.close()
                return jsonify({
                    "error": f"Exam has not started yet. Please wait until {exam_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
                }), 425
            
            if current_time > exam_end_entry_window:
                cur.close()
                return jsonify({
                    "error": f"Exam entry time has expired. You cannot start the exam after 10 minutes of exam start time."
                }), 410

            # Check if student is assigned
            cur.execute("""
                SELECT COUNT(*) FROM applicant_exam_assign 
                WHERE Applicant_Id = %s AND Exam_Id = %s
            """, (applicant_id, exam_id))
            
            if cur.fetchone()[0] == 0:
                cur.close()
                return jsonify({
                    "message": "Access Denied", 
                    "error": "You are not assigned to this exam. Please contact your faculty."
                }), 403

            # Check existing attempt - INCLUDING RESTRICTION CHECK
            cur.execute("""
                SELECT aa.Attempt_Id, aa.Status, aa.Start_Time, ra.Id as Restriction_Id
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                LEFT JOIN restricted_attempts ra ON aa.Attempt_Id = ra.Attempt_Id
                WHERE aa.Applicant_Id = %s AND ep.Exam_Id = %s
                ORDER BY aa.Start_Time DESC LIMIT 1
            """, (applicant_id, exam_id))
            
            attempt_result = cur.fetchone()
            
            attempt_id = None
            remaining_seconds = duration_minutes * 60
            
            if attempt_result:
                attempt_id, status, start_time, restriction_id = attempt_result
                if status == 'Submitted' or restriction_id is not None:
                    cur.close()
                    return jsonify({
                        "message": "Already Attempted", 
                        "error": "You have already attempted this exam. Multiple attempts are not allowed."
                    }), 409
                
                if status == 'In Progress':
                    attempt_start_time = start_time
                    exam_duration = timedelta(minutes=duration_minutes)
                    exam_end_time = attempt_start_time + exam_duration
                    time_remaining = exam_end_time - current_time
                    
                    if time_remaining.total_seconds() <= 0:
                        # Attempt timed out - auto-submit with 0 marks
                        cur.execute("""
                            UPDATE applicant_attempt 
                            SET End_Time = %s, Status = 'Submitted', Marks_Obtained = 0.00
                            WHERE Attempt_Id = %s
                        """, (current_time, attempt_id))
                        # Insert/Update auto_grading for timeout
                        cur.execute("""
                            INSERT INTO auto_grading (Attempt_Id, Total_Score, Status)
                            VALUES (%s, 0.00, 'Fail')
                            ON DUPLICATE KEY UPDATE Total_Score=0.00, Status='Fail'
                        """, (attempt_id,))
                        mysql.connection.commit()
                        cur.close()
                        return jsonify({
                            "message": "Attempt Timed Out", 
                            "error": "Your previous attempt timed out and was automatically closed."
                        }), 410
                        
                    remaining_seconds = int(time_remaining.total_seconds())

            # Fetch questions
            cur.execute("""
                SELECT q.Question_Id, q.Exam_Id, q.Question_Type, q.Question_Text, 
                       q.Option_A, q.Option_B, q.Option_C, q.Option_D
                FROM entrance_question_bank q   
                JOIN exam_paper_questions epq ON q.Question_Id = epq.Question_Id
                JOIN exam_paper ep ON epq.Exam_Paper_Id = ep.Exam_Paper_Id    
                WHERE ep.Exam_Id = %s
            """, (exam_id,))
            questions = cur.fetchall()

            # Get or create exam paper
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
                    "Remaining_Seconds": remaining_seconds
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
                ],
                "attempt_id": attempt_id
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Get assigned exams - WITH RESTRICTION STATUS
    @student_routes.route('/assigned-exams/<int:applicant_id>', methods=['GET'])
    def get_assigned_exams(applicant_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT ee.Exam_Id, ee.Exam_Name, ee.Exam_Date, ee.Exam_Time, 
                       ee.Duration_Minutes, ee.Total_Questions, ee.Max_Marks,
                       aea.Assigned_On,
                       aa.Status,
                       ra.Id
                FROM applicant_exam_assign aea
                JOIN entrance_exam ee ON aea.Exam_Id = ee.Exam_Id
                LEFT JOIN exam_paper ep ON ee.Exam_Id = ep.Exam_Id
                LEFT JOIN applicant_attempt aa ON aa.Applicant_Id = aea.Applicant_Id AND aa.Exam_Paper_Id = ep.Exam_Paper_Id
                LEFT JOIN restricted_attempts ra ON aa.Attempt_Id = ra.Attempt_Id
                WHERE aea.Applicant_Id = %s
                ORDER BY ee.Exam_Date, ee.Exam_Time, aa.Start_Time DESC
            """, (applicant_id,))
            
            assigned_exams_raw = cur.fetchall()
            cur.close()

            exam_statuses = {}
            for exam in assigned_exams_raw:
                exam_id = exam[0]
                attempt_status = exam[8]
                restriction_id = exam[9]

                current_status = 'Pending'
                if restriction_id or attempt_status == 'Restricted':
                    current_status = 'Restricted'
                elif attempt_status == 'Submitted':
                    current_status = 'Completed'
                elif attempt_status == 'In Progress':
                    current_status = 'In Progress'
                
                # Use only the status of the latest relevant attempt per exam
                if exam_id not in exam_statuses or current_status in ('Restricted', 'Completed', 'In Progress'):
                    exam_statuses[exam_id] = {
                        "Exam_Id": exam[0],
                        "Exam_Name": exam[1],
                        "Exam_Date": str(exam[2]),
                        "Exam_Time": str(exam[3]),
                        "Duration_Minutes": exam[4],
                        "Total_Questions": exam[5],
                        "Max_Marks": exam[6],
                        "Assigned_On": str(exam[7]),
                        "Status": current_status
                    }

            return jsonify({
                "assigned_exams": list(exam_statuses.values())
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Report student restriction (for cheating/malpractice)
    @student_routes.route('/report-restriction', methods=['POST'])
    def report_restriction():
        try:
            data = request.json
            attempt_id = data.get('attempt_id')
            applicant_id = data.get('applicant_id')
            exam_paper_id = data.get('exam_paper_id')
            reason = data.get('reason', 'Academic misconduct detected')
            
            if not attempt_id or not applicant_id or not exam_paper_id:
                return jsonify({"error": "Missing required fields"}), 400
            
            cur = mysql.connection.cursor()
            
            cur.execute("""
                SELECT Attempt_Id, Status, Student_Email FROM applicant_attempt 
                WHERE Attempt_Id = %s AND Applicant_Id = %s
            """, (attempt_id, applicant_id))
            
            attempt = cur.fetchone()
            if not attempt:
                cur.close()
                return jsonify({"error": "Attempt not found"}), 404
            
            student_email = attempt[2]

            cur.execute("""
                SELECT Id FROM restricted_attempts WHERE Attempt_Id = %s
            """, (attempt_id,))
            
            if cur.fetchone():
                cur.close()
                return jsonify({"message": "Attempt already marked as restricted"}), 200
            
            # 1. Update attempt status to 'Restricted' and set Marks_Obtained to 0.00
            current_time = datetime.now()
            cur.execute("""
                UPDATE applicant_attempt 
                SET Status = 'Restricted', End_Time = %s, Marks_Obtained = 0.00
                WHERE Attempt_Id = %s
            """, (current_time, attempt_id))
            
            # 2. Insert into restricted_attempts table
            cur.execute("""
                INSERT INTO restricted_attempts (Attempt_Id, Applicant_Id, Exam_Paper_Id, Reason)
                VALUES (%s, %s, %s, %s)
            """, (attempt_id, applicant_id, exam_paper_id, reason))
            
            # 3. Update or Insert into auto_grading to show 'Restricted' status (Total_Score must be 0.00)
            cur.execute("""
                INSERT INTO auto_grading (Attempt_Id, Total_Score, Status, Evaluated_At)
                VALUES (%s, 0.00, 'Restricted', %s)
                ON DUPLICATE KEY UPDATE 
                Total_Score = 0.00, Status = 'Restricted', Evaluated_At = %s
            """, (attempt_id, current_time, current_time))
            
            # 4. Auto-logout
            cur2 = mysql.connection.cursor()
            cur2.execute("""
                UPDATE login_log
                SET Logout_Time = %s
                WHERE User_Email = %s
                AND Role = 'Student'
                ORDER BY Log_ID DESC
                LIMIT 1
            """, (current_time, student_email))
            cur2.close()

            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                "message": "Student attempt marked as restricted successfully",
                "attempt_id": attempt_id,
                "status": "Restricted",
                "total_marks": 0.00
            })
            
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": str(e)}), 500

    # Submit answers with optional restriction flag
    @student_routes.route('/submit', methods=['POST'])
    def submit_answers():
        try:
            data = request.json
            applicant_id = data['applicant_id']
            exam_paper_id = data['exam_paper_id']
            answers = data['answers']
            attempt_id = data.get('attempt_id')
            is_restricted = data.get('is_restricted', False)
            restriction_reason = data.get('restriction_reason', 'Academic misconduct detected')

            cur = mysql.connection.cursor()
            end_time = datetime.now()
            total_marks = 0.00 

            cur.execute("SELECT Email FROM applicants WHERE Applicant_Id = %s", (applicant_id,))
            applicant_result = cur.fetchone()
            if not applicant_result:
                cur.close()
                return jsonify({"error": "Applicant not found"}), 404
            student_email = applicant_result[0]

            # --- 1. Process Answers and Calculate Marks ---
            for ans in answers:
                question_id = ans['question_id']
                selected_option = ans.get('selected_option') or ans.get('answer_text')
                if not selected_option:
                    continue
                
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
                option_map = {'A': opt_a, 'B': opt_b, 'C': opt_c, 'D': opt_d}
                
                selected_text = selected_option
                is_correct = False
                
                if q_type in ('MCQ', 'TF'):
                    # Selected_option will be 'A', 'B', 'C', or 'D'
                    selected_text = option_map.get(selected_option, "")
                    is_correct = selected_text.strip().lower() == correct_answer.strip().lower()
                elif q_type in ('Fill', 'OneWord'):
                    # Selected_option/answer_text is the user's input
                    is_correct = selected_text.strip().lower() == correct_answer.strip().lower()
                
                # Award marks only if correct and NOT restricted
                if is_correct and not is_restricted:
                    total_marks += marks
                
                # Insert answer record - using INSERT IGNORE or ON DUPLICATE KEY UPDATE might be better for safety
                cur.execute("""
                    INSERT INTO applicant_answers (Attempt_Id, Question_Id, Selected_Option_Id, Answer_Text)
                    VALUES (%s, %s, %s, %s)
                """, (
                    attempt_id,
                    question_id,
                    selected_option if q_type in ('MCQ', 'TF') else None, # Store option letter for MCQ/TF
                    selected_text
                ))

            # --- 2. Update/Create Attempt Record ---
            attempt_status = "Restricted" if is_restricted else "Submitted"
            final_marks = 0.00 if is_restricted else total_marks

            if attempt_id:
                # Update existing attempt
                cur.execute("""
                    UPDATE applicant_attempt 
                    SET End_Time = %s, Status = %s, Marks_Obtained = %s
                    WHERE Attempt_Id = %s
                """, (end_time, attempt_status, final_marks, attempt_id))
            else:
                # Create new attempt (Shouldn't happen if /start-exam is used)
                start_time = end_time
                cur.execute("""
                    INSERT INTO applicant_attempt (Applicant_Id, Student_Email, Exam_Paper_Id, Start_Time, End_Time, Status, Marks_Obtained)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (applicant_id, student_email, exam_paper_id, start_time, end_time, attempt_status, final_marks))
                attempt_id = cur.lastrowid
                
           # --- 3. Handle Restriction and Grading ---
# --- 3. Handle Restriction and Grading ---
            if is_restricted:
                grading_status = "Restricted"
                grading_score = 0.00
                
                # Insert into restricted_attempts table
                cur.execute("""
                    INSERT INTO restricted_attempts (Attempt_Id, Applicant_Id, Exam_Paper_Id, Reason)
                    VALUES (%s, %s, %s, %s)
                """, (attempt_id, applicant_id, exam_paper_id, restriction_reason))
                
            else:
                # Normal submission - calculate Pass/Fail based on actual marks earned
                grading_score = total_marks  # Use the calculated marks
                
                cur.execute("SELECT Total_Marks FROM exam_paper WHERE Exam_Paper_Id = %s", (exam_paper_id,))
                exam_paper_result = cur.fetchone()
                
                if exam_paper_result and exam_paper_result[0]:
                    total_possible_marks = float(exam_paper_result[0])
                    if total_possible_marks > 0:
                        percentage = (total_marks / total_possible_marks) * 100
                        grading_status = "Pass" if percentage >= 40 else "Fail"
                    else:
                        grading_status = "Fail"
                else:
                    grading_status = "Fail"

            # ALWAYS insert/update auto_grading for EVERY submission
            cur.execute("""
                INSERT INTO auto_grading (Attempt_Id, Total_Score, Status, Evaluated_At)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                Total_Score = %s, Status = %s, Evaluated_At = %s
            """, (attempt_id, grading_score, grading_status, end_time, grading_score, grading_status, end_time))

            # Commit everything together
            mysql.connection.commit()

            mysql.connection.commit()

            # --- 4. Auto-logout ---
            cur2 = mysql.connection.cursor()
            cur2.execute("""
                UPDATE login_log
                SET Logout_Time = %s
                WHERE User_Email = %s
                AND Role = 'Student'
                ORDER BY Log_ID DESC
                LIMIT 1
            """, (end_time, student_email))
            mysql.connection.commit()
            cur2.close()
            cur.close()

            return jsonify({
                "message": "Exam restricted due to violation" if is_restricted else "Exam submitted successfully",
                "Attempt_Id": attempt_id,
                "Student_Email": student_email,
                "Total_Marks": final_marks,
                "Status": grading_status,
                "Is_Restricted": is_restricted
            })
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"error": str(e)}), 500

    # View all attempts (including restricted) - UPDATED TO SHOW RESTRICTION PROPERLY
    @student_routes.route('/attempts/<int:applicant_id>', methods=['GET'])
    def get_attempts(applicant_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT aa.Attempt_Id, aa.Start_Time, aa.End_Time, aa.Status, 
                       aa.Marks_Obtained, aa.Student_Email, ep.Title, ee.Exam_Name, ee.Max_Marks,
                       ag.Status as Grade_Status,
                       ra.Reason as Restriction_Reason,
                       ra.Id as Restriction_Id
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN entrance_exam ee ON ep.Exam_Id = ee.Exam_Id
                LEFT JOIN auto_grading ag ON aa.Attempt_Id = ag.Attempt_Id
                LEFT JOIN restricted_attempts ra ON aa.Attempt_Id = ra.Attempt_Id
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
                    # Primary status for sorting/filtering (Submitted or Restricted)
                    "Status": "Restricted" if a[11] else a[3], 
                    "Marks_Obtained": float(a[4]), 
                    "Student_Email": a[5],
                    "Paper_Title": a[6],
                    "Exam_Name": a[7],
                    "Max_Marks": a[8],
                    # Grade_Status is used for Pass/Fail/Restricted display
                    "Grade_Status": "Restricted" if a[11] else a[9],
                    "Is_Restricted": bool(a[11]), # Use this flag on the frontend!
                    "Restriction_Reason": a[10] if a[11] else None
                } for a in attempts],
                "total_attempts": len(attempts)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Get exam status
    @student_routes.route('/exam-status/<int:exam_id>/<int:applicant_id>', methods=['GET'])
    def get_exam_status(exam_id, applicant_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM entrance_exam WHERE Exam_Id = %s", (exam_id,))
            exam = cur.fetchone()
            
            if not exam:
                return jsonify({"error": "Exam not found"}), 404
            
            exam_date = exam[2]
            exam_time = exam[3]
            
            exam_datetime = get_exam_datetime(exam_date, exam_time)
            
            exam_end_entry_window = exam_datetime + timedelta(minutes=10)
            current_time = datetime.now()
            
            status = "NOT_STARTED"
            message = f"Exam will start at {exam_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            
            if current_time > exam_datetime:
                if current_time > exam_end_entry_window:
                    status = "EXPIRED"
                    message = f"Exam entry time expired."
                else:
                    status = "ACTIVE"
                    remaining_seconds = int((exam_end_entry_window - current_time).total_seconds())
                    message = f"Exam entry window is active. {remaining_seconds} seconds remaining."
            
            # Check for existing attempts (submitted or restricted)
            cur.execute("""
                SELECT aa.Attempt_Id, aa.Status, ra.Id as Restriction_Id
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                LEFT JOIN restricted_attempts ra ON aa.Attempt_Id = ra.Attempt_Id
                WHERE aa.Applicant_Id = %s AND ep.Exam_Id = %s
                ORDER BY aa.Start_Time DESC LIMIT 1
            """, (applicant_id, exam_id))
            
            attempt_result = cur.fetchone()
            
            if attempt_result:
                attempt_status = attempt_result[1]
                restriction_id = attempt_result[2]
                
                if restriction_id or attempt_status == 'Restricted':
                    status = "RESTRICTED"
                    message = "You are restricted from this exam due to academic misconduct."
                elif attempt_status == 'Submitted':
                    status = "COMPLETED"
                    message = "You have already completed this exam."
                elif attempt_status == 'In Progress':
                    status = "IN_PROGRESS"
                    message = "You have an ongoing attempt."
            
            cur.close()
            return jsonify({
                "status": status,
                "message": message,
                "exam_datetime": exam_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                "exam_end_entry_window": exam_end_entry_window.strftime('%Y-%m-%d %H:%M:%S'),
                "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Get all restricted attempts (Admin/Faculty view)
    @student_routes.route('/restricted-attempts', methods=['GET'])
    def get_restricted_attempts():
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT ra.Id, ra.Attempt_Id, ra.Applicant_Id, ra.Exam_Paper_Id, 
                       ra.Reason, ra.Restricted_Timestamp,
                       ap.Full_Name, ap.Email,
                       ee.Exam_Name, ep.Title as Paper_Title,
                       aa.Marks_Obtained
                FROM restricted_attempts ra
                JOIN applicants ap ON ra.Applicant_Id = ap.Applicant_Id
                JOIN exam_paper ep ON ra.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN entrance_exam ee ON ep.Exam_Id = ee.Exam_Id
                JOIN applicant_attempt aa ON ra.Attempt_Id = aa.Attempt_Id
                ORDER BY ra.Restricted_Timestamp DESC
            """)
            
            restricted = cur.fetchall()
            cur.close()
            
            return jsonify({
                "restricted_attempts": [{
                    "Id": r[0],
                    "Attempt_Id": r[1],
                    "Applicant_Id": r[2],
                    "Exam_Paper_Id": r[3],
                    "Reason": r[4],
                    "Restricted_Timestamp": str(r[5]),
                    "Student_Name": r[6],
                    "Student_Email": r[7],
                    "Exam_Name": r[8],
                    "Paper_Title": r[9],
                    "Marks_Obtained": 0.00 # Marks are always 0.00 for restricted attempts
                } for r in restricted],
                "total_restricted": len(restricted)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return student_routes