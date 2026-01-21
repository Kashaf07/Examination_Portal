from flask import Blueprint, request, jsonify, current_app

group_bp = Blueprint('group_bp', __name__)

# Helper to get mysql instance
def get_mysql():
    return current_app.config['MYSQL']

# ---------------------------------------------------
# CREATE GROUP
# ---------------------------------------------------
@group_bp.route('/create', methods=['POST'])
def create_group():
    print("CREATE GROUP API HIT")

    data = request.get_json()
    print("DATA:", data)

    group_name = data.get('group_name')
    faculty_email = data.get('faculty_email')

    if not group_name or not faculty_email:
        return jsonify(success=False, message="Missing required fields"), 400

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    try:
        cur.execute("""
            INSERT INTO Applicant_Groups (group_name, Faculty_Email)
            VALUES (%s, %s)
        """, (group_name, faculty_email))

        mysql.connection.commit()
        return jsonify(success=True, message="Group created successfully")

    except Exception as e:
        mysql.connection.rollback()
        print("CREATE GROUP ERROR:", e)
        return jsonify(success=False, message=str(e)), 500

    finally:
        cur.close()

# ---------------------------------------------------
# GET GROUPS (FACULTY-WISE)
# ---------------------------------------------------
@group_bp.route('/<faculty_email>', methods=['GET'])
def get_groups(faculty_email):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT group_id, group_name, Created_At
        FROM Applicant_Groups
        WHERE Faculty_Email = %s
        ORDER BY Created_At DESC
    """, (faculty_email,))

    rows = cur.fetchall()
    cur.close()

    groups = [{
        "Group_Id": r[0],
        "Group_Name": r[1],
        "Created_At": r[2]
    } for r in rows]

    return jsonify(success=True, groups=groups)

# ---------------------------------------------------
# UPDATE GROUP
# ---------------------------------------------------
@group_bp.route('/update/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    data = request.get_json()
    group_name = data.get('group_name')

    if not group_name:
        return jsonify(success=False, message="Group name required"), 400

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE Applicant_Groups
        SET group_name = %s
        WHERE group_id = %s
    """, (group_name, group_id))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True, message="Group updated successfully")

# ---------------------------------------------------
# DELETE GROUP
# ---------------------------------------------------
@group_bp.route('/delete/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    try:
        cur.execute("DELETE FROM Applicant_Groups WHERE group_id = %s", (group_id,))
        mysql.connection.commit()
        return jsonify(success=True, message="Group deleted")
    except Exception as e:
        mysql.connection.rollback()
        return jsonify(success=False, message=str(e)), 500
    finally:
        cur.close()

# ---------------------------------------------------
# VIEW STUDENTS IN GROUP
# ---------------------------------------------------
@group_bp.route('/<int:group_id>/students', methods=['GET'])
def get_group_students(group_id):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT Applicant_Id, Full_Name, Email, Phone, Gender
        FROM applicants
        WHERE group_id = %s
    """, (group_id,))

    rows = cur.fetchall()
    cur.close()

    students = [{
        "Applicant_Id": r[0],
        "Full_Name": r[1],
        "Email": r[2],
        "Phone": r[3],
        "Gender": r[4]
    } for r in rows]

    return jsonify(success=True, students=students)
