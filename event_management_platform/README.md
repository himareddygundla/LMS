# Event Management Platform

A colorful full-stack backend assignment project built with **FastAPI + SQLAlchemy + SQLite + MongoDB + Docker + Pytest + GitHub Actions**.

## Features
- Participants CRUD
- Trainers CRUD + session view
- Events CRUD + trainer assignment
- Participant registration with capacity validation
- MongoDB logging for activity, event logs, and feedback comments
- Stylish frontend dashboard served from FastAPI
- Swagger API docs
- Dockerized setup with MongoDB
- CI pipeline using GitHub Actions
- Pytest-based integration tests

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **SQL DB:** SQLite (easy local execution; can be swapped for PostgreSQL/MySQL)
- **NoSQL:** MongoDB
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Testing:** Pytest, FastAPI TestClient, mongomock
- **DevOps:** Docker, Docker Compose, GitHub Actions

## Project Structure
```text
event_management_platform/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── mongo.py
│   ├── routers/
│   ├── templates/
│   ├── static/
│   └── tests/
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## ER Diagram
```text
Participants (1) ----< Registrations >---- (1) Events
                     
Trainers (1) ----------------------------> Events
```

## SQL Tables
- `participants`
- `trainers`
- `events`
- `registrations`

## MongoDB Collections
- `event_logs`
- `user_activity_logs`
- `feedback_comments`

## How to Run Locally
### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate it
**Windows PowerShell**
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start MongoDB
Make sure MongoDB is running locally, or use Docker Compose below.

### 5. Run the app
```bash
uvicorn app.main:app --reload
```

### 6. Open in browser
- Frontend: `http://127.0.0.1:8000/`
- Swagger Docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Run with Docker Compose
```bash
docker compose up --build
```

Then open:
- Frontend: `http://localhost:8000/`
- Docs: `http://localhost:8000/docs`

## API Endpoints
### Participants
- `POST /api/participants`
- `GET /api/participants`
- `PUT /api/participants/{participant_id}`
- `DELETE /api/participants/{participant_id}`
- `POST /api/participants/register`

### Trainers
- `POST /api/trainers`
- `GET /api/trainers`
- `PUT /api/trainers/{trainer_id}`
- `GET /api/trainers/sessions`

### Events
- `POST /api/events`
- `GET /api/events`
- `PUT /api/events/{event_id}`
- `DELETE /api/events/{event_id}`
- `POST /api/events/{event_id}/assign-trainer`

### Logs
- `GET /api/logs/event`
- `GET /api/logs/activity`
- `POST /api/logs/feedback`
- `GET /api/logs/feedback`
- `DELETE /api/logs/feedback/{feedback_id}`

## Testing
```bash
pytest -v
```

## Coverage
```bash
pytest --cov=app --cov-report=term-missing
```

## CI/CD Explanation
The GitHub Actions workflow:
1. checks out the code,
2. installs Python dependencies,
3. runs all tests with coverage,
4. builds the Docker image.

It triggers on **push** and **pull request** for `main` and `master`.

## Environment Variables
Use these values in `.env` if needed:
```env
DATABASE_URL=sqlite:///./event_management.db
MONGO_URL=mongodb://mongo:27017
MONGO_DB_NAME=event_platform
```

## Notes
- SQLite is chosen for easiest execution during submission.
- You can switch to PostgreSQL/MySQL by changing `DATABASE_URL`.
- MongoDB is used specifically for logs and feedback tracking.


## Frontend Pages

The frontend now includes separate colorful pages for each core module:

- `/participants` → Register participant, update participant profile, delete participant, view participants, register participant for event
- `/trainers` → Add trainer, update trainer profile, assign trainer to event, view sessions
- `/events` → Create event, update event, delete event, manage capacity

The home page (`/`) acts as a dashboard and navigation landing page.
