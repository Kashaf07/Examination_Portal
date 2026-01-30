from flask import Blueprint, request, jsonify
import MySQLdb.cursors
from functools import wraps
import jwt
from routes.auth_routes import SECRET_KEY  # Replace with your JWT secret key

def create_faculty_routes(mysql):
    faculty_bp = Blueprint("faculty_bp", __name__)

    # -------------------------
    # JWT Token decorator
    # -------------------------
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if "Authorization" in request.headers:
                auth_header = request.headers["Authorization"]
                token = auth_header.split(" ")[1] if " " in auth_header else auth_header

            if not token:
                return jsonify({"success": False, "message": "Token is missing"}), 401

            try:
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

                # Store user email for all routes
                request.faculty_email = decoded["email"]

                current_user = {
                    "email": decoded["email"],
                    "roles": decoded.get("roles", []),
                    "active_role": decoded.get("active_role")
                }

            except Exception as e:
                return jsonify({"success": False, "message": f"Invalid token: {str(e)}"}), 401

            return f(current_user, *args, **kwargs)
        return decorated

    # -------------------------
    # Faculty Profile
    # -------------------------
    @faculty_bp.route("/profile", methods=["GET"])
    @token_required
    def get_faculty_profile(current_user):
        if "Faculty" not in current_user["roles"]:
            return jsonify({"success": False, "message": "Access denied"}), 403

        email = current_user["email"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT F_ID, F_Name, F_Email FROM Mst_Faculty WHERE F_Email = %s", (email,))
        faculty = cursor.fetchone()
        cursor.close()

        if faculty:
            return jsonify({"success": True, "faculty": faculty})
        else:
            return jsonify({"success": False, "message": "Faculty not found"}), 404


    # -------------------------
    # Conducted Exams by Faculty Email (without token)
    # -------------------------
    @faculty_bp.route("/conducted_exams/<faculty_email>", methods=["GET"])
    def get_conducted_exams_by_email(faculty_email):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
                SELECT 
                    ee.Exam_Id,
                    ee.Exam_Name,
                    ee.Exam_Date,
                    COUNT(DISTINCT aea.Applicant_Id) AS total_applicants,
                    COALESCE(attempts.attempted_applicants, 0) AS attempted_applicants
                FROM Entrance_Exam ee
                LEFT JOIN applicant_exam_assign aea ON ee.Exam_Id = aea.Exam_Id
                LEFT JOIN (
                    SELECT ep.Exam_Id, COUNT(DISTINCT aa.Applicant_Id) AS attempted_applicants
                    FROM exam_paper ep
                    JOIN applicant_attempt aa ON ep.Exam_Paper_Id = aa.Exam_Paper_Id
                    WHERE aa.Status = 'Submitted'
                    GROUP BY ep.Exam_Id
                ) AS attempts ON ee.Exam_Id = attempts.Exam_Id
                WHERE ee.faculty_email = %s
                  AND TIMESTAMP(ee.Exam_Date, ee.Exam_Time) + INTERVAL ee.Duration_Minutes MINUTE <= NOW()
                GROUP BY ee.Exam_Id, ee.Exam_Name, ee.Exam_Date, attempts.attempted_applicants
                ORDER BY ee.Exam_Date DESC
            """
            cursor.execute(query, (faculty_email,))
            exams = cursor.fetchall()
            cursor.close()

            return jsonify({"success": True, "exams": exams})

        except Exception as e:
            print("Error fetching conducted exams:", e)
            return jsonify({"success": False, "message": str(e)}), 500
    
    
    
    # -------------------------
    # Conducted Exams with Applicant Attempts
    # -------------------------
    @faculty_bp.route("/conducted_exams", methods=["GET"])
    @token_required
    def get_conducted_exams():
        faculty_email = request.faculty_email
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
                SELECT 
                    ee.Exam_Id,
                    ee.Exam_Name,
                    ee.Exam_Date,
                    COUNT(DISTINCT aea.Applicant_Id) AS total_applicants,
                    COALESCE(attempts.attempted_applicants, 0) AS attempted_applicants
                FROM Entrance_Exam ee
                LEFT JOIN applicant_exam_assign aea ON ee.Exam_Id = aea.Exam_Id
                LEFT JOIN (
                    SELECT ep.Exam_Id, COUNT(DISTINCT aa.Applicant_Id) AS attempted_applicants
                    FROM exam_paper ep
                    JOIN applicant_attempt aa ON ep.Exam_Paper_Id = aa.Exam_Paper_Id
                    WHERE aa.Status = 'Submitted'
                    GROUP BY ep.Exam_Id
                ) AS attempts ON ee.Exam_Id = attempts.Exam_Id
                WHERE ee.faculty_email = %s
                GROUP BY ee.Exam_Id, ee.Exam_Name, ee.Exam_Date, attempts.attempted_applicants
                ORDER BY ee.Exam_Date DESC
            """
            cursor.execute(query, (faculty_email,))
            exams = cursor.fetchall()
            cursor.close()

            return jsonify({"success": True, "exams": exams})

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # -------------------------
    # Exam Applicants Statistics
    # -------------------------
    @faculty_bp.route("/exam_applicants_stats", methods=["GET"])
    @token_required
    def get_exam_applicants_stats():
        faculty_email = request.faculty_email
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
                SELECT 
                    ee.Exam_Id,
                    ee.Exam_Name,
                    COUNT(DISTINCT aea.Applicant_Id) AS total_applicants,
                    COALESCE(attempts.attempted_applicants, 0) AS attempted_applicants
                FROM Entrance_Exam ee
                LEFT JOIN applicant_exam_assign aea ON ee.Exam_Id = aea.Exam_Id
                LEFT JOIN (
                    SELECT ep.Exam_Id, COUNT(DISTINCT aa.Applicant_Id) AS attempted_applicants
                    FROM exam_paper ep
                    JOIN applicant_attempt aa ON ep.Exam_Paper_Id = aa.Exam_Paper_Id
                    WHERE aa.Status = 'Submitted'
                    GROUP BY ep.Exam_Id
                ) AS attempts ON ee.Exam_Id = attempts.Exam_Id
                WHERE ee.faculty_email = %s
                GROUP BY ee.Exam_Id, ee.Exam_Name, attempts.attempted_applicants
                ORDER BY ee.Exam_Name
            """
            cursor.execute(query, (faculty_email,))
            stats = cursor.fetchall()
            cursor.close()

            return jsonify({"success": True, "stats": stats})

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
        
    # -------------------------
    # DELETE EXAM (FACULTY)
    # -------------------------
    @faculty_bp.route("/exam/delete/<int:exam_id>", methods=["DELETE"])
    @token_required
    def delete_exam_faculty(current_user, exam_id):
        try:
            faculty_email = current_user["email"]
            cursor = mysql.connection.cursor()

            # 🔐 1️⃣ Verify exam belongs to this faculty
            cursor.execute("SELECT Exam_Id FROM Entrance_Exam WHERE Exam_Id = %s AND faculty_email = %s",(exam_id, faculty_email))
            exam = cursor.fetchone()

            if not exam:
                cursor.close()
                return jsonify({
                    "success": False,
                    "message": "Unauthorized or exam not found"
                }), 403

            # 🧹 2️⃣ DELETE QUESTION BANK FIRST (FK FIX)
            cursor.execute("DELETE FROM entrance_question_bank WHERE Exam_Id = %s",(exam_id,))

            # 3️⃣ Get exam paper IDs
            cursor.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s",(exam_id,))
            paper_ids = [row[0] for row in cursor.fetchall()]

            if paper_ids:
                # 4️⃣ Get attempt IDs
                cursor.execute(f""" SELECT Attempt_Id FROM applicant_attempt WHERE Exam_Paper_Id IN ({','.join(['%s'] * len(paper_ids))})""",paper_ids)
                attempt_ids = [row[0] for row in cursor.fetchall()]

                # 5️⃣ Delete answers
                if attempt_ids:
                    cursor.execute(f""" DELETE FROM applicant_answers WHERE Attempt_Id IN ({','.join(['%s'] * len(attempt_ids))})""",attempt_ids)

                # 6️⃣ Delete attempts
                cursor.execute(f"""DELETE FROM applicant_attempt WHERE Exam_Paper_Id IN ({','.join(['%s'] * len(paper_ids))})""",paper_ids)

            # 7️⃣ Delete applicant-exam assignments
            cursor.execute("DELETE FROM applicant_exam_assign WHERE Exam_Id = %s",(exam_id,))

            # 8️⃣ Delete exam papers
            cursor.execute("DELETE FROM exam_paper WHERE Exam_Id = %s",(exam_id,))

            # 9️⃣ Finally delete exam
            cursor.execute("DELETE FROM Entrance_Exam WHERE Exam_Id = %s",(exam_id,))

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "success": True,
                "message": "Exam deleted successfully"
            }), 200

        except Exception as e:
            mysql.connection.rollback()
            print("🔥 Faculty exam delete failed:", e)
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    return faculty_bp
