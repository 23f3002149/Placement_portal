# Placement Portal - Startup Guide with Celery + Redis

## Prerequisites
- Python 3.8+
- Redis installed
- All dependencies from requirements.txt

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or individually
pip install celery redis flask flask_sqlalchemy flask_jwt_extended flask_cors python-dotenv
```

## Startup (3 Processes Required)

### 1. Start Redis Server
```bash
redis-server
```
- Runs on: `localhost:6379`
- This is the message broker and result backend

### 2. Start Celery Worker (in a new terminal)
```bash
cd backend
celery -A app worker --loglevel=info
```
- Processes background tasks
- Handles emails, CSV exports, reminders
- Check console for task execution logs

### 3. Start Flask Backend (in a new terminal)
```bash
cd backend
python3 app.py
```
- Runs on: `http://127.0.0.1:5000`
- API endpoints

### 4. Start Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```
- Runs on: `http://localhost:5173` (or similar)

## Environment Setup

Add to `.env` (if not already there):
```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
ADMIN_EMAIL=admin@example.com
SMTP_PORT=587
```

## What Uses Celery Now

✅ **Email Notifications:**
- Student application confirmation
- Application status updates (shortlisted/rejected/selected)
- Interview schedule notifications
- Interview reminders (2 minutes after initial email)
- Admin notifications on new applications

✅ **CSV Exports:**
- Student applications report
- Company monthly report

✅ **Scheduled Tasks:**
- Interview reminders scheduled for 2 minutes after notification

## Task Monitoring

### View Task Status
- Tasks are queued in Redis
- Check Celery worker console for execution logs

### Check Running Tasks
```bash
celery -A app inspect active
```

### Monitor Task Results
```bash
celery -A app inspect reserved
```

## Troubleshooting

### Redis not starting
```bash
# Check if Redis is installed
redis-server --version

# Install on Linux
sudo apt-get install redis-server

# On macOS
brew install redis
```

### Celery worker not picking tasks
- Ensure Redis is running
- Check worker logs for errors
- Make sure app.py is using Celery config

### Tasks not executing
- Verify Redis connection: `redis-cli ping`
- Check Celery worker is running
- Review app.py logs for task queue messages

## Architecture

```
Request → Flask API → Celery Task Queue → Redis → Celery Worker → Task Execution
                                            ↑
                                       (Result Storage)
```

## Development Tips

- Keep 4 terminals open: Redis, Celery Worker, Flask, Frontend
- Watch Celery worker console for real-time task execution
- Use `celery -A app purge` to clear task queue if needed

---

That's it! Your placement portal now has production-ready async task handling! 🚀
