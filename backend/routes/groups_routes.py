from flask import Blueprint, request, jsonify, current_app

group_bp = Blueprint("group_bp", __name__)

def get_mysql():
    return current_app.config["MYSQL"]

# ==================================================
# CREATE APPLICANT GROUP
# ==================================================
@group_bp.route("/create", methods=["POST"])
def create_group():
    data = request.get_json()
    group_name = data.get("group_name")
    role = data.get("role")
    email = data.get("email")

    if not group_name or not role or not email:
        return jsonify(success=False, message="Invalid data"), 400

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    if role == "Admin":
        cur.execute("SELECT 1 FROM mst_admin WHERE Email=%s", (email,))
    else:
        cur.execute("SELECT 1 FROM mst_faculty WHERE F_Email=%s", (email,))

    if not cur.fetchone():
        cur.close()
        return jsonify(success=False, message="Unauthorized"), 403

    cur.execute(
        "SELECT 1 FROM applicant_groups WHERE group_name=%s",
        (group_name.strip(),)
    )
    if cur.fetchone():
        cur.close()
        return jsonify(success=False, message="Group already exists"), 409

    cur.execute("""
        INSERT INTO applicant_groups (group_name, Faculty_Email)
        VALUES (%s, %s)
    """, (group_name.strip(), email))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True, message="Group created successfully")

# ==================================================
# GET GROUPS WITH APPLICANT COUNT ✅ FIXED
# ==================================================
@group_bp.route("", methods=["GET"])
def get_groups():
    role = request.args.get("role")
    email = request.args.get("email")

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    if role == "Admin":
        cur.execute("""
            SELECT 
                g.group_id,
                g.group_name,
                g.Faculty_Email,
                g.Created_At,
                COUNT(a.Applicant_Id) AS applicant_count
            FROM applicant_groups g
            LEFT JOIN applicants a ON a.group_id = g.group_id AND a.Is_Active = 1
            WHERE g.group_name != '__UNASSIGNED__'
            GROUP BY g.group_id
            ORDER BY g.Created_At DESC
        """)
    else:
        cur.execute("""
            SELECT 
                g.group_id,
                g.group_name,
                g.Faculty_Email,
                g.Created_At,
                COUNT(a.Applicant_Id) AS applicant_count
            FROM applicant_groups g
            LEFT JOIN applicants a ON a.group_id = g.group_id AND a.Is_Active = 1
            WHERE g.Faculty_Email=%s
              AND g.group_name != '__UNASSIGNED__'
            GROUP BY g.group_id
            ORDER BY g.Created_At DESC
        """, (email,))

    rows = cur.fetchall()
    cur.close()

    return jsonify(
        success=True,
        groups=[
            {
                "Group_Id": r[0],
                "Group_Name": r[1],
                "Faculty_Email": r[2],
                "Created_At": r[3],
                "Applicant_Count": r[4]
            } for r in rows
        ]
    )

# ==================================================
# GET APPLICANTS OF GROUP
# ==================================================
@group_bp.route("/<int:group_id>/applicants", methods=["GET"])
def get_group_applicants(group_id):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT Applicant_Id, Full_Name, Email
        FROM applicants
        WHERE group_id=%s
        AND Is_Active = 1
    """, (group_id,))

    rows = cur.fetchall()
    cur.close()

    return jsonify(
        success=True,
        applicants=[
            {
                "Applicant_Id": r[0],
                "Full_Name": r[1],
                "Email": r[2]
            } for r in rows
        ]
    )

# ==================================================
# REMOVE APPLICANT FROM GROUP
# ==================================================
@group_bp.route("/remove-applicant", methods=["POST"])
def remove_applicant():
    data = request.get_json()
    applicant_id = data.get("applicant_id")

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT group_id FROM applicant_groups
        WHERE group_name='__UNASSIGNED__'
        LIMIT 1
    """)
    row = cur.fetchone()

    if row:
        unassigned_id = row[0]
    else:
        cur.execute("""
            INSERT INTO applicant_groups (group_name, Faculty_Email)
            VALUES ('__UNASSIGNED__', 'system@internal')
        """)
        mysql.connection.commit()
        unassigned_id = cur.lastrowid

    cur.execute("""
        UPDATE applicants
        SET group_id=%s
        WHERE Applicant_Id=%s
    """, (unassigned_id, applicant_id))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)

# ==================================================
# DELETE GROUP (ONE CLICK)
# ==================================================
@group_bp.route("/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT group_id FROM applicant_groups
        WHERE group_name='__UNASSIGNED__'
        LIMIT 1
    """)
    row = cur.fetchone()

    if row:
        unassigned_id = row[0]
    else:
        cur.execute("""
            INSERT INTO applicant_groups (group_name, Faculty_Email)
            VALUES ('__UNASSIGNED__', 'system@internal')
        """)
        mysql.connection.commit()
        unassigned_id = cur.lastrowid

    cur.execute("""
        UPDATE applicants
        SET group_id=%s
        WHERE group_id=%s
    """, (unassigned_id, group_id))

    cur.execute("""
        DELETE FROM applicant_groups
        WHERE group_id=%s
    """, (group_id,))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True, message="Group deleted successfully")
