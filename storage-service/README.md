
# Distributed Service Assembly

This project consists of two microservices: `storage-service` and `gateway-service`. These services are built using Flask and Docker, and they demonstrate a simple distributed system architecture.

## Services

### Storage Service

The `storage-service` is a simple Flask application that provides a few endpoints:

- `/`: Serves an HTML page that says "Hello from Storage Service!"
- `/data`: Returns some dummy data in JSON format.
- `/health`: Returns the health status of the service.

### Gateway Service

The `gateway-service` is a Flask application that acts as a gateway to the `storage-service`. It provides the following endpoints:

- `/`: Serves an HTML page that says "Hello from Gateway Service!"
- `/service1`: Serves an HTML page that says "Hello from Service 1!"
- `/service1/<path:path>`: Proxies requests to the `storage-service`.
- `/health`: Returns the health status of the service.

## Dependencies

Both services use the following dependencies:

- Flask: A micro web framework for Python.
- Gunicorn: A Python WSGI HTTP Server for UNIX.
- Requests: A simple HTTP library for Python.
- Werkzeug: A comprehensive WSGI web application library.
- Psutil: A library for retrieving information on system utilization (CPU, memory, disks, network, sensors).

## Project Structure

```
distributed-service-assembly/
├── 

docker-compose.yml


├── storage-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       └── index.html
└── gateway-service/
    ├── app.py
    ├── Dockerfile
    ├── requirements.txt
    ├── templates/
    │   ├── index.html
    │   └── service1.html
    └── routes/
        ├── __init__.py
        └── service1.py
```

## Setup and Run

1. **Clone the repository**:

   ```sh
   git clone <repository-url>
   cd distributed-service-assembly
   ```

2. **Build and run the services using Docker Compose**:

   ```sh
   docker-compose up --build
   ```

3. **Access the services**:

   - `Storage Service`: [http://localhost:5001](http://localhost:5001)
   - `Gateway Service`: [http://localhost:8081](http://localhost:8081)
   - `Service 1`: [http://localhost:8081/service1](http://localhost:8081/service1)

## Explanation

### Storage Service

The 

storage-service

 is a simple Flask application that provides a few endpoints. It serves an HTML page at the root endpoint, returns some dummy data at the `/data` endpoint, and provides a health check endpoint at `/health`.

### Gateway Service

The 

gateway-service

 acts as a gateway to the 

storage-service

. It serves an HTML page at the root endpoint, another HTML page at the `/service1` endpoint, and proxies requests to the 

storage-service

 at the `/service1/<path:path>` endpoint. It also provides a health check endpoint at `/health`.

### Docker Configuration

Both services are containerized using Docker. The 

docker-compose.yml

 file is used to define and run multi-container Docker applications. It maps the container ports to the host ports, allowing you to access the services via `localhost`.



 What should the Gateway do if no Storage Services are running?

### Additional Features

- **Connection Pooling**: The 

gateway-service

 uses a connection pool to maintain a pool of connections to the 

storage-service

.
- **Health Checks**: The 

gateway-service

 performs regular health checks on the 

storage-service

.
- **Resource Monitoring**: The 

gateway-service

 monitors CPU and memory usage.
- **Background Tasks**: The 

gateway-service

 performs background tasks such as data cleanup or cache invalidation.
- **Keepalive Mechanisms**: The 

gateway-service

 ensures that connections to the 

storage-service

 remain active.
- **Graceful Shutdown**: The 

gateway-service

 handles signals to gracefully shut down the service and clean up resources.

By following these steps, you can set up and run the distributed services, and understand the architecture and functionality of the project.