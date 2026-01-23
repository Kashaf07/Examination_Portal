from flask import Blueprint, request, jsonify, current_app

group_bp = Blueprint("group_bp", __name__)

def get_mysql():
    return current_app.config["MYSQL"]

# CREATE GROUP
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
        return jsonify(success=False, message="Unauthorized"), 403

    cur.execute("""
        INSERT INTO applicant_groups (group_name, Faculty_Email)
        VALUES (%s, %s)
    """, (group_name.strip(), email))

    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)

# GET GROUPS
@group_bp.route("", methods=["GET"])
def get_groups():
    role = request.args.get("role")
    email = request.args.get("email")

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    if role == "Admin":
        cur.execute("""
            SELECT group_id, group_name, Faculty_Email, Created_At
            FROM applicant_groups
            ORDER BY Created_At DESC
        """)
    else:
        cur.execute("""
            SELECT group_id, group_name, Faculty_Email, Created_At
            FROM applicant_groups
            WHERE Faculty_Email=%s
            ORDER BY Created_At DESC
        """, (email,))

    rows = cur.fetchall()
    cur.close()

    return jsonify(success=True, groups=[
        {
            "Group_Id": r[0],
            "Group_Name": r[1],
            "Faculty_Email": r[2],
            "Created_At": r[3]
        } for r in rows
    ])

# GET APPLICANTS BY GROUP
@group_bp.route("/<int:group_id>/applicants", methods=["GET"])
def get_group_applicants(group_id):
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT Applicant_Id, Full_Name, Email, Phone, Gender
        FROM applicants
        WHERE group_id=%s
    """, (group_id,))

    rows = cur.fetchall()
    cur.close()

    return jsonify(success=True, applicants=[
        {
            "Applicant_Id": r[0],
            "Full_Name": r[1],
            "Email": r[2],
            "Phone": r[3],
            "Gender": r[4]
        } for r in rows
    ])
