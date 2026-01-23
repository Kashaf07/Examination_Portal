from flask import Blueprint, jsonify, request
import MySQLdb.cursors

def create_add_applicants_exam_bp(mysql):
    bp = Blueprint('add_applicants_exam', __name__)

    # ==================================================
    # ✅ GET APPLICANTS OF A GROUP (SAFE + BACKWARD COMPATIBLE)
    # ==================================================
    @bp.route('/groups/<int:group_id>/applicants', methods=['GET'])
    def get_group_applicants(group_id):
        try:
            exam_id = request.args.get("exam_id")  # OPTIONAL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # --------------------------------------------------
            # If exam_id is provided → mark already assigned
            # --------------------------------------------------
            if exam_id:
                cursor.execute("""
                    SELECT 
                        a.Applicant_Id,
                        a.Full_Name,
                        a.Email,
                        CASE 
                            WHEN ae.Assign_Id IS NULL THEN 0
                            ELSE 1
                        END AS is_assigned
                    FROM applicants a
                    LEFT JOIN applicant_exam_assign ae
                      ON a.Applicant_Id = ae.Applicant_Id
                      AND ae.Exam_Id = %s
                    WHERE a.group_id = %s
                """, (exam_id, group_id))
            else:
                # --------------------------------------------------
                # OLD BEHAVIOR (unchanged)
                # --------------------------------------------------
                cursor.execute("""
                    SELECT 
                        Applicant_Id,
                        Full_Name,
                        Email,
                        0 AS is_assigned
                    FROM applicants
                    WHERE group_id = %s
                """, (group_id,))

            applicants = cursor.fetchall()
            cursor.close()

            return jsonify(
                success=True,
                applicants=applicants
            )

        except Exception as e:
            print("❌ Error fetching group applicants:", e)
            return jsonify(
                success=False,
                message="Failed to load applicants"
            ), 500

    # ==================================================
    # ✅ ASSIGN SELECTED APPLICANTS TO EXAM (FINAL CONFIRM)
    # ==================================================
    @bp.route('/assign_applicants', methods=['POST'])
    def assign_applicants():
        try:
            data = request.get_json()
            exam_id = data.get("exam_id")
            applicant_ids = data.get("applicant_ids", [])

            if not exam_id or not applicant_ids:
                return jsonify(
                    success=False,
                    message="Missing exam_id or applicant_ids"
                ), 400

            cursor = mysql.connection.cursor()

            # --------------------------------------------------
            # Fetch already assigned applicants
            # --------------------------------------------------
            cursor.execute("""
                SELECT Applicant_Id
                FROM applicant_exam_assign
                WHERE Exam_Id = %s
            """, (exam_id,))
            already_assigned = set(row[0] for row in cursor.fetchall())

            inserted_count = 0

            # --------------------------------------------------
            # Insert only NEW applicants
            # --------------------------------------------------
            for applicant_id in applicant_ids:
                if applicant_id not in already_assigned:
                    cursor.execute("""
                        INSERT INTO applicant_exam_assign (Applicant_Id, Exam_Id)
                        VALUES (%s, %s)
                    """, (applicant_id, exam_id))
                    inserted_count += 1

            mysql.connection.commit()
            cursor.close()

            return jsonify(
                success=True,
                assigned_count=inserted_count
            )

        except Exception as e:
            print("❌ Error assigning applicants:", e)
            return jsonify(
                success=False,
                message="Failed to assign applicants"
            ), 500

    # ==================================================
    # ⚠️ OLD GROUP ASSIGN API (UNCHANGED – OPTIONAL)
    # ==================================================
    @bp.route('/exam/assign-group', methods=['POST'])
    def assign_group_to_exam():
        try:
            data = request.get_json()
            exam_id = data.get("exam_id")
            group_id = data.get("group_id")

            if not exam_id or not group_id:
                return jsonify(
                    success=False,
                    message="Missing exam_id or group_id"
                ), 400

            cursor = mysql.connection.cursor()

            cursor.execute("""
                SELECT Applicant_Id
                FROM applicants
                WHERE group_id = %s
            """, (group_id,))
            applicant_ids = [row[0] for row in cursor.fetchall()]

            if not applicant_ids:
                return jsonify(
                    success=False,
                    message="Group has no applicants"
                ), 400

            cursor.execute("""
                SELECT Applicant_Id
                FROM applicant_exam_assign
                WHERE Exam_Id = %s
            """, (exam_id,))
            assigned = set(row[0] for row in cursor.fetchall())

            new_ids = [aid for aid in applicant_ids if aid not in assigned]

            for aid in new_ids:
                cursor.execute("""
                    INSERT INTO applicant_exam_assign (Applicant_Id, Exam_Id)
                    VALUES (%s, %s)
                """, (aid, exam_id))

            mysql.connection.commit()
            cursor.close()

            return jsonify(
                success=True,
                assigned_count=len(new_ids)
            )

        except Exception as e:
            print("❌ Error assigning group:", e)
            return jsonify(
                success=False,
                message="Failed to assign exam"
            ), 500

    return bp
