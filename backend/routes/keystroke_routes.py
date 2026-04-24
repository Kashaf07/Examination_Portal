from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback
import MySQLdb.cursors

def create_keystroke_routes(mysql):
    keystroke_bp = Blueprint('keystroke', __name__)

    # =====================================================
    # SAVE KEYSTROKE LOGS (BATCH)
    # =====================================================
    @keystroke_bp.route('/log', methods=['POST'])
    def log_keystrokes():
        try:
            data = request.json
            logs = data.get('logs', [])
            if not logs:
                return jsonify(success=False, message="No logs provided"), 400

            cursor = mysql.connection.cursor()
            insert_query = """
                INSERT INTO keystroke_logs
                (Attempt_Id, Applicant_Id, Question_Id, Key_Pressed, Key_Code,
                 Is_Ctrl, Is_Alt, Is_Shift, Is_Meta, Key_Combination, Log_Type, Timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = []
            for log in logs:
                values.append((
                    log.get('attempt_id'),
                    log.get('applicant_id'),
                    log.get('question_id'),
                    log.get('key_pressed'),
                    log.get('key_code'),
                    1 if log.get('is_ctrl') else 0,
                    1 if log.get('is_alt') else 0,
                    1 if log.get('is_shift') else 0,
                    1 if log.get('is_meta') else 0,
                    log.get('key_combination'),
                    log.get('log_type', 'key'),   # 'key' | 'mouse'
                    log.get('timestamp')
                ))
            cursor.executemany(insert_query, values)
            mysql.connection.commit()
            cursor.close()
            return jsonify(success=True, message=f"{len(logs)} keystrokes logged")

        except Exception as e:
            print("❌ Keystroke logging error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Server error"), 500

    # =====================================================
    # GET KEYSTROKE LOGS BY ATTEMPT (grouped by question)
    # =====================================================
    @keystroke_bp.route('/logs/<int:attempt_id>', methods=['GET'])
    def get_keystroke_logs(attempt_id):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Attempt info
            cursor.execute("""
                SELECT ee.Exam_Name, aa.Applicant_Id, a.Full_Name, a.Email
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN entrance_exam ee ON ep.Exam_Id = ee.Exam_Id
                JOIN applicants a ON aa.Applicant_Id = a.Applicant_Id
                WHERE aa.Attempt_Id = %s
            """, (attempt_id,))
            attempt_info = cursor.fetchone()

            if not attempt_info:
                cursor.close()
                return jsonify(success=False, message="Attempt not found"), 404

            # All questions for this exam paper (so we show ALL questions even if no keystrokes)
            cursor.execute("""
                SELECT DISTINCT eq.Question_Id, eq.Question_Text, eq.Question_Type
                FROM applicant_attempt aa
                JOIN exam_paper ep ON aa.Exam_Paper_Id = ep.Exam_Paper_Id
                JOIN exam_paper_questions epq ON ep.Exam_Paper_Id = epq.Exam_Paper_Id
                JOIN entrance_question_bank eq ON epq.Question_Id = eq.Question_Id
                WHERE aa.Attempt_Id = %s
                ORDER BY eq.Question_Id
            """, (attempt_id,))
            all_questions = cursor.fetchall()

            # Keystroke logs
            cursor.execute("""
                SELECT
                    kl.Question_Id,
                    kl.Key_Pressed,
                    kl.Key_Code,
                    kl.Is_Ctrl,
                    kl.Is_Alt,
                    kl.Is_Shift,
                    kl.Is_Meta,
                    kl.Key_Combination,
                    kl.Log_Type,
                    kl.Timestamp
                FROM keystroke_logs kl
                WHERE kl.Attempt_Id = %s
                ORDER BY kl.Question_Id, kl.Timestamp
            """, (attempt_id,))
            raw_logs = cursor.fetchall()
            cursor.close()

            # Group keystrokes by question_id
            ks_by_question = {}
            for log in raw_logs:
                qid = log['Question_Id']
                if qid not in ks_by_question:
                    ks_by_question[qid] = []
                ks_by_question[qid].append({
                    'key':         log['Key_Pressed'],
                    'code':        log['Key_Code'],
                    'ctrl':        bool(log['Is_Ctrl']),
                    'alt':         bool(log['Is_Alt']),
                    'shift':       bool(log['Is_Shift']),
                    'meta':        bool(log['Is_Meta']),
                    'combination': log['Key_Combination'],
                    'log_type':    log['Log_Type'] or 'key',
                    'timestamp':   str(log['Timestamp'])
                })

            # Build result for every question
            result_logs = []
            for q in all_questions:
                qid = q['Question_Id']
                keystrokes = ks_by_question.get(qid, [])
                result_logs.append({
                    'question_id':   qid,
                    'question_text': q['Question_Text'],
                    'question_type': q['Question_Type'],
                    'keystrokes':    keystrokes
                })

            return jsonify(
                success=True,
                exam_name=attempt_info['Exam_Name'],
                student_name=attempt_info['Full_Name'],
                student_email=attempt_info['Email'],
                logs=result_logs
            )

        except Exception as e:
            print("❌ Get keystroke logs error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Server error"), 500

    # =====================================================
    # GET WARNINGS (from restricted_attempts)
    # =====================================================
    @keystroke_bp.route('/warnings/<int:attempt_id>', methods=['GET'])
    def get_warnings(attempt_id):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""
                SELECT Reason, Restricted_Timestamp
                FROM restricted_attempts
                WHERE Attempt_Id = %s
                ORDER BY Restricted_Timestamp
            """, (attempt_id,))
            rows = cursor.fetchall()
            cursor.close()

            warnings = []
            for r in rows:
                warnings.append({
                    'Reason': r['Reason'],
                    'Timestamp': str(r['Restricted_Timestamp'])
                })

            return jsonify(success=True, warnings=warnings)

        except Exception as e:
            print("❌ Get warnings error:", e)
            traceback.print_exc()
            return jsonify(success=False, message="Server error"), 500

    return keystroke_bp
