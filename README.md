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

---

## Limitations (If scaled to 10,000+ users)

- In-memory DB (no persistence)
- Notification logic triggered by manual GET request
- No concurrency handling
- Events lost on app restart

---

## Possible Improvements

- Add a real database like PostgreSQL  
- Use background jobs for async notifications  
- Dockerize the project  
- Add pagination & search filters  
- Improve logging & API docs  

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


