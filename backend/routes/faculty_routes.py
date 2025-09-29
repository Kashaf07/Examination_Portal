from flask import Blueprint, request, jsonify
import MySQLdb.cursors  # Using flask-mysqldb DictCursor

def create_faculty_routes(mysql):
    faculty_bp = Blueprint("faculty_bp", __name__)

    # -------------------------
    # Faculty Login
    # -------------------------
    @faculty_bp.route("/login", methods=["POST"])
    def faculty_login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM Mst_Faculty WHERE F_Email = %s", (email,))
            faculty = cursor.fetchone()
            cursor.close()

            if not faculty:
                return jsonify({"success": False, "message": "Faculty not found"}), 404

            # If you use plain text passwords (⚠️ insecure but works for now)
            if faculty["F_Password"] == password:
                return jsonify({
                    "success": True,
                    "faculty": {
                        "id": faculty["F_ID"],
                        "name": faculty["F_Name"],
                        "email": faculty["F_Email"]
                    }
                })
            else:
                return jsonify({"success": False, "message": "Invalid password"}), 401

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # -------------------------
    # Faculty Profile
    # -------------------------
    @faculty_bp.route("/profile", methods=["GET"])
    def get_faculty_profile():
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "Email is required"}), 400

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT F_Name FROM Mst_Faculty WHERE F_Email = %s", (email,))
            faculty = cursor.fetchone()
            cursor.close()

            if faculty:
                return jsonify({"success": True, "name": faculty["F_Name"]})
            else:
                return jsonify({"success": False, "message": "Faculty not found"}), 404

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # -------------------------
    # Conducted Exams
    # -------------------------
    @faculty_bp.route("/conducted_exams/<faculty_email>", methods=["GET"])
    def get_conducted_exams(faculty_email):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
               SELECT
    ee.Exam_Id,
    ee.Exam_Name,
    ee.Exam_Date,
    ee.Exam_Time,
    ee.Duration_Minutes,
    ee.Total_Questions,
    ee.Max_Marks,
    IFNULL(assigns.total_applicants, 0) AS total_applicants,
    IFNULL(attempts.attempted_applicants, 0) AS attempted_applicants
FROM
    entrance_exam ee
    LEFT JOIN (
        SELECT Exam_Id, COUNT(*) AS total_applicants
        FROM applicant_exam_assign
        GROUP BY Exam_Id
    ) assigns ON ee.Exam_Id = assigns.Exam_Id
    LEFT JOIN (
        SELECT ep.Exam_Id, COUNT(DISTINCT aa.Applicant_Id) AS attempted_applicants
        FROM exam_paper ep
        JOIN applicant_attempt aa ON ep.Exam_Paper_Id = aa.Exam_Paper_Id
        WHERE aa.Status = 'Submitted'
        GROUP BY ep.Exam_Id
    ) attempts ON ee.Exam_Id = attempts.Exam_Id
WHERE
    ee.Faculty_Email = %s
ORDER BY ee.Exam_Date DESC;



            """
            cursor.execute(query, (faculty_email,))
            exams = cursor.fetchall()
            print("Returned exams:", exams)  # Debug print
            cursor.close()
            return jsonify({"success": True, "exams": exams})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    return faculty_bp