# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full app
COPY . .

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

