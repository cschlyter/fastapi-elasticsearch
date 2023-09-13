# FastAPI and Elasticsearch App

A simple application that uses FastAPI with Elasticsearch.

## Prerequisites

Before you begin, ensure you have Docker and Docker Compose installed on your machine. If not, you can download them from [Docker's official website](https://docs.docker.com/get-docker/).

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:cschlyter/fastapi-elasticsearch.git
cd fastapi-elasticsearch/
```

### 2. Build and Start the Services

Use Docker Compose to build and start the services:

```bash
docker-compose up --build
```

This command will set up the FastAPI application, Elasticsearch, and any other services defined in your `docker-compose.yml` file. Once everything is up and running, you can access the FastAPI application via your web browser or a tool like [httpie](https://httpie.io/) or [curl](https://curl.se/).

### 3. Access the API Documentation

FastAPI provides automatic interactive API documentation. Once the application is running, visit:

```
http://localhost:8004/docs
```

This will display the available API endpoints, and you can test them directly from the browser.

## Running Tests

Tests have been implemented using `pytest`.

To run the tests:

```bash
docker-compose exec server python -m pytest
```

## Running The Coverage Report

To run the coverage report:

```bash
docker-compose exec server python -m pytest --cov="."
```

This command will execute all the tests in the application. It's recommended to run tests before making changes to ensure the application is functioning as expected.

## Accessing the Frontend

Once the application is running, you can access the React frontend by navigating to:

```
http://localhost:3000/
```

## Code formatting tools

In order to follow code formatting best practices, the Python code uses Black, isort and flake8 tools. Here's how to run those:

Flake8:

```bash
docker-compose exec server flake8 .
```

Black:

```bash
docker-compose exec server black .
```

isort:

```bash
docker-compose exec server isort .
```
