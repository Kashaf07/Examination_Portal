from flask import Blueprint, request, jsonify
import MySQLdb.cursors

def create_faculty_groups_routes(mysql):
    bp = Blueprint('faculty_groups', __name__)

    # GET ALL FACULTY GROUPS
    @bp.route('/faculty-groups', methods=['GET'])
    def get_faculty_groups():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT 
                Group_Id,
                Group_Name,
                Created_On,
                Is_Active
            FROM faculty_groups
            ORDER BY Is_Active DESC, Group_Name
        """)
        groups = cursor.fetchall()
        cursor.close()
        return jsonify(success=True, groups=groups)

    
    @bp.route('/faculty-groups/toggle-status/<int:group_id>', methods=['PUT'])
    def toggle_group_status(group_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE faculty_groups
            SET Is_Active = CASE
                WHEN Is_Active = 1 THEN 0
                ELSE 1
            END
            WHERE Group_Id = %s
        """, (group_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify(success=True, message="Group status updated")

    # CREATE FACULTY GROUP (ADMIN ONLY)
   
    @bp.route('/faculty-groups/create', methods=['POST'])
    def create_faculty_group():
        data = request.get_json()
        role = data.get("role")
        group_name = data.get("group_name")

        if role != "Admin":
            return jsonify(success=False, message="Only admin allowed"), 403

        if not group_name:
            return jsonify(success=False, message="Group name required"), 400

        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT 1 FROM faculty_groups WHERE Group_Name = %s
        """, (group_name,))
        if cursor.fetchone():
            cursor.close()
            return jsonify(success=False, message="Group already exists"), 409

        cursor.execute("""
            INSERT INTO faculty_groups (Group_Name)
            VALUES (%s)
        """, (group_name,))
        mysql.connection.commit()
        cursor.close()

        return jsonify(success=True, message="Faculty group created")

   
    # VIEW FACULTY IN A GROUP
    @bp.route('/faculty-groups/<int:group_id>/faculty', methods=['GET'])
    def view_group_faculty(group_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT 
                f.Faculty_Id,
                f.F_Name  AS Faculty_Name,
                f.F_Email AS Faculty_Email,
                fga.Assigned_On
            FROM faculty_group_assign fga
            INNER JOIN mst_faculty f
                ON fga.Faculty_Id = f.Faculty_Id
            WHERE fga.Group_Id = %s
            ORDER BY f.F_Name
        """, (group_id,))
        faculty = cursor.fetchall()
        cursor.close()
        return jsonify(success=True, faculty=faculty)

    # GET AVAILABLE FACULTY (NOT IN GROUP) 

    @bp.route('/faculty-groups/<int:group_id>/available-faculty', methods=['GET'])
    def available_faculty(group_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT 
                f.Faculty_Id,
                f.F_Name  AS Faculty_Name,
                f.F_Email AS Faculty_Email
            FROM mst_faculty f
            WHERE f.Faculty_Id NOT IN (
                SELECT Faculty_Id
                FROM faculty_group_assign
                WHERE Group_Id = %s
            )
            ORDER BY f.F_Name
        """, (group_id,))
        faculty = cursor.fetchall()
        cursor.close()
        return jsonify(success=True, faculty=faculty)

    # ADD SINGLE FACULTY TO GROUP  
    @bp.route('/faculty-groups/add-faculty', methods=['POST'])
    def add_faculty_to_group():
        data = request.get_json()
        group_id = data.get("group_id")
        faculty_id = data.get("faculty_id")

        if not group_id or not faculty_id:
            return jsonify(success=False, message="Missing data"), 400

        cursor = mysql.connection.cursor()

        # 🔒 CHECK IF GROUP IS ACTIVE
        cursor.execute("""
            SELECT Is_Active
            FROM faculty_groups
            WHERE Group_Id = %s
        """, (group_id,))
        row = cursor.fetchone()

        if not row:
            cursor.close()
            return jsonify(success=False, message="Group not found"), 404

        if row[0] == 0:
            cursor.close()
            return jsonify(
                success=False,
                message="This faculty group is disabled"
            ), 403

        # ✅ GROUP IS ACTIVE → ADD FACULTY
        cursor.execute("""
            INSERT IGNORE INTO faculty_group_assign (Faculty_Id, Group_Id)
            VALUES (%s, %s)
        """, (faculty_id, group_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify(success=True, message="Faculty added successfully")

    # REMOVE FACULTY FROM GROUP
    @bp.route('/faculty-groups/remove-faculty', methods=['POST'])
    def remove_faculty():
        data = request.get_json()
        group_id = data.get("group_id")
        faculty_id = data.get("faculty_id")

        if not group_id or not faculty_id:
            return jsonify(success=False, message="Missing data"), 400

        cursor = mysql.connection.cursor()

        # 🔒 CHECK GROUP STATUS
        cursor.execute("""
            SELECT Is_Active
            FROM faculty_groups
            WHERE Group_Id = %s
        """, (group_id,))
        row = cursor.fetchone()

        if not row or row[0] == 0:
            cursor.close()
            return jsonify(
                success=False,
                message="This faculty group is disabled"
            ), 403

        cursor.execute("""
            DELETE FROM faculty_group_assign
            WHERE Group_Id = %s AND Faculty_Id = %s
        """, (group_id, faculty_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify(success=True, message="Faculty removed")

    # DELETE FACULTY GROUP (ADMIN ONLY)
    @bp.route('/faculty-groups/<int:group_id>', methods=['DELETE'])
    def delete_group(group_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            DELETE FROM faculty_group_assign WHERE Group_Id = %s
        """, (group_id,))
        cursor.execute("""
            DELETE FROM faculty_groups WHERE Group_Id = %s
        """, (group_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify(success=True, message="Faculty group deleted")

    return bp
