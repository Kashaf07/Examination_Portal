from flask import Blueprint, request, jsonify
import MySQLdb.cursors

def create_view_responses_bp(mysql):
    view_responses_bp = Blueprint('view_responses', __name__)

    @view_responses_bp.route('/exam/can-view-responses', methods=['GET'])
    def can_view_responses():
        exam_id = request.args.get("exam_id")
        email = request.args.get("email")
        role = request.args.get("role")  # Admin / Faculty

        if not exam_id or not email or not role:
            return jsonify(success=False), 400

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 🔴 Admin → exam must exist
        if role == "Admin":
            cursor.execute(
                "SELECT 1 FROM entrance_exam WHERE Exam_Id = %s",
                (exam_id,)
            )

        # 🔵 Faculty → exam must belong to them
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

        exam = cursor.fetchone()
        cursor.close()

        if not exam:
            return jsonify(success=False), 403

        return jsonify(success=True), 200

    @view_responses_bp.route('/attempts', methods=['GET'])
    def get_attempts():
        exam_id = request.args.get('exam_id')
        email = request.args.get('email')
        role = request.args.get('role')

        if not exam_id or not email or not role:
            return jsonify(success=False, message="Missing parameters"), 400

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Auth check
            if role not in ['Admin', 'Faculty']:
                return jsonify(success=False, message="Unauthorized"), 403

            # Authorization check
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

            if not cursor.fetchone():
                cursor.close()
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

            # ── Key Logs (one query for all attempts) - ONLY blocked and warning ────
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
                      AND Event_Type IN ('blocked', 'warning')
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

            # ── Build summary (counts per key+type) - ONLY violations ────────
            def build_summary(logs):
                from collections import Counter
                counts = Counter()
                for l in logs:
                    # Skip 'allowed' events (already filtered in query, but double-check)
                    if l["event_type"] == "allowed":
                        continue
                    
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

            cursor.close()
            return jsonify(success=True, attempts=attempts_out)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify(success=False, message=str(e)), 500

    return view_responses_bp
