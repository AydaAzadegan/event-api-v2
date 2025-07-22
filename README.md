# Event API – FastAPI Project

This is a REST API built using **FastAPI**. It allows users to create, view, and manage events, with the added functionality of simulating notifications when an event is about to start.

---

## Features

- Add new events with title, description, and datetime  
- List all existing events  
- Retrieve a specific event by its ID  
- Simulated notifications: If an event is scheduled to begin within the next 5 minutes, a message is printed to the console  
- MVC-like structure for clarity and maintainability (`models/`, `services/`, `controllers/`)  
- In-memory data storage using Python dictionary  
- Timezone-aware datetime validation with Pydantic  
- Unit tests with `pytest` and FastAPI’s `TestClient`  

---

## How to Set Up & Run

### 1. **Clone the project**

```bash
git clone https://github.com/AydaAzadegan/event-api.git
cd event-api
```


### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Run the app**

```bash
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API.

---

## Swagger UI

FastAPI provides an interactive Swagger UI at:

```
http://127.0.0.1:8000/docs
```

You can test:
- `POST /events` – Create an event  
- `GET /events` – List all events  
- `GET /events/{event_id}` – Get one by ID  
If any event starts in ≤ 5 mins, a console message will be printed.

---

## Run the Tests

```bash
pytest
```

Tests include:
- Creating events
- Listing all events
- Handling non-existent event ID (404)
- Triggering notification for soon-starting events
You should see something like this if everything works:

```bash
tests/test_events.py .... [100%]
4 passed in 0.7s
```
---

## Limitations (If scaled to more than 10,000 users)

### 1. In-Memory Data Storage 

Currently, all event data is stored in a **Python dictionary** (`events_db`). This means:
- **All data is lost** when the server restarts.
- It cannot support horizontal scaling (e.g. multiple servers) because memory isn’t shared.
- There’s no long-term data retention, backups, or query optimization.

 **Solution**: Migrate to a **persistent database** like PostgreSQL.

---

### 2. Notification Logic Tied to Manual Requests

Right now, the "notification" is just a `print()` statement triggered **only when someone visits `/events`**. This is not scalable or reliable because:
- If no one visits the route, notifications are never triggered.
- There's no real-time background process monitoring upcoming events.
- Notifications are printed to the server console, not sent to users (email, SMS, push, etc.).

 **Solution**: Use a background task queue like **Celery** with **Redis**, or FastAPI’s `BackgroundTasks`, to monitor and dispatch real-time alerts independently of user actions.

---

### 3. No Fault Tolerance or Persistence on Restart

Every time the app restarts:
- All created events are gone.
- There is no backup or caching system to recover previous data.

This makes the system **unsuitable for production** or even internal tools.

 **Solution**: Persist data using a real DB and add proper error handling and logging mechanisms.

---

While this project is great for showcasing **FastAPI fundamentals**, testing, and modular design, it requires significant upgrades for real-world scalability.

---


## Folder Structure

```
.
├── controllers/        # Route handlers
├── models/             # Pydantic schemas
├── services/           # Business logic
├── tests/              # Test cases
├── main.py             # FastAPI entry point
├── requirements.txt    # Dependencies
├── README.md           # Project info
└── .gitignore          # Ignored files
```


