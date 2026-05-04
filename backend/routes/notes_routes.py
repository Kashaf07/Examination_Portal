from flask import Blueprint, request, jsonify
import os
import json
from groq import Groq
from datetime import datetime

def create_notes_routes(mysql):
    notes_bp = Blueprint('notes', __name__)
    
    # Initialize Groq client
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    @notes_bp.route('/generate', methods=['POST'])
    def generate_notes():
        """
        Generate educational notes using AI based on subject, topics, and difficulty level
        """
        try:
            data = request.get_json()
            
            # Extract parameters
            subject = data.get("subject", "").strip()
            topics = data.get("topics", "").strip()
            difficulty = data.get("difficulty", "Medium")
            note_type = data.get("note_type", "Lecture Notes")
            length = data.get("length", "Medium")
            additional_context = data.get("additional_context", "").strip()
            email = data.get("email")
            role = data.get("role")
            
            # Validation
            if not all([subject, topics, email, role]):
                return jsonify({"error": "Subject, topics, email, and role are required"}), 400
            
            # Build AI prompt based on parameters
            prompt = build_notes_prompt(
                subject, topics, difficulty, note_type, length, additional_context
            )
            
            # Call Groq API
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert educational content creator. Generate well-structured, comprehensive study notes in markdown format."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Extract generated content
            generated_notes = response.choices[0].message.content.strip()
            
            # Save to database
            conn = mysql.connection
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO generated_notes 
                    (faculty_email, subject, topics, difficulty, note_type, length, content, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    email,
                    subject,
                    topics,
                    difficulty,
                    note_type,
                    length,
                    generated_notes,
                    datetime.now()
                ))
                conn.commit()
                note_id = cursor.lastrowid
            except Exception as db_error:
                # If table doesn't exist, just return notes without saving
                print(f"Database save failed: {db_error}")
                note_id = None
            finally:
                cursor.close()
            
            return jsonify({
                "success": True,
                "notes": generated_notes,
                "note_id": note_id,
                "metadata": {
                    "subject": subject,
                    "topics": topics,
                    "difficulty": difficulty,
                    "note_type": note_type,
                    "length": length
                }
            }), 200
            
        except Exception as e:
            print(f"Error generating notes: {str(e)}")
            return jsonify({"error": f"Failed to generate notes: {str(e)}"}), 500

    @notes_bp.route('/history', methods=['GET'])
    def get_notes_history():
        """
        Get previously generated notes for a faculty member
        """
        try:
            email = request.args.get("email")
            role = request.args.get("role")
            
            if not email or not role:
                return jsonify({"error": "Email and role are required"}), 400
            
            conn = mysql.connection
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    SELECT id, subject, topics, difficulty, note_type, length, 
                           content, created_at
                    FROM generated_notes
                    WHERE faculty_email = %s
                    ORDER BY created_at DESC
                    LIMIT 50
                """, (email,))
                
                rows = cursor.fetchall()
                
                notes_history = []
                for row in rows:
                    notes_history.append({
                        "id": row[0],
                        "subject": row[1],
                        "topics": row[2],
                        "difficulty": row[3],
                        "note_type": row[4],
                        "length": row[5],
                        "content": row[6],
                        "created_at": row[7].isoformat() if row[7] else None
                    })
                
                return jsonify({
                    "success": True,
                    "notes": notes_history
                }), 200
                
            except Exception as db_error:
                # Table might not exist yet
                return jsonify({
                    "success": True,
                    "notes": []
                }), 200
            finally:
                cursor.close()
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @notes_bp.route('/delete/<int:note_id>', methods=['DELETE'])
    def delete_note(note_id):
        """
        Delete a generated note
        """
        try:
            email = request.args.get("email")
            role = request.args.get("role")
            
            if not email or not role:
                return jsonify({"error": "Email and role are required"}), 400
            
            conn = mysql.connection
            cursor = conn.cursor()
            
            try:
                # Verify ownership
                cursor.execute("""
                    DELETE FROM generated_notes
                    WHERE id = %s AND faculty_email = %s
                """, (note_id, email))
                
                conn.commit()
                
                if cursor.rowcount > 0:
                    return jsonify({
                        "success": True,
                        "message": "Note deleted successfully"
                    }), 200
                else:
                    return jsonify({
                        "error": "Note not found or unauthorized"
                    }), 404
                    
            finally:
                cursor.close()
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return notes_bp


def build_notes_prompt(subject, topics, difficulty, note_type, length, additional_context):
    """
    Build a comprehensive prompt for AI note generation
    """
    
    # Length mapping
    length_guide = {
        "Short": "1-2 pages (500-800 words)",
        "Medium": "3-5 pages (1200-2000 words)",
        "Long": "6+ pages (2500-4000 words)"
    }
    
    # Difficulty level instructions
    difficulty_instructions = {
        "Low": """
        - Use simple, beginner-friendly language
        - Avoid complex jargon; explain technical terms when used
        - Include everyday examples and analogies
        - Break down concepts into small, digestible steps
        - Focus on foundational understanding
        """,
        "Medium": """
        - Use moderate technical terminology with explanations
        - Include practical applications and examples
        - Balance theory with practice
        - Provide some problem-solving examples
        - Assume basic prior knowledge
        """,
        "High": """
        - Use advanced technical language and industry terminology
        - Include complex problem-solving and algorithms
        - Reference research papers and advanced concepts
        - Provide in-depth theoretical explanations
        - Include edge cases and optimization techniques
        """
    }
    
    # Note type specific instructions
    note_type_instructions = {
        "Lecture Notes": """
        Create comprehensive lecture notes with:
        - Clear section headings and subheadings
        - Key concepts highlighted
        - Detailed explanations with examples
        - Visual descriptions (diagrams, flowcharts concepts)
        - Summary points at the end
        """,
        "Revision Notes": """
        Create concise revision notes with:
        - Bullet-point summaries
        - Key formulas and definitions
        - Quick reference tables
        - Important points highlighted
        - Memory aids and mnemonics
        """,
        "Exam Preparation": """
        Create exam-focused notes with:
        - Important topics likely to appear in exams
        - Previous year pattern analysis
        - Practice problems with solutions
        - MCQ preparation tips
        - Common mistakes to avoid
        """,
        "Concept Explanation": """
        Create detailed concept explanations with:
        - Step-by-step breakdown
        - Real-world applications
        - Use cases and scenarios
        - Common misconceptions addressed
        - Related concepts and connections
        """,
        "Assignment Guidelines": """
        Create assignment/project guidelines with:
        - Clear objectives and scope
        - Step-by-step instructions
        - Evaluation criteria
        - Resources and references
        - Tips for success
        """
    }
    
    prompt = f"""
Generate comprehensive educational notes for the following:

**Subject:** {subject}
**Topics:** {topics}
**Difficulty Level:** {difficulty}
**Note Type:** {note_type}
**Target Length:** {length_guide.get(length, "Medium length")}

**Difficulty Level Instructions:**
{difficulty_instructions.get(difficulty, difficulty_instructions["Medium"])}

**Note Type Instructions:**
{note_type_instructions.get(note_type, note_type_instructions["Lecture Notes"])}
"""

    if additional_context:
        prompt += f"""
**Additional Context:**
{additional_context}
"""

    prompt += """

**Format Requirements:**
- Use markdown formatting
- Include clear headings (##) and subheadings (###)
- Use bullet points and numbered lists where appropriate
- Highlight key terms using **bold**
- Include code blocks for technical content (if applicable)
- Add examples in blockquotes (>)
- End with a summary section

**Structure:**
1. Introduction/Overview
2. Main Content (organized by subtopics)
3. Examples and Applications
4. Key Takeaways/Summary
5. Further Reading/References (if applicable)

Generate the notes now:
"""
    
    return prompt
