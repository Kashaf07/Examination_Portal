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
# GET GROUPS WITH APPLICANT COUNT
# ==================================================
@group_bp.route("", methods=["GET"])
def get_groups():
    role = request.args.get("role")
    email = request.args.get("email")
    show_all = request.args.get("show_all") == "true"

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    base_query = """
        SELECT 
            g.group_id,
            g.group_name,
            g.Faculty_Email,
            g.Created_At,
            g.Is_Active,
            COUNT(CASE WHEN a.Is_Active = 1 THEN 1 END) AS applicant_count
        FROM applicant_groups g
        LEFT JOIN applicants a ON a.group_id = g.group_id
        WHERE g.group_name != '__UNASSIGNED__'
    """

    params = []

    if role != "Admin":
        base_query += " AND g.Faculty_Email=%s"
        params.append(email)

    if not show_all:
        base_query += " AND g.Is_Active = 1"

    base_query += """
        GROUP BY g.group_id
        ORDER BY g.Is_Active DESC, g.Created_At DESC
    """

    cur.execute(base_query, params)
    rows = cur.fetchall()
    cur.close()

    return jsonify(
        success=True,
        groups=[{
            "Group_Id": r[0],
            "Group_Name": r[1],
            "Faculty_Email": r[2],
            "Created_At": r[3],
            "Is_Active": r[4],
            "Applicant_Count": r[5]
        } for r in rows]
    )

@group_bp.route("/toggle-status/<int:group_id>", methods=["PUT"])
def toggle_group_status(group_id):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE applicant_groups
        SET Is_Active = CASE
            WHEN Is_Active = 1 THEN 0
            ELSE 1
        END
        WHERE group_id = %s
    """, (group_id,))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True, message="Group status updated")

# ==================================================
# GET APPLICANTS OF GROUP - ✅ ONLY ACTIVE STUDENTS
# ==================================================
@group_bp.route("/<int:group_id>/applicants", methods=["GET"])
def get_group_applicants(group_id):
    """
    Returns ONLY active students (Is_Active = 1) for a specific group
    """
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    print(f"\n{'='*70}")
    print(f"🔍 [GROUP_BP] GET APPLICANTS FOR GROUP {group_id}")
    print(f"{'='*70}")
    
    # Get only active students
    cur.execute("""
        SELECT Applicant_Id, Full_Name, Email, Is_Active
        FROM applicants
        WHERE group_id = %s
        ORDER BY Full_Name ASC
    """, (group_id,))
    
    all_rows = cur.fetchall()
    print(f"\n📋 ALL STUDENTS IN GROUP {group_id}:")
    for row in all_rows:
        status = "✅ ACTIVE" if row[3] == 1 else "❌ DISABLED"
        print(f"  {status} - ID: {row[0]}, Name: {row[1]}, Is_Active: {row[3]}")
    
    # Filter for active only
    cur.execute("""
        SELECT Applicant_Id, Full_Name, Email
        FROM applicants
        WHERE group_id = %s
          AND Is_Active = 1
        ORDER BY Full_Name ASC
    """, (group_id,))

    active_rows = cur.fetchall()
    
    print(f"\n✅ RETURNING {len(active_rows)} ACTIVE STUDENTS:")
    for row in active_rows:
        print(f"  - ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
    print(f"{'='*70}\n")
    
    cur.close()

    result = [
        {
            "Applicant_Id": r[0],
            "Full_Name": r[1],
            "Email": r[2]
        } for r in active_rows
    ]
    
    return jsonify(success=True, applicants=result)

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
# DELETE GROUP
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