# Event Notification API

A FastAPI-based backend that allows users to create scheduled events and automatically sends notification emails before the event occurs. Built with PostgreSQL, SQLAlchemy, and async background workers.

## Features

- Create, retrieve, and list events via REST API  
- Automatic email notifications for upcoming events  
- Background worker runs asynchronously  
- Notification logs to prevent duplicate alerts  
- Fully async database operations using SQLAlchemy  
- Docker & Docker Compose setup for local development  
- Unit and integration tests using `pytest` and `httpx`  

---

## How to use the code:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/event-api-project.git
cd event-api-project
```

### 2. Optional: Environment Configuration

> **Want to test email notifications?**
> You can use Mailtrap to safely capture outgoing emails. 
>
> Follow the steps below to set it up:
1. Log in to Mailtrap.
2. Go to **Inbox** → **SMTP Settings** → Copy the credentials:
   - `MAIL_USERNAME` → your SMTP user
   - `MAIL_PASSWORD` → your SMTP password
   - `MAIL_FROM` → noreply@example.com
   - `MAIL_to` → use your email
   - `EMAIL_NOTIFICATIONS` → true
(Under your inbox settings, you can **add your own email address as a BCC** or **check the inbox dashboard** to view incoming emails.)
3. Change the current `.env` file with it.
4. Restart the app after updating your `.env` file.
---

### 3. Run with Docker 

```bash
docker-compose up --build
```

This will start:

- FastAPI app (on `http://localhost:8000`)  
- PostgreSQL database  
- Background task worker (in the same container)  

---

## Running Tests

```bash
docker-compose exec api pytest tests/test_notifications.py
```

### Test Coverage

The `test_event_notification_flow` test validates:

- Creating a new event via the API
- Retrieving the created event from the database
- Sending a notification for an event happening within the next 5 minutes
- Recording a notification log in the database
- Ensuring duplicate notifications are not sent on repeated checks
  

---

## API Documentation

FastAPI automatically provides Swagger UI at:

- `http://localhost:8000/docs` – Interactive API docs  
- `http://localhost:8000/redoc` – ReDoc-style documentation  

---

---

## Scalability & Future Improvements 

### If I had more time, I would:
- Add user authentication and support for multiple users to associate events with user accounts.
- Implement a notification retry mechanism with exponential backoff in case of email failures.
- Add filtering for event listings.
- Use Celery with Redis or RabbitMQ instead of an in-process background task for better task management and reliability.
- Add frontend or dashboard to manage events visually.
- Implement support for recurring events and calendar integrations.
- Improve logging, monitoring, and alerting for production deployment.

###  Limitations (If scaled to more than 10,000 users):
- **In-memory background tasks** may not scale—shifting to a distributed task queue (like Celery + Redis) is essential.
- **Database bottlenecks**: With a high volume of events, PostgreSQL performance could degrade without indexing and query optimization.
- **Notification delivery**: Mailtrap is only for testing; a production email service (like SendGrid) with rate-limiting and throttling is required.
- **Horizontal scaling**: The current app runs a single background task loop—would need to decouple workers from the web app to scale independently.
- **No multi-tenancy**: Events aren't scoped to users or organizations yet, which would be needed in a production environment.


---

## Tech Stack

- **FastAPI** — Async web framework  
- **PostgreSQL** — Relational database  
- **SQLAlchemy** — Async ORM  
- **Mailtrap** — Email testing  
- **Docker** — Containerization  
- **Pytest** — Testing framework  

---