from flask import Blueprint, request, jsonify
from MySQLdb.cursors import DictCursor

def create_exam_result_routes(mysql):
    exam_result_bp = Blueprint('exam_result', __name__)

    def is_exam_authorized(cursor, exam_id, email, role):
        if role == "Admin":
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s",
                (exam_id,)
            )
        else:
            cursor.execute(
                """
                SELECT 1 FROM entrance_exam
                WHERE Exam_Id = %s AND Faculty_Email = %s
                """,
                (exam_id, email)
            )
        return cursor.fetchone() is not None

    # ─── /attempts  (admin student attempts table) ────────────────────────────
    @exam_result_bp.route('/attempts', methods=['GET'])
    def get_attempts():
        exam_id = request.args.get('exam_id')
        email   = request.args.get('email')
        role    = request.args.get('role')

        if not exam_id or not email or not role:
            return jsonify(success=False, message="Missing parameters"), 400

        try:
            cursor = mysql.connection.cursor(DictCursor)

            # Auth check
            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            if not is_exam_authorized(cursor, exam_id, email, role):
                return jsonify(success=False, message="Unauthorized Access"), 403

            # Fetch all attempts for this exam
            cursor.execute("""
                SELECT
                    aa.Attempt_Id,
                    aa.Applicant_Id,
                    aa.Student_Email,
                    aa.Start_Time,
                    aa.End_Time,
                    aa.Marks_Obtained,
                    ee.Max_Marks,
                    ag.Status   AS Status,
                    ra.Id       AS Restriction_Id
                FROM applicant_attempt aa
                JOIN exam_paper  ep ON ep.Exam_Paper_Id = aa.Exam_Paper_Id
                JOIN entrance_exam ee ON ee.Exam_Id     = ep.Exam_Id
                LEFT JOIN auto_grading ag ON ag.Attempt_Id = aa.Attempt_Id
                LEFT JOIN restricted_attempts ra ON ra.Attempt_Id = aa.Attempt_Id
                WHERE ep.Exam_Id = %s
                  AND aa.Status IN ('Submitted', 'Restricted')
                ORDER BY aa.Attempt_Id ASC
            """, (exam_id,))
            raw_attempts = cursor.fetchall()

            # ── Key Logs (one query for all attempts) ────────────────────────
            attempt_ids = [r["Attempt_Id"] for r in raw_attempts]
            key_logs_by_attempt = {}

            if attempt_ids:
                fmt = ",".join(["%s"] * len(attempt_ids))
                cursor.execute(f"""
                    SELECT
                        Attempt_Id,
                        Event_Type,
                        Key_Value,
                        Ctrl_Key,
                        Shift_Key,
                        Alt_Key,
                        Meta_Key,
                        Log_Timestamp
                    FROM attempt_key_logs
                    WHERE Attempt_Id IN ({fmt})
                    ORDER BY Attempt_Id, Log_Timestamp ASC
                """, attempt_ids)
                for log in cursor.fetchall():
                    aid = log["Attempt_Id"]
                    if aid not in key_logs_by_attempt:
                        key_logs_by_attempt[aid] = []
                    key_logs_by_attempt[aid].append({
                        "event_type":    log["Event_Type"],
                        "key_value":     log["Key_Value"],
                        "ctrl_key":      bool(log["Ctrl_Key"]),
                        "shift_key":     bool(log["Shift_Key"]),
                        "alt_key":       bool(log["Alt_Key"]),
                        "meta_key":      bool(log["Meta_Key"]),
                        "log_timestamp": str(log["Log_Timestamp"])
                    })

            # ── Build summary (counts per key+type) ──────────────────────────
            def build_summary(logs):
                from collections import Counter
                counts = Counter()
                for l in logs:
                    modifiers = []
                    if l["ctrl_key"]:  modifiers.append("Ctrl")
                    if l["shift_key"]: modifiers.append("Shift")
                    if l["alt_key"]:   modifiers.append("Alt")
                    if l["meta_key"]:  modifiers.append("Meta")
                    label = "+".join(modifiers + [l["key_value"]]) if modifiers else l["key_value"]
                    counts[(label, l["event_type"])] += 1
                return [
                    {"key_label": k, "event_type": t, "count": c}
                    for (k, t), c in sorted(counts.items())
                ]

            # ── Format datetime helper ───────────────────────────────────────
            def fmt_dt(val):
                if val is None:
                    return None
                if hasattr(val, 'strftime'):
                    return val.strftime('%d %b %Y, %H:%M')
                return str(val)

            # ── Build response ───────────────────────────────────────────────
            attempts_out = []
            for r in raw_attempts:
                aid  = r["Attempt_Id"]
                logs = key_logs_by_attempt.get(aid, [])

                # Determine display status
                if r["Restriction_Id"]:
                    display_status = "Restricted"
                elif r["Status"]:
                    display_status = r["Status"]
                else:
                    display_status = "-"

                attempts_out.append({
                    "Attempt_Id":       aid,
                    "Applicant_Id":     r["Applicant_Id"],
                    "Student_Email":    r["Student_Email"] or "-",
                    "Start_Time":       fmt_dt(r["Start_Time"]),
                    "End_Time":         fmt_dt(r["End_Time"]),
                    "Marks_Obtained":   float(r["Marks_Obtained"]) if r["Marks_Obtained"] is not None else 0,
                    "Max_Marks":        float(r["Max_Marks"])       if r["Max_Marks"]       is not None else 0,
                    "Status":           display_status,
                    "key_log_summary":  build_summary(logs),
                    "key_log_total":    len(logs)
                })

            return jsonify(success=True, attempts=attempts_out)

        except Exception as e:
            import traceback; traceback.print_exc()
            return jsonify(success=False, message=str(e)), 500

    # ─── /exam/<id>/results  (result page) ───────────────────────────────────
    @exam_result_bp.route('/exam/<int:exam_id>/results', methods=['GET'])
    def get_exam_results(exam_id):

        email = request.args.get('email')
        role  = request.args.get('role')

        if not email or not role:
            return jsonify(success=False, message="Missing authentication"), 400

        try:
            cursor = mysql.connection.cursor(DictCursor)

            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            if not is_exam_authorized(cursor, exam_id, email, role):
                return jsonify(success=False, message="Unauthorized Access"), 403

            # Exam Info
            cursor.execute("""
                SELECT Exam_Name, Exam_Date, Exam_Time
                FROM entrance_exam
                WHERE Exam_Id = %s
            """, (exam_id,))
            exam = cursor.fetchone()

            if not exam:
                return jsonify(success=False, message="Exam not found"), 404

            # Student Results
            cursor.execute("""
                SELECT
                    a.Attempt_Id,
                    a.Applicant_Id,
                    ap.Full_Name  AS Student_Name,
                    a.Marks_Obtained,
                    a.Status
                FROM applicant_attempt a
                JOIN exam_paper ep ON ep.Exam_Paper_Id = a.Exam_Paper_Id
                JOIN applicants  ap ON ap.Applicant_Id  = a.Applicant_Id
                WHERE ep.Exam_Id = %s
                AND   a.Status IN ('Submitted', 'Restricted')
                ORDER BY a.Applicant_Id ASC
            """, (exam_id,))
            raw_results = cursor.fetchall()

            # Key Logs
            attempt_ids = [r["Attempt_Id"] for r in raw_results]
            key_logs_by_attempt = {}

            if attempt_ids:
                fmt = ",".join(["%s"] * len(attempt_ids))
                cursor.execute(f"""
                    SELECT
                        Attempt_Id,
                        Event_Type,
                        Key_Value,
                        Ctrl_Key,
                        Shift_Key,
                        Alt_Key,
                        Meta_Key,
                        Log_Timestamp
                    FROM attempt_key_logs
                    WHERE Attempt_Id IN ({fmt})
                    ORDER BY Attempt_Id, Log_Timestamp ASC
                """, attempt_ids)
                for log in cursor.fetchall():
                    aid = log["Attempt_Id"]
                    if aid not in key_logs_by_attempt:
                        key_logs_by_attempt[aid] = []
                    key_logs_by_attempt[aid].append({
                        "event_type":     log["Event_Type"],
                        "key_value":      log["Key_Value"],
                        "ctrl_key":       bool(log["Ctrl_Key"]),
                        "shift_key":      bool(log["Shift_Key"]),
                        "alt_key":        bool(log["Alt_Key"]),
                        "meta_key":       bool(log["Meta_Key"]),
                        "log_timestamp":  str(log["Log_Timestamp"])
                    })

            def build_summary(logs):
                from collections import Counter
                counts = Counter()
                for l in logs:
                    modifiers = []
                    if l["ctrl_key"]:  modifiers.append("Ctrl")
                    if l["shift_key"]: modifiers.append("Shift")
                    if l["alt_key"]:   modifiers.append("Alt")
                    if l["meta_key"]:  modifiers.append("Meta")
                    label = "+".join(modifiers + [l["key_value"]]) if modifiers else l["key_value"]
                    counts[(label, l["event_type"])] += 1
                return [
                    {"key_label": k, "event_type": t, "count": c}
                    for (k, t), c in sorted(counts.items())
                ]

            results = []
            for r in raw_results:
                aid  = r["Attempt_Id"]
                logs = key_logs_by_attempt.get(aid, [])
                results.append({
                    "Applicant_Id":    r["Applicant_Id"],
                    "Student_Name":    r["Student_Name"],
                    "Marks_Obtained":  r["Marks_Obtained"],
                    "Status":          r["Status"],
                    "key_log_summary": build_summary(logs),
                    "key_log_total":   len(logs)
                })

            return jsonify(
                success=True,
                exam_name=exam["Exam_Name"],
                exam_date=exam["Exam_Date"].strftime('%Y-%m-%d') if exam["Exam_Date"] else None,
                exam_time=str(exam["Exam_Time"]) if exam["Exam_Time"] else None,
                results=results
            )

        except Exception as e:
            return jsonify(success=False, message=str(e)), 500

    return exam_result_bp