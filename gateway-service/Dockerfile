# filepath: /Users/spectorclef/Documents/Keith/distributed_service/distributed-service-assembly/storage-service/Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

# filepath: /Users/spectorclef/Documents/Keith/distributed_service/distributed-service-assembly/gateway-service/Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]

# filepath: /Users/spectorclef/Documents/Keith/distributed_service/distributed-service-assembly/gateway-service/routes/__init__.py