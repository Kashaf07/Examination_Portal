from flask import Blueprint, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import pytz

def create_admin_routes(mysql):
    admin_bp = Blueprint('admin_routes', __name__)
    def convert_to_ist(dt):
        if dt is None:
            return None
        utc = pytz.utc
        ist = pytz.timezone('Asia/Kolkata')
        utc_dt = utc.localize(dt)
        ist_dt = utc_dt.astimezone(ist)
        return ist_dt.strftime('%Y-%m-%d %H:%M:%S')

    # ID Management Route
    @admin_bp.route('/reorganize-ids', methods=['POST'])
    def reorganize_ids():
        try:
            cursor = mysql.connection.cursor()
        
            # Execute the comprehensive reorganization script
            with open('scripts/reorganize_ids_complete.sql', 'r') as file:
                sql_script = file.read()
        
            # Split and execute each statement
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
        
            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "All IDs reorganized successfully in perfect sequential order (1,2,3,4...)", "status": "complete"}), 200
        except Exception as e:
            print("Error reorganizing IDs:", e)
            mysql.connection.rollback()
            return jsonify({"error": f"Unable to reorganize IDs: {str(e)}"}), 500

    # ID Gap Detection Route
    @admin_bp.route('/check-id-gaps', methods=['GET'])
    def check_id_gaps():
        try:
            cursor = mysql.connection.cursor()
            gaps_report = {}
        
            # Check each table for gaps including all discovered tables
            tables = [
                ('mst_school', 'School_Id'),
                ('mst_faculty', 'Faculty_Id'),
                ('applicants', 'Applicant_Id'),
                ('applicant_attempt', 'Attempt_Id'),
                ('mst_admin', 'Admin_ID'),
                ('login_log', 'Log_ID')
            ]
        
            # Check if additional tables exist and add them
            cursor.execute("SHOW TABLES LIKE 'auto_grading'")
            if cursor.fetchone():
                tables.append(('auto_grading', 'Grading_Id'))
            
            cursor.execute("SHOW TABLES LIKE 'applicant_exam_assign'")
            if cursor.fetchone():
                tables.append(('applicant_exam_assign', 'Assign_ID'))
            
            cursor.execute("SHOW TABLES LIKE 'applicant_answers'")
            if cursor.fetchone():
                # Note: applicant_answers doesn't have its own ID, it references Attempt_Id
                pass
        
            for table_name, id_column in tables:
                try:
                    cursor.execute(f"""
                        SELECT 
                            COUNT(*) as total_records,
                            COALESCE(MIN({id_column}), 0) as min_id,
                            COALESCE(MAX({id_column}), 0) as max_id,
                            CASE WHEN COUNT(*) = 0 THEN 0 
                                 ELSE (COALESCE(MAX({id_column}), 0) - COALESCE(MIN({id_column}), 0) + 1) 
                            END as expected_count,
                            CASE WHEN COUNT(*) = 0 THEN 0 
                                 ELSE ((COALESCE(MAX({id_column}), 0) - COALESCE(MIN({id_column}), 0) + 1) - COUNT(*)) 
                            END as gaps
                        FROM {table_name}
                    """)
                    result = cursor.fetchone()
                
                    if result:
                        gaps_report[table_name] = {
                            'total_records': result[0],
                            'min_id': result[1],
                            'max_id': result[2],
                            'expected_count': result[3],
                            'gaps': result[4],
                            'has_gaps': result[4] > 0,
                            'status': 'Perfect Order' if result[4] == 0 and result[0] > 0 else ('Empty' if result[0] == 0 else 'Has Gaps')
                        }
                except Exception as table_error:
                    gaps_report[table_name] = {
                        'error': f"Unable to check table: {str(table_error)}"
                    }
        
            cursor.close()
            return jsonify(gaps_report), 200
        except Exception as e:
            print("Error checking ID gaps:", e)
            return jsonify({"error": "Unable to check ID gaps"}), 500

    # Faculty Routes
    @admin_bp.route('/faculty', methods=['GET'])
    def get_faculty():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT 
                f.Faculty_Id,
                f.F_Name,
                f.F_Email,
                f.School_Id,
                f.Designation_Id,
                d.Designation_Name,
                f.Role_Id,
                f.Is_Active
            FROM mst_faculty f
            LEFT JOIN mst_designation d ON f.Designation_Id = d.Designation_Id
            ORDER BY f.Is_Active DESC, f.F_Name ASC
        """)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        return jsonify(result), 200


    @admin_bp.route('/faculty', methods=['POST'])
    def add_faculty():
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()

            # 1️⃣ Duplicate Email Check
            cursor.execute("SELECT COUNT(*) FROM mst_faculty WHERE F_Email = %s", (data['F_Email'],))
            if cursor.fetchone()[0] > 0:
                cursor.close()
                return jsonify({"error": "A faculty member with this email already exists."}), 400

            # 2️⃣ Auto-map Role_Id from Designation_Id
            cursor.execute("SELECT Role_Id FROM mst_designation WHERE Designation_Id = %s", 
                        (data['Designation_Id'],))
            role_row = cursor.fetchone()

            if not role_row:
                cursor.close()
                return jsonify({"error": "Invalid Designation_Id"}), 400

            role_id = role_row[0]

            # 3️⃣ Insert Faculty using new structure
            cursor.execute("""
                INSERT INTO mst_faculty 
                (F_Name, F_Email, School_Id, Designation_Id, Role_Id, Password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ( data['F_Name'], data['F_Email'], data['School_Id'], data['Designation_Id'], role_id, data['Password']))

            mysql.connection.commit()
            faculty_id = cursor.lastrowid
            cursor.close()

            return jsonify({
                "message": "Faculty added successfully",
                "Faculty_Id": faculty_id
            }), 201

        except Exception as e:
            print("Error adding faculty:", e)
            return jsonify({"error": "Unable to add faculty"}), 500

    @admin_bp.route('/faculty/<int:faculty_id>', methods=['PUT'])
    def update_faculty(faculty_id):
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()

            # 1️⃣ Get Role_Id automatically
            cursor.execute("SELECT Role_Id FROM mst_designation WHERE Designation_Id = %s",
                        (data['Designation_Id'],))
            role_row = cursor.fetchone()

            if not role_row:
                cursor.close()
                return jsonify({"error": "Invalid Designation_Id"}), 400

            role_id = role_row[0]

            # 2️⃣ Update record
            cursor.execute(""" UPDATE mst_faculty SET F_Name = %s, F_Email = %s, School_Id = %s, 
                           Designation_Id = %s, Role_Id = %s WHERE Faculty_Id = %s """, 
                           ( data['F_Name'], data['F_Email'], data['School_Id'], data['Designation_Id'], role_id, faculty_id ))

            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "Faculty updated successfully"}), 200

        except Exception as e:
            print("Error updating faculty:", e)
            return jsonify({"error": "Unable to update faculty"}), 500


    @admin_bp.route('/faculty/toggle-status/<int:faculty_id>', methods=['PUT'])
    def toggle_faculty_status(faculty_id):
        try:
            cursor = mysql.connection.cursor()

            cursor.execute("""
                UPDATE mst_faculty
                SET Is_Active = CASE 
                    WHEN Is_Active = 1 THEN 0
                    ELSE 1
                END
                WHERE Faculty_Id = %s
            """, (faculty_id,))

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "success": True,
                "message": "Faculty status updated successfully"
            }), 200

        except Exception as e:
            mysql.connection.rollback()
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    # ----------------------------------
    # GET ALL GROUPS
    # ----------------------------------
    @admin_bp.route('/groups', methods=['GET'])
    def get_groups():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT group_id, group_name FROM applicant_groups ORDER BY group_id DESC")
        rows = cursor.fetchall()
        cursor.close()

        return jsonify([
            {'group_id': r[0], 'group_name': r[1]}
            for r in rows
        ]), 200

    # ----------------------------------
    # ADD GROUP
    # ----------------------------------
    @admin_bp.route('/groups/add', methods=['POST'])
    def add_group():
        data = request.json
        group_name = data.get('group_name')

        if not group_name:
            return jsonify({'error': 'Group name required'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO applicant_groups (group_name) VALUES (%s)",
            (group_name,)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Group added successfully'}), 201

    # ----------------------------------
    # UPDATE GROUP
    # ----------------------------------
    @admin_bp.route('/groups/<int:group_id>', methods=['PUT'])
    def update_group(group_id):
        data = request.json
        group_name = data.get('group_name')

        if not group_name:
            return jsonify({'error': 'Group name required'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE applicant_groups SET group_name=%s WHERE group_id=%s",
            (group_name, group_id)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Group updated successfully'}), 200

    # ----------------------------------
    # DELETE GROUP
    # ----------------------------------
    @admin_bp.route('/groups/<int:group_id>', methods=['DELETE'])
    def delete_group(group_id):
        cursor = mysql.connection.cursor()

        # Optional safety: check applicants exist
        cursor.execute("SELECT COUNT(*) FROM applicants WHERE group_id=%s", (group_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.close()
            return jsonify({
                'error': 'Cannot delete group. Applicants exist.'
            }), 400

        cursor.execute("DELETE FROM applicant_groups WHERE group_id=%s", (group_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Group deleted successfully'}), 200

    # ----------------------------------
    # VIEW APPLICANTS OF A GROUP
    # ----------------------------------
    @admin_bp.route('/groups/<int:group_id>/applicants', methods=['GET'])
    def get_group_applicants(group_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT Applicant_Id, Full_Name, Email
            FROM applicants
            WHERE group_id=%s
            ORDER BY Applicant_Id DESC
        """, (group_id,))
        rows = cursor.fetchall()
        cursor.close()

        return jsonify([
            {
                'Applicant_Id': r[0],
                'Full_Name': r[1],
                'Email': r[2]
            }
            for r in rows
        ]), 200

    # Schools Routes
    @admin_bp.route('/schools', methods=['GET'])
    def get_schools():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT School_Id, School_Name, School_Short, Is_Active FROM mst_school ORDER BY Is_Active DESC, School_Name ASC")
            schools = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in schools]
            cursor.close()
            return jsonify(result), 200
        except Exception as e:
            print("Error fetching schools:", e)
            return jsonify({"error": "Unable to fetch schools"}), 500

    @admin_bp.route('/schools', methods=['POST'])
    def add_school():
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()
            
            # --- START CHANGE: Check for duplicate School_Name or School_Short ---
            cursor.execute("SELECT School_Name, School_Short FROM mst_school WHERE School_Name = %s OR School_Short = %s", 
                           (data['School_Name'], data['School_Short']))
            existing = cursor.fetchone()
            if existing:
                cursor.close()
                if existing[0] == data['School_Name']:
                    return jsonify({"error": "A school with this name already exists."}), 400
                if existing[1] == data['School_Short']:
                    return jsonify({"error": "A school with this short name already exists."}), 400
            # --- END CHANGE ---
            
            cursor.execute("""
                INSERT INTO mst_school (School_Name, School_Short)
                VALUES (%s, %s)
            """, (data['School_Name'], data['School_Short']))
            
            mysql.connection.commit()
            school_id = cursor.lastrowid
            cursor.close()
            return jsonify({"message": "School added successfully", "School_Id": school_id}), 201
        except Exception as e:
            print("Error adding school:", e)
            # --- START CHANGE: Catch DB-level duplicate errors ---
            if 'Duplicate entry' in str(e):
                if 'School_Name' in str(e):
                     return jsonify({"error": "A school with this name already exists."}), 400
                if 'School_Short' in str(e):
                     return jsonify({"error": "A school with this short name already exists."}), 400
                return jsonify({"error": "A school with this name or short name already exists."}), 400
            # --- END CHANGE ---            
            return jsonify({"error": "Unable to add school"}), 500

    @admin_bp.route('/schools/<int:school_id>', methods=['PUT'])
    def update_school(school_id):
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()
            
            cursor.execute("""
                UPDATE mst_school 
                SET School_Name = %s, School_Short = %s
                WHERE School_Id = %s
            """, (data['School_Name'], data['School_Short'], school_id))
            
            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "School updated successfully"}), 200
        except Exception as e:
            print("Error updating school:", e)
            return jsonify({"error": "Unable to update school"}), 500

    @admin_bp.route('/schools/toggle-status/<int:school_id>', methods=['PUT'])
    def toggle_school_status(school_id):
        try:
            cursor = mysql.connection.cursor()

            cursor.execute("""
                UPDATE mst_school
                SET Is_Active = CASE
                    WHEN Is_Active = 1 THEN 0
                    ELSE 1
                END
                WHERE School_Id = %s
            """, (school_id,))

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "success": True,
                "message": "School status updated successfully"
            }), 200

        except Exception as e:
            mysql.connection.rollback()
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    # Applicants Routes
    @admin_bp.route('/applicants', methods=['GET'])
    def get_applicants():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT Applicant_Id, Full_Name, Email, Phone, DOB, Gender, Address, Registration_Date
                FROM applicants 
                ORDER BY Applicant_Id
            """)
            applicants = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in applicants]
            cursor.close()
            return jsonify(result), 200
        except Exception as e:
            print("Error fetching applicants:", e)
            return jsonify({"error": "Unable to fetch applicants"}), 500

    @admin_bp.route('/applicants/<int:applicant_id>', methods=['DELETE'])
    def delete_applicant(applicant_id):
        try:
            cursor = mysql.connection.cursor()
        
            # Get all attempt IDs for this applicant
            cursor.execute("SELECT Attempt_Id FROM applicant_attempt WHERE Applicant_Id = %s", (applicant_id,))
            attempt_ids = [row[0] for row in cursor.fetchall()]
        
            # Delete from applicant_answers table first
            answers_deleted = 0
            if attempt_ids:
                for attempt_id in attempt_ids:
                    cursor.execute("SELECT COUNT(*) FROM applicant_answers WHERE Attempt_Id = %s", (attempt_id,))
                    answer_count = cursor.fetchone()[0]
                    if answer_count > 0:
                        cursor.execute("DELETE FROM applicant_answers WHERE Attempt_Id = %s", (attempt_id,))
                        answers_deleted += answer_count
        
            # Delete related records
            cursor.execute("SELECT COUNT(*) FROM applicant_attempt WHERE Applicant_Id = %s", (applicant_id,))
            attempt_count = cursor.fetchone()[0]
        
            if attempt_count > 0:
                cursor.execute("DELETE FROM applicant_attempt WHERE Applicant_Id = %s", (applicant_id,))
                print(f"Deleted {attempt_count} exam attempts for applicant {applicant_id}")
        
            # Delete from auto_grading table (if exists)
            try:
                cursor.execute("SELECT COUNT(*) FROM auto_grading WHERE Attempt_Id IN (%s)" % ','.join(['%s'] * len(attempt_ids)) if attempt_ids else "SELECT 0", attempt_ids if attempt_ids else [])
                grading_count = cursor.fetchone()[0] if attempt_ids else 0
                if grading_count > 0:
                    cursor.execute("DELETE FROM auto_grading WHERE Attempt_Id IN (%s)" % ','.join(['%s'] * len(attempt_ids)), attempt_ids)
            except Exception as e:
                print(f"Note: auto_grading table handling: {e}")
        
            # Delete from applicant_exam_assign table (if exists)
            try:
                cursor.execute("SELECT COUNT(*) FROM applicant_exam_assign WHERE Applicant_Id = %s", (applicant_id,))
                assign_count = cursor.fetchone()[0]
                if assign_count > 0:
                    cursor.execute("DELETE FROM applicant_exam_assign WHERE Applicant_Id = %s", (applicant_id,))
            except Exception as e:
                print(f"Note: applicant_exam_assign table handling: {e}")
        
            # Delete from login_log table by User_Email
            cursor.execute("SELECT Email FROM applicants WHERE Applicant_Id = %s", (applicant_id,))
            row = cursor.fetchone()
            applicant_email = row[0] if row else None

            if applicant_email:
                cursor.execute("SELECT COUNT(*) FROM login_log WHERE User_Email = %s", (applicant_email,))
                log_count = cursor.fetchone()[0]
                if log_count > 0:
                    cursor.execute("DELETE FROM login_log WHERE User_Email = %s", (applicant_email,))
                    print(f"Deleted {log_count} login logs for applicant {applicant_id}")
            else:
                log_count = 0
        
            # Finally delete the applicant
            cursor.execute("DELETE FROM applicants WHERE Applicant_Id = %s", (applicant_id,))
        
            mysql.connection.commit()
            cursor.close()
        
            message = f"Applicant deleted successfully"
            details = []
            if answers_deleted > 0:
                details.append(f"{answers_deleted} exam answers")
            if attempt_count > 0:
                details.append(f"{attempt_count} exam attempts")
            if log_count > 0:
                details.append(f"{log_count} login logs")
        
            if details:
                message += f" (also removed {', '.join(details)})"
        
            return jsonify({"message": message}), 200
        except Exception as e:
            print("Error deleting applicant:", e)
            mysql.connection.rollback()
            return jsonify({"error": f"Unable to delete applicant: {str(e)}"}), 500

    # Exam Attempts Routes
    @admin_bp.route('/attempts', methods=['GET'])
    def get_attempts():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT Attempt_Id, Applicant_Id, Exam_Paper_Id, Start_Time, End_Time, Status,
                       Security_Violations, Screen_Log, Fullscreen_Mode, Browser_Info,
                       Submission_Type, Termination_Reason, Escape_Key_Violations,
                       Lockdown_Mode, Fullscreen_Exit_Attempts, Fullscreen_Lock_Mode,
                       Keyboard_Violations
                FROM applicant_attempt 
                ORDER BY Attempt_Id
            """)
            attempts = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in attempts]
            cursor.close()
            return jsonify(result), 200
        except Exception as e:
            print("Error fetching attempts:", e)
            return jsonify({"error": "Unable to fetch attempts"}), 500

    @admin_bp.route('/attempts', methods=['POST'])
    def add_attempt():
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()
            
            # Check if applicant exists
            cursor.execute("SELECT COUNT(*) FROM applicants WHERE Applicant_Id = %s", (data['Applicant_Id'],))
            if cursor.fetchone()[0] == 0:
                cursor.close()
                return jsonify({"error": "Applicant not found"}), 400
            
            cursor.execute("""
                INSERT INTO applicant_attempt (
                    Applicant_Id, Exam_Paper_Id, Status, Security_Violations,
                    Screen_Log, Fullscreen_Mode, Browser_Info, Submission_Type,
                    Termination_Reason, Escape_Key_Violations, Lockdown_Mode,
                    Fullscreen_Exit_Attempts, Fullscreen_Lock_Mode, Keyboard_Violations
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['Applicant_Id'], data['Exam_Paper_Id'], data['Status'],
                data['Security_Violations'], data.get('Screen_Log', ''),
                data.get('Fullscreen_Mode', 1), data.get('Browser_Info', ''),
                data['Submission_Type'], data.get('Termination_Reason', ''),
                data.get('Escape_Key_Violations', 0), data.get('Lockdown_Mode', 1),
                data.get('Fullscreen_Exit_Attempts', 0), data.get('Fullscreen_Lock_Mode', 1),
                data.get('Keyboard_Violations', 0)
            ))
            
            mysql.connection.commit()
            attempt_id = cursor.lastrowid
            cursor.close()
            return jsonify({"message": "Attempt added successfully", "Attempt_Id": attempt_id}), 201
        except Exception as e:
            print("Error adding attempt:", e)
            return jsonify({"error": f"Unable to add attempt: {str(e)}"}), 500

    @admin_bp.route('/attempts/<int:attempt_id>', methods=['PUT'])
    def update_attempt(attempt_id):
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()
            
            # Check if applicant exists
            cursor.execute("SELECT COUNT(*) FROM applicants WHERE Applicant_Id = %s", (data['Applicant_Id'],))
            if cursor.fetchone()[0] == 0:
                cursor.close()
                return jsonify({"error": "Applicant not found"}), 400
            
            cursor.execute("""
                UPDATE applicant_attempt 
                SET Applicant_Id = %s, Exam_Paper_Id = %s, Status = %s,
                    Security_Violations = %s, Submission_Type = %s,
                    Termination_Reason = %s, Escape_Key_Violations = %s,
                    Fullscreen_Exit_Attempts = %s, Keyboard_Violations = %s
                WHERE Attempt_Id = %s
            """, (
                data['Applicant_Id'], data['Exam_Paper_Id'], data['Status'],
                data['Security_Violations'], data['Submission_Type'],
                data.get('Termination_Reason', ''), data.get('Escape_Key_Violations', 0),
                data.get('Fullscreen_Exit_Attempts', 0), data.get('Keyboard_Violations', 0),
                attempt_id
            ))
            
            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "Attempt updated successfully"}), 200
        except Exception as e:
            print("Error updating attempt:", e)
            return jsonify({"error": f"Unable to update attempt: {str(e)}"}), 500

    @admin_bp.route('/attempts/<int:attempt_id>', methods=['DELETE'])
    def delete_attempt(attempt_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM applicant_attempt WHERE Attempt_Id = %s", (attempt_id,))
            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "Attempt deleted successfully"}), 200
        except Exception as e:
            print("Error deleting attempt:", e)
            return jsonify({"error": f"Unable to delete attempt: {str(e)}"}), 500

    # Admin Management Routes
    @admin_bp.route('/admins', methods=['GET'])
    def get_admins():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT Admin_ID, Name, Email FROM mst_admin ORDER BY Admin_ID")
            admins = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in admins]
            cursor.close()
            return jsonify(result), 200
        except Exception as e:
            print("Error fetching admins:", e)
            return jsonify({"error": "Unable to fetch admins"}), 500

    # ✅ CORRECT - Add it HERE with 4 spaces indentation
    @admin_bp.route('/check-faculty-role/<email>', methods=['GET'])
    def check_faculty_role(email):
        """Check if admin email exists in faculty table"""
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT Faculty_Id FROM mst_faculty WHERE F_Email = %s", (email,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return jsonify({
                    "success": True,
                    "isFaculty": True,
                    "message": "Admin is also assigned as faculty"
                }), 200
            else:
                return jsonify({
                    "success": True,
                    "isFaculty": False,
                    "message": "Admin is not assigned as faculty"
                }), 200
                
        except Exception as e:
            print("Error checking faculty role:", e)
            return jsonify({
                "success": False,
                "isFaculty": False,
                "message": "Error checking faculty role"
            }), 500
            
            
    @admin_bp.route('/admins', methods=['POST'])
    def add_admin():
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()
            
            # Check if email already exists (This was already correct)
            cursor.execute("SELECT COUNT(*) FROM mst_admin WHERE Email = %s", (data['Email'],))
            if cursor.fetchone()[0] > 0:
                cursor.close()
                return jsonify({"error": "Email already exists"}), 400
            
            cursor.execute("""
                INSERT INTO mst_admin (Name, Email, Password)
                VALUES (%s, %s, %s)
            """, (data['Name'], data['Email'], data['Password']))
            
            mysql.connection.commit()
            admin_id = cursor.lastrowid
            cursor.close()
            return jsonify({"message": "Admin added successfully", "Admin_ID": admin_id}), 201
        except Exception as e:
            print("Error adding admin:", e)
            return jsonify({"error": f"Unable to add admin: {str(e)}"}), 500

    @admin_bp.route('/admins/<int:admin_id>', methods=['PUT'])
    def update_admin(admin_id):
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor()
            
            # Check if email already exists for other admins
            cursor.execute("SELECT COUNT(*) FROM mst_admin WHERE Email = %s AND Admin_ID != %s", (data['Email'], admin_id))
            if cursor.fetchone()[0] > 0:
                cursor.close()
                return jsonify({"error": "Email already exists"}), 400
            
            cursor.execute("""
                UPDATE mst_admin 
                SET Name = %s, Email = %s
                WHERE Admin_ID = %s
            """, (data['Name'], data['Email'], admin_id))
            
            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "Admin updated successfully"}), 200
        except Exception as e:
            print("Error updating admin:", e)
            return jsonify({"error": f"Unable to update admin: {str(e)}"}), 500

    @admin_bp.route('/admins/<int:admin_id>', methods=['DELETE'])
    def delete_admin(admin_id):
        try:
            cursor = mysql.connection.cursor()
            
            # Check if this is the last admin
            cursor.execute("SELECT COUNT(*) FROM mst_admin")
            admin_count = cursor.fetchone()[0]
            
            if admin_count <= 1:
                cursor.close()
                return jsonify({"error": "Cannot delete the last admin account"}), 400
            
            cursor.execute("DELETE FROM mst_admin WHERE Admin_ID = %s", (admin_id,))
            mysql.connection.commit()
            cursor.close()
            return jsonify({"message": "Admin deleted successfully"}), 200
        except Exception as e:
            print("Error deleting admin:", e)
            return jsonify({"error": f"Unable to delete admin: {str(e)}"}), 500

    # Login Logs Routes
    @admin_bp.route('/logs', methods=['GET'])
    def get_logs():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT l.Log_ID,l.User_Email,l.Role,l.Login_Time,l.Logout_Time,
                    -- Get name based on role
                    CASE 
                        WHEN l.Role = 'Admin' THEN (SELECT Name FROM mst_admin WHERE Email = l.User_Email LIMIT 1)
                        WHEN l.Role = 'Faculty' THEN (SELECT F_Name FROM mst_faculty WHERE F_Email = l.User_Email LIMIT 1)
                        WHEN l.Role = 'Student' THEN (SELECT Full_Name FROM applicants WHERE Email = l.User_Email LIMIT 1)
                        ELSE 'Unknown'
                    END AS User_Name
                FROM login_log l
                ORDER BY l.Log_ID DESC
            """)
            
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]

            cursor.close()
            return jsonify(result), 200

        except Exception as e:
            print("Error fetching logs:", e)
            return jsonify({"error": "Unable to fetch logs"}), 500

    # ------------------- USER HISTORY -------------------
    @admin_bp.route('/logs/history/<email>', methods=['GET'])
    def get_user_log_history(email):
        try:
            cursor = mysql.connection.cursor()

            cursor.execute("""
                SELECT 
                    Log_ID,
                    User_Email,
                    Role,
                    Login_Time,
                    Logout_Time
                FROM login_log
                WHERE User_Email = %s
                ORDER BY Log_ID DESC
            """, (email,))

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            result = []
            for row in rows:
                item = dict(zip(columns, row))

                # format datetime
                if item.get("Login_Time"):
                    item["Login_Time"] = (
                        item["Login_Time"].strftime('%Y-%m-%d %H:%M:%S')
                        if hasattr(item["Login_Time"], "strftime")
                        else str(item["Login_Time"])
                    )

                if item.get("Logout_Time"):
                    item["Logout_Time"] = (
                        item["Logout_Time"].strftime('%Y-%m-%d %H:%M:%S')
                        if hasattr(item["Logout_Time"], "strftime")
                        else str(item["Logout_Time"])
                    )

                result.append(item)

            cursor.close()
            return jsonify(result), 200

        except Exception as e:
            print("Error fetching user history:", e)
            return jsonify({"error": "Unable to fetch user history"}), 500

    @admin_bp.route('/logout', methods=['POST'])
    def update_logout():
        try:
            data = request.get_json()
            email = data.get("email")

            cursor = mysql.connection.cursor()

            # ✔ FIXED VERSION
            cursor.execute("""
                UPDATE login_log
                SET Logout_Time = NOW()
                WHERE Log_ID = (
                    SELECT Log_ID FROM (
                        SELECT Log_ID
                        FROM login_log
                        WHERE User_Email = %s AND Logout_Time IS NULL
                        ORDER BY Log_ID DESC
                        LIMIT 1
                    ) AS recent
                )
            """, (email,))

            mysql.connection.commit()
            print("Logout updated for:", email, "Rows:", cursor.rowcount)

            cursor.close()
            return jsonify({"message": "Logout time updated"}), 200

        except Exception as e:
            print("Logout error:", e)
            return jsonify({"error": "Unable to update logout"}), 500

    # Bulk delete operations
    @admin_bp.route('/applicants/bulk-delete', methods=['POST'])
    def bulk_delete_applicants():
        try:
            data = request.get_json()
            applicant_ids = data.get('applicant_ids', [])
        
            if not applicant_ids:
                return jsonify({"error": "No applicant IDs provided"}), 400
        
            cursor = mysql.connection.cursor()
            deleted_count = 0
            errors = []
            total_answers_deleted = 0
            total_attempts_deleted = 0
            total_logs_deleted = 0
        
            for applicant_id in applicant_ids:
                try:
                    # Get all attempt IDs for this applicant
                    cursor.execute("SELECT Attempt_Id FROM applicant_attempt WHERE Applicant_Id = %s", (applicant_id,))
                    attempt_ids = [row[0] for row in cursor.fetchall()]
                
                    # Delete from applicant_answers first
                    if attempt_ids:
                        for attempt_id in attempt_ids:
                            cursor.execute("SELECT COUNT(*) FROM applicant_answers WHERE Attempt_Id = %s", (attempt_id,))
                            answer_count = cursor.fetchone()[0]
                            if answer_count > 0:
                                cursor.execute("DELETE FROM applicant_answers WHERE Attempt_Id = %s", (attempt_id,))
                                total_answers_deleted += answer_count
                
                    # Delete related records
                    cursor.execute("SELECT COUNT(*) FROM applicant_attempt WHERE Applicant_Id = %s", (applicant_id,))
                    attempt_count = cursor.fetchone()[0]
                    if attempt_count > 0:
                        cursor.execute("DELETE FROM applicant_attempt WHERE Applicant_Id = %s", (applicant_id,))
                        total_attempts_deleted += attempt_count
                
                    cursor.execute("SELECT Email FROM applicants WHERE Applicant_Id = %s", (applicant_id,))
                    row = cursor.fetchone()
                    applicant_email = row[0] if row else None
                    if applicant_email:
                        cursor.execute("SELECT COUNT(*) FROM login_log WHERE User_Email = %s", (applicant_email,))
                        log_count = cursor.fetchone()[0]
                        if log_count > 0:
                            cursor.execute("DELETE FROM login_log WHERE User_Email = %s", (applicant_email,))
                            total_logs_deleted += log_count
                
                    # Delete the applicant
                    cursor.execute("DELETE FROM applicants WHERE Applicant_Id = %s", (applicant_id,))
                    deleted_count += 1
                except Exception as e:
                    errors.append(f"Error deleting applicant {applicant_id}: {str(e)}")
        
            mysql.connection.commit()
            cursor.close()
        
            message = f"Successfully deleted applicants"
            details = []
            if total_answers_deleted > 0:
                details.append(f"{total_answers_deleted} exam answers")
            if total_attempts_deleted > 0:
                details.append(f"{total_attempts_deleted} exam attempts")
            if total_logs_deleted > 0:
                details.append(f"{total_logs_deleted} login logs")
        
            if details:
                message += f" (also removed {', '.join(details)})"
        
            if errors:
                message += f". Errors: {'; '.join(errors)}"
        
            return jsonify({"message": message}), 200
        except Exception as e:
            print("Error in bulk delete:", e)
            mysql.connection.rollback()
            return jsonify({"error": f"Bulk delete failed: {str(e)}"}), 500

    # Student Upload Routes
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @admin_bp.route('/add_students', methods=['POST'])
    def add_students():
        file = request.files.get('file')
        exam_id = request.form.get('exam_id')  # optional exam linkage

        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid or missing file'}), 400

        try:
            # Read Excel or CSV file
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            required_columns = ['Full_Name', 'Email', 'Password', 'Phone', 'DOB', 'Gender', 'Address']
            if not all(col in df.columns for col in required_columns):
                return jsonify({'error': 'Missing required columns in uploaded file'}), 400

            cursor = mysql.connection.cursor()
            successful_uploads = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    cursor.execute("""INSERT INTO applicants (Full_Name, Email, Password, Phone, DOB, Gender, Address, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                        row['Full_Name'],
                        row['Email'],
                        row['Password'],
                        row['Phone'],
                        row['DOB'],
                        row['Gender'],
                        row['Address'],
                        None
                    ))
                    successful_uploads += 1

                    # OPTIONAL: Insert into exam_applicants/exam_student mapping table
                    # if exam_id:
                    #     applicant_id = cursor.lastrowid
                    #     cursor.execute("INSERT INTO exam_applicants (exam_id, applicant_id) VALUES (%s, %s)", (exam_id, applicant_id))

                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
                    continue  # Skip duplicate emails or other errors

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {successful_uploads} students',
                'successful_uploads': successful_uploads,
                'errors': errors
            }), 200

        except Exception as e:
            print("Upload Error:", e)
            return jsonify({'error': str(e)}), 500

    @admin_bp.route('/upload_students', methods=['POST'])
    def upload_students():
        file = request.files.get('file')
        exam_id = request.form.get('exam_id')
        uploaded_by = request.form.get('email')
        role = request.form.get('role', 'Admin')

        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid or missing file'}), 400

        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            upload_path = os.path.join('uploads/students', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)

            # Read Excel or CSV
            if filename.endswith('.csv'):
                df = pd.read_csv(upload_path)
            else:
                df = pd.read_excel(upload_path)

            required_columns = ['Full_Name', 'Email', 'Password', 'Phone', 'DOB', 'Gender', 'Address']
            if not all(col in df.columns for col in required_columns):
                return jsonify({'error': 'Missing required columns in uploaded file'}), 400

            cursor = mysql.connection.cursor()
            successful_uploads = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    cursor.execute("""INSERT INTO applicants (Full_Name, Email, Password, Phone, DOB, Gender, Address, group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                        row['Full_Name'],
                        row['Email'],
                        row['Password'],
                        row['Phone'],
                        row['DOB'],
                        row['Gender'],
                        row['Address'],
                        None
                    ))
                    successful_uploads += 1

                    # Optional: Insert into exam_applicants
                    # if exam_id:
                    #     applicant_id = cursor.lastrowid
                    #     cursor.execute("INSERT INTO exam_applicants (exam_id, applicant_id) VALUES (%s, %s)", (exam_id, applicant_id))

                except Exception as e:
                    errors.append(f"Row {index + 1}: {str(e)}")
                    continue  # skip duplicates or bad rows

            # Log the upload (if file_uploads table exists)
            try:
                cursor.execute("""INSERT INTO file_uploads (Uploaded_By, Role, File_Name, File_Path) VALUES (%s, %s, %s, %s)""", (uploaded_by, role, filename, upload_path))
            except Exception as e:
                print("Logging upload failed:", e)
                # Continue even if logging fails

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                'success': True,
                'message': f'Successfully uploaded {successful_uploads} students and logged the upload',
                'successful_uploads': successful_uploads,
                'errors': errors
            }), 200

        except Exception as e:
            print("Upload Error:", e)
            return jsonify({'error': str(e)}), 500

    # Conducted Exams Route - Admin can see ALL conducted exams
    @admin_bp.route('/conducted_exams', methods=['GET'])
    def get_all_conducted_exams():
        try:
            cursor = mysql.connection.cursor()
            query = """
                SELECT 
                    ee.Exam_Id,
                    ee.Exam_Name,
                    ee.Exam_Date,
                    ee.faculty_email,
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
                WHERE TIMESTAMP(ee.Exam_Date, ee.Exam_Time) + INTERVAL ee.Duration_Minutes MINUTE <= NOW()
                GROUP BY ee.Exam_Id, ee.Exam_Name, ee.Exam_Date, ee.faculty_email, attempts.attempted_applicants
                ORDER BY ee.Exam_Date DESC
            """
            cursor.execute(query)
        
            # Fetch all results and convert to list of dictionaries
            columns = [desc[0] for desc in cursor.description]
            exams = []
            for row in cursor.fetchall():
                exams.append(dict(zip(columns, row)))
        
            cursor.close()
            return jsonify({"success": True, "exams": exams}), 200
        except Exception as e:
            print("Error fetching conducted exams:", e)
            return jsonify({"success": False, "error": str(e)}), 500

    # Conducted Exams by Faculty - Admin can filter by specific faculty
    @admin_bp.route('/conducted_exams/<faculty_email>', methods=['GET'])
    def get_conducted_exams_by_faculty(faculty_email):
        try:
            cursor = mysql.connection.cursor()
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
            columns = [desc[0] for desc in cursor.description]
            exams = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            return jsonify({"success": True, "exams": exams}), 200
        except Exception as e:
            print("Error fetching conducted exams for faculty:", e)
            return jsonify({"success": False, "error": str(e)}), 500
        
    @admin_bp.route('/exam/delete/<int:exam_id>', methods=['DELETE'])
    def delete_exam(exam_id):
        try:
            cursor = mysql.connection.cursor()

            # 1️⃣ DELETE QUESTION BANK FIRST (🔥 REQUIRED)
            cursor.execute("DELETE FROM entrance_question_bank WHERE Exam_Id = %s",(exam_id,))

            # 2️⃣ Get all exam paper IDs
            cursor.execute("SELECT Exam_Paper_Id FROM exam_paper WHERE Exam_Id = %s",(exam_id,))
            paper_ids = [row[0] for row in cursor.fetchall()]

            if paper_ids:
                # 3️⃣ Get all attempt IDs
                cursor.execute(f"""SELECT Attempt_Id FROM applicant_attempt WHERE Exam_Paper_Id IN ({','.join(['%s'] * len(paper_ids))})""",paper_ids)
                attempt_ids = [row[0] for row in cursor.fetchall()]

                # 4️⃣ Delete answers
                if attempt_ids:
                    cursor.execute(f"""DELETE FROM applicant_answers WHERE Attempt_Id IN ({','.join(['%s'] * len(attempt_ids))})""",attempt_ids)

                # 5️⃣ Delete attempts
                cursor.execute(f"""DELETE FROM applicant_attempt WHERE Exam_Paper_Id IN ({','.join(['%s'] * len(paper_ids))})""",paper_ids)

            # 6️⃣ Delete exam assignments
            cursor.execute("DELETE FROM applicant_exam_assign WHERE Exam_Id = %s",(exam_id,))

            # 7️⃣ Delete exam papers
            cursor.execute("DELETE FROM exam_paper WHERE Exam_Id = %s",(exam_id,))

            # 8️⃣ FINALLY delete exam
            cursor.execute("DELETE FROM Entrance_Exam WHERE Exam_Id = %s",(exam_id,))

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "success": True,
                "message": "Exam and all related data deleted successfully"
            }), 200

        except Exception as e:
            mysql.connection.rollback()
            print("🔥 Exam delete failed:", e)
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
       
    @admin_bp.route('/designations', methods=['GET'])
    def get_designations():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Designation_Id, Designation_Name FROM mst_designation ORDER BY Designation_Id ASC")
        rows = cursor.fetchall()
        cursor.close()

        data = [
            {"id": row[0], "name": row[1]}
        for row in rows]

        return jsonify({"status": "success", "data": data})
    
    # ADD DESIGNATION
    @admin_bp.route('/designations', methods=['POST'])
    def add_designation():
        data = request.json
        name = data.get("name")

        cursor = mysql.connection.cursor()

        # 🔍 Check if designation already exists
        cursor.execute("SELECT COUNT(*) FROM mst_designation WHERE Designation_Name = %s", (name,))
        exists = cursor.fetchone()[0]

        if exists > 0:
            cursor.close()
            return jsonify({
                "status": "error",
                "message": "Designation already exists"
            }), 400

        # ➕ Insert new designation
        cursor.execute(
            "INSERT INTO mst_designation (Designation_Name) VALUES (%s)",
            (name,)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({"status": "success","message": "Designation added"})

    @admin_bp.route('/designations/<int:id>', methods=['PUT'])
    def update_designation(id):
        data = request.json
        name = data.get("name")

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE mst_designation SET Designation_Name = %s WHERE Designation_Id = %s",
            (name, id)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({"status": "success", "message": "Designation updated"})
    
    @admin_bp.route('/designations/<int:id>', methods=['DELETE'])
    def delete_designation(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM mst_designation WHERE Designation_Id = %s", (id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"status": "success", "message": "Designation deleted"})
    
    # GET-DESIGNATION-ROLE
    @admin_bp.route('/designation-roles', methods=['GET'])
    def get_designation_roles():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT d.Designation_Id, d.Designation_Name, 
                r.Role_Id, r.Role_Name, r.Access_Level
            FROM mst_designation d
            LEFT JOIN mst_roles r ON d.Role_Id = r.Role_Id
            ORDER BY d.Designation_Id
        """)
        rows = cursor.fetchall()
        cursor.close()

        data = [
            {
                "Designation_Id": r[0],
                "Designation_Name": r[1],
                "Role_Id": r[2],
                "Role_Name": r[3],
                "Access_Level": r[4]
            }
            for r in rows
        ]

        return jsonify({"status": "success", "data": data})

    # UPDATE-DESIGNATION-ROLE
    @admin_bp.route('/designation-roles/<int:designation_id>', methods=['PUT'])
    def update_designation_role(designation_id):
        data = request.json
        role_id = data.get("role_id")

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE mst_designation 
            SET Role_Id = %s 
            WHERE Designation_Id = %s
        """, (role_id, designation_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify({"status": "success", "message": "Role updated successfully"})

    # GET-ROLES
    @admin_bp.route('/roles', methods=['GET'])
    def get_roles():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Role_Id, Role_Name, Access_Level FROM mst_roles ORDER BY Access_Level")
        rows = cursor.fetchall()
        cursor.close()

        return jsonify({
            "status": "success",
            "data": [
                {"Role_Id": r[0], "Role_Name": r[1], "Access_Level": r[2]}
                for r in rows
            ]
        })

    @admin_bp.route('/applicants/<int:applicant_id>', methods=['GET'])
    def get_single_applicant(applicant_id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT 
                    Applicant_Id,
                    Full_Name,
                    Email,
                    Phone,
                    DOB,
                    Gender,
                    Address,
                    Registration_Date
                FROM applicants
                WHERE Applicant_Id = %s
            """, (applicant_id,))
            
            row = cursor.fetchone()
            cursor.close()

            if not row:
                return jsonify({"error": "Applicant not found"}), 404

            columns = [
                "Applicant_Id",
                "Full_Name",
                "Email",
                "Phone",
                "DOB",
                "Gender",
                "Address",
                "Registration_Date"
            ]

            return jsonify(dict(zip(columns, row))), 200

        except Exception as e:
            print("Error fetching applicant details:", e)
            return jsonify({"error": "Unable to fetch applicant"}), 500

    return admin_bp
