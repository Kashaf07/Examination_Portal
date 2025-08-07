from flask import Blueprint, request, jsonify

def create_faculty_routes(mysql):
    faculty_bp = Blueprint('faculty_bp', __name__)

    @faculty_bp.route('/api/faculty/profile', methods=['GET'])
    def get_faculty_profile():
        email = request.args.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT F_Name FROM Mst_Faculty WHERE F_Email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return jsonify({'status': 'success', 'name': result[0]}), 200
            else:
                return jsonify({'status': 'fail', 'error': 'Faculty not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'error': str(e)}), 500
        finally:
            cursor.close()
            
    @faculty_bp.route('/api/faculty/view_responses/<int:exam_id>', methods=['GET'])
    def view_responses(exam_id):
        try:
            cursor = mysql.connection.cursor(dictionary=True)

            query = """
            SELECT 
                aa.Attempt_Id,
                ap.Full_Name,
                ap.Email,
                aa.Start_Time,
                aa.End_Time,
                aa.Status
            FROM applicant_attempt aa
            JOIN applicants ap ON aa.Applicant_Id = ap.Applicant_Id
            WHERE aa.Exam_Paper_Id = %s
            """
            cursor.execute(query, (exam_id,))
            data = cursor.fetchall()
            return jsonify({'success': True, 'responses': data})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        finally:
            cursor.close()
            
    @faculty_bp.route('/api/faculty/conducted_exams/<faculty_email>', methods=['GET'])
    def get_conducted_exams(faculty_email):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            
            # Step 1: Get Faculty_Id from email
            cursor.execute("SELECT Faculty_Id FROM mst_faculty WHERE F_Email = %s", (faculty_email,))
            faculty_row = cursor.fetchone()

            if not faculty_row:
                return jsonify({'success': False, 'message': 'Faculty not found'}), 404

            faculty_id = faculty_row['Faculty_Id']

            query = """
            SELECT 
                ep.Exam_Paper_Id,
                ep.Exam_Title,
                ep.Exam_Date,
                COUNT(DISTINCT aa.Applicant_Id) AS Students_Attended
            FROM exam_paper ep
            LEFT JOIN applicant_attempt aa ON ep.Exam_Paper_Id = aa.Exam_Paper_Id
            WHERE ep.Faculty_Email = %s
            GROUP BY ep.Exam_Paper_Id
            ORDER BY ep.Exam_Date DESC
            """

            cursor.execute(query, (faculty_email,))
            exams = cursor.fetchall()
            return jsonify({'success': True, 'exams': exams}), 200

        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            cursor.close()



    return faculty_bp
