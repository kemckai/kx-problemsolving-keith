# filepath: /Users/spectorclef/Documents/Keith/distributed_service/distributed-service-assembly/storage-service/Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["python", "app.py"]