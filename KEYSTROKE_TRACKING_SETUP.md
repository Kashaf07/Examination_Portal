# 🔍 Keystroke Tracking Feature - Setup Instructions

## Overview
This feature tracks ALL keyboard activity during exams, including:
- Every key pressed (letters, numbers, symbols)
- Special keys (Ctrl, Alt, Tab, Shift, etc.)
- Key combinations (Ctrl+C, Ctrl+V, etc.)
- Timestamps for each keystroke
- Question-wise grouping

## What Was Changed

### 1. Database Changes
- **New Table**: `keystroke_logs` - stores all keystroke data
- **Migration File**: `db/migrate_keystroke_tracking.sql`
- **Updated**: `db/init.sql` - includes keystroke_logs table for fresh installs

### 2. Backend Changes
- **New Route**: `backend/routes/keystroke_routes.py`
  - `/api/keystroke/log` - Save keystroke logs (batch)
  - `/api/keystroke/logs/<attempt_id>` - Get logs by attempt
  - `/api/keystroke/summary/<attempt_id>` - Get summary stats
- **Updated**: `backend/app.py` - registered keystroke routes

### 3. Frontend Changes
- **New Composable**: `frontend/src/composables/useKeystrokeTracking.js`
- **New Component**: `frontend/src/components/KeystrokeLogsModal.vue`
- **Updated**: `frontend/src/views/Student.vue` - tracks keystrokes during exam
- **Updated**: `frontend/src/views/ViewResponsesAdmin.vue` - added eye icon to view logs

## 📋 Commands to Run

### Step 1: Stop Running Containers
```bash
docker-compose down
```

### Step 2: Build Docker Images
```bash
docker build -t izma7681/exam-frontend:latest ./frontend
docker build -t izma7681/exam-backend:latest ./backend
docker build -t izma7681/exam-db:latest ./db
```

### Step 3: Start Containers
```bash
docker-compose up --build
```

### Step 4: Run Migration (In Another Terminal)
**IMPORTANT**: Wait for containers to fully start, then run:

```bash
docker exec -i <mysql_container_name> mysql -uroot -proot entrance_database < db/migrate_keystroke_tracking.sql
```

**To find your MySQL container name**, run:
```bash
docker ps
```
Look for the container with MySQL image (usually named like `exam_db` or similar).

**Example**:
```bash
docker exec -i exam_db mysql -uroot -proot entrance_database < db/migrate_keystroke_tracking.sql
```

### Alternative: If you want to use docker-compose service name
```bash
docker-compose exec db mysql -uroot -proot entrance_database < db/migrate_keystroke_tracking.sql
```

## ✅ Verification

### 1. Check if table was created:
```bash
docker exec -i <mysql_container_name> mysql -uroot -proot entrance_database -e "SHOW TABLES LIKE 'keystroke_logs';"
```

### 2. Check table structure:
```bash
docker exec -i <mysql_container_name> mysql -uroot -proot entrance_database -e "DESCRIBE keystroke_logs;"
```

### 3. Test the feature:
1. Login as a student
2. Start an exam
3. Type some answers, press various keys
4. Submit the exam (or get restricted)
5. Login as admin/faculty
6. Go to "View Responses" for that exam
7. Find a "Restricted" status row
8. Click the **eye icon** 👁️ next to "Restricted"
9. You should see the keystroke logs modal with all keys pressed

## 🎯 How It Works

### During Exam:
1. Student takes exam
2. Every keystroke is captured in real-time
3. Logs are batched and sent to backend every 10 seconds (or when 50 keys are pressed)
4. Backend stores logs in `keystroke_logs` table with question ID

### Viewing Logs:
1. Admin/Faculty views exam responses
2. For "Restricted" status students, an eye icon appears
3. Clicking the icon opens a modal showing:
   - Exam name
   - Student details
   - Question-by-question keystroke breakdown
   - Statistics: Total keys, Copy attempts, Paste attempts, Suspicious keys
   - Timeline of all keystrokes with timestamps

## 📊 What Gets Tracked

### Regular Keys:
- Letters: a, b, c, A, B, C
- Numbers: 1, 2, 3, 4, 5
- Symbols: !, @, #, $, %

### Special Keys:
- Navigation: Arrow keys, Tab, Enter, Backspace, Delete
- Modifiers: Ctrl, Alt, Shift, Cmd/Meta
- Function keys: F1-F12
- Other: Escape, Space, etc.

### Key Combinations:
- Copy: Ctrl+C, Cmd+C
- Paste: Ctrl+V, Cmd+V
- Select All: Ctrl+A, Cmd+A
- Any Ctrl/Alt/Cmd combinations

## 🔒 Privacy & Performance

### Performance:
- Logs are batched (50 keys or 10 seconds)
- Minimal impact on exam performance
- Async sending to backend

### Storage:
- Each keystroke: ~200 bytes
- 1000 keystrokes: ~200 KB
- Indexed for fast queries

### Privacy:
- Only stored for exam attempts
- Linked to attempt ID
- Deleted when attempt is deleted (CASCADE)

## 🚨 Troubleshooting

### Migration fails:
```bash
# Check if containers are running
docker ps

# Check MySQL logs
docker logs <mysql_container_name>

# Try manual migration
docker exec -it <mysql_container_name> bash
mysql -uroot -proot entrance_database
source /db/migrate_keystroke_tracking.sql
```

### Eye icon not showing:
- Make sure student status is "Restricted"
- Clear browser cache
- Check browser console for errors

### No logs appearing:
- Check if keystroke tracking is enabled in Student.vue
- Check browser console for API errors
- Verify backend route is registered
- Check MySQL table has data:
  ```bash
  docker exec -i <mysql_container_name> mysql -uroot -proot entrance_database -e "SELECT COUNT(*) FROM keystroke_logs;"
  ```

## 📝 Notes

- This feature works for **new exam attempts** after migration
- Old exam attempts won't have keystroke logs
- Logs are automatically cleaned up when attempts are deleted
- Eye icon only appears for "Restricted" status (you can modify this in ViewResponsesAdmin.vue)

## 🎉 Done!

Your keystroke tracking feature is now ready to use!
