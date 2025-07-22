This is a REST API built using FastAPI. It allows users to create, view, and manage events, with the added functionality of simulating notifications when an event is about to start.

The API supports:

Adding new events with title, description, and datetime

Listing all existing events

Retrieving a specific event by its ID

Simulated notifications: If an event is scheduled to begin within the next 5 minutes, a message is printed to the console

The project uses an MVC-like structure for clarity and maintainability, separating logic into models, services, and controllers. Data is stored in memory using a Python dictionary, and Pydantic is used to validate incoming data and ensure all datetime values are timezone-aware.

Unit tests are written using pytest and FastAPI's TestClient, covering both successful and edge-case scenarios, including notification triggering and invalid ID handling.

The project includes a requirements.txt for easy setup. So just Run pip install -r requirements.txt in the terminal to set it up.

If this system were to scale to 10,000 users per day, the main issues would be:

Memory limitations due to in-memory data storage

Notification logic tied to on-demand requests

No persistence layer (events would disappear on restart)

No concurrency controls for simultaneous read/write

If more time were available, improvements could include:

Persistent database integration (e.g. PostgreSQL)

Background workers for real-time notifications

Full Dockerization for deployment

Pagination and filtering for event listings

Logging upgrades and API documentation via OpenAPI annotations
