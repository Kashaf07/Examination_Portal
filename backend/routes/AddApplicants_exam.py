from flask import Blueprint, jsonify, request
import MySQLdb.cursors

def create_add_applicants_exam_bp(mysql):
    bp = Blueprint('add_applicants_exam', __name__)

    # ==================================================
    # ❌ REMOVED / COMMENTED OUT GROUP LIST ROUTE
    # Groups are handled ONLY in groups_routes.py
    # ==================================================
    #
    # @bp.route('/groups', methods=['GET'])
    # def get_groups():
    #     pass
    #

    # ==================================================
    # ✅ GET APPLICANTS OF A GROUP
    # ==================================================
    @bp.route('/groups/<int:group_id>/applicants', methods=['GET'])
    def get_group_applicants(group_id):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("""
                SELECT 
                    Applicant_Id,
                    Full_Name,
                    Email
                FROM applicants
                WHERE group_id = %s
            """, (group_id,))

            applicants = cursor.fetchall()
            cursor.close()

            return jsonify({
                "success": True,
                "applicants": applicants
            })

        except Exception as e:
            print("❌ Error fetching group applicants:", e)
            return jsonify({
                "success": False,
                "message": "Failed to load applicants"
            }), 500

    # ==================================================
    # ✅ ASSIGN ENTIRE GROUP TO EXAM
    # ==================================================
    @bp.route('/exam/assign-group', methods=['POST'])
    def assign_group_to_exam():
        try:
            data = request.get_json()
            exam_id = data.get("exam_id")
            group_id = data.get("group_id")

            if not exam_id or not group_id:
                return jsonify({
                    "success": False,
                    "message": "Missing exam_id or group_id"
                }), 400

            cursor = mysql.connection.cursor()

            # Get applicants of the group
            cursor.execute("""
                SELECT Applicant_Id
                FROM applicants
                WHERE group_id = %s
            """, (group_id,))
            applicant_ids = [row[0] for row in cursor.fetchall()]

            if not applicant_ids:
                return jsonify({
                    "success": False,
                    "message": "Group has no applicants"
                }), 400

            # Already assigned applicants
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

            return jsonify({
                "success": True,
                "assigned_count": len(new_ids)
            })

        except Exception as e:
            print("❌ Error assigning group:", e)
            return jsonify({
                "success": False,
                "message": "Failed to assign exam"
            }), 500

    return bp
