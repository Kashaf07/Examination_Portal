from flask import Blueprint, request, jsonify
import MySQLdb.cursors

def create_faculty_groups_routes(mysql):
    bp = Blueprint('faculty_groups', __name__)

    # ==================================================
    # GET ALL FACULTY GROUPS
    # ==================================================
    @bp.route('/faculty-groups', methods=['GET'])
    def get_faculty_groups():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT Group_Id, Group_Name
            FROM faculty_groups
            ORDER BY Group_Name
        """)
        groups = cursor.fetchall()
        cursor.close()

        return jsonify({
            "success": True,
            "groups": groups
        })

    # ==================================================
    # GET FACULTY LIST OF A GROUP (WITH is_assigned FLAG)
    # ==================================================
    @bp.route('/faculty-groups/<int:group_id>/faculty', methods=['GET'])
    def get_group_faculty(group_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            SELECT 
                f.Faculty_Id,
                f.Faculty_Name,
                f.Faculty_Email,
                CASE 
                    WHEN fga.Faculty_Id IS NULL THEN 0 ELSE 1
                END AS is_assigned
            FROM mst_faculty f
            LEFT JOIN faculty_group_assign fga
                ON f.Faculty_Id = fga.Faculty_Id
                AND fga.Group_Id = %s
            ORDER BY f.Faculty_Name
        """, (group_id,))

        faculty = cursor.fetchall()
        cursor.close()

        return jsonify({
            "success": True,
            "faculty": faculty
        })

    # ==================================================
    # ASSIGN FACULTY TO GROUP
    # ==================================================
    @bp.route('/faculty-groups/assign', methods=['POST'])
    def assign_faculty_to_group():
        data = request.get_json()
        group_id = data.get("group_id")
        faculty_ids = data.get("faculty_ids", [])

        if not group_id or not faculty_ids:
            return jsonify({
                "success": False,
                "message": "Missing group_id or faculty_ids"
            }), 400

        cursor = mysql.connection.cursor()

        for fid in faculty_ids:
            cursor.execute("""
                INSERT IGNORE INTO faculty_group_assign (Faculty_Id, Group_Id)
                VALUES (%s, %s)
            """, (fid, group_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "assigned_count": len(faculty_ids)
        })

    return bp

