# AI Question Generation Integration - Setup Guide

## Overview
This integration adds AI-powered question generation to your Question Bank page. Users can click the "Generate Question" button to open a modal where they can generate questions using AI and add them directly to the question bank.

## What Was Added

### Backend Changes

1. **Dependencies Added** (`backend/requirements.txt`):
   - `groq` - For AI question generation
   - `python-dotenv` - For environment variable management

2. **New Endpoints** (`backend/app.py`):
   - `POST /generate-paper` - Generates questions using Groq AI
   - `POST /api/questions/add-generated` - Saves AI-generated questions to database

### Frontend Changes

1. **New Component** (`frontend/src/components/GenerateQuestionModal.vue`):
   - Modal interface for AI question generation
   - Form to specify subject, topics, difficulty, and question type
   - Display generated questions with selection
   - Save selected questions to question bank

2. **Updated Component** (`frontend/src/views/UploadQuestionBank.vue`):
   - Added "Generate Question" button
   - Integrated GenerateQuestionModal component

## Setup Instructions

### Step 1: Get Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Create a new API key
4. Copy the API key

### Step 2: Configure Environment Variables

1. Create a `.env` file in the `backend` folder:
   ```bash
   cd backend
   touch .env
   ```

2. Add your Groq API key to the `.env` file:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

### Step 3: Install Backend Dependencies

**IMPORTANT**: You need to install the new Python packages manually:

```bash
cd backend
pip install groq python-dotenv
```

Or if you're using a virtual environment:

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install groq python-dotenv
```

### Step 4: Restart Backend Server

After installing dependencies and setting up the `.env` file, restart your Flask backend:

```bash
cd backend
python app.py
```

### Step 5: Test the Integration

1. Log in to your application as Admin or Faculty
2. Navigate to the Question Bank page
3. Click the "🤖 Generate Question" button (purple button on the right)
4. Fill in the form:
   - Subject (e.g., "Mathematics")
   - Topics (e.g., "Algebra, Geometry")
   - Number of questions (1-20)
   - Difficulty (Easy/Medium/Hard)
   - Question Type (MCQ/Fill/One Word/True-False/Descriptive)
5. Click "✨ Generate"
6. Select the questions you want to add
7. Click "✅ Add X Question(s) to Bank"

## Features

- **AI-Powered Generation**: Uses Groq's Llama 3.1 model for intelligent question generation
- **Multiple Question Types**: Supports MCQ, Fill in the Blanks, One Word, True/False, and Descriptive questions
- **Difficulty Levels**: Generate Easy, Medium, or Hard questions
- **Batch Generation**: Generate multiple questions at once
- **Generate More**: Add more questions to the current set
- **Selective Addition**: Choose which generated questions to add to your bank
- **Authorization**: Respects existing role-based access control

## Troubleshooting

### Error: "Server error. Make sure the AI backend is running."
- Check that your backend server is running
- Verify the GROQ_API_KEY is set in your `.env` file
- Check backend console for error messages

### Error: "Missing required fields"
- Ensure all form fields are filled before clicking Generate

### Error: "Unauthorized Access"
- Verify you're logged in with proper credentials
- Check that you have permission to add questions to the selected exam

### Questions not appearing after generation
- Check browser console for errors
- Verify the backend response in Network tab
- Ensure the AI response is valid JSON

## Database Schema

The generated questions are saved to the `entrance_question_bank` table with the following structure:

- `Exam_Id` - The exam ID
- `Question_Type` - Type of question (MCQ, Fill, etc.)
- `Question_Text` - The question text
- `Option_A`, `Option_B`, `Option_C`, `Option_D` - MCQ options (if applicable)
- `Correct_Answer` - The correct answer
- `Marks` - Points for the question (default: 1)

## Security Notes

- The `.env` file is gitignored and should never be committed
- API keys should be kept secure and not shared
- The integration respects existing authorization checks
- Only authorized users (Admin/Faculty) can generate and add questions

## Support

If you encounter any issues:
1. Check the backend console logs
2. Check the browser console for frontend errors
3. Verify all dependencies are installed
4. Ensure the `.env` file is properly configured
