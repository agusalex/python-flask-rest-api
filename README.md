# Sprocket API 
Flask Web Application running on Docker.


## Overview
It handles Sprocket and sprocket factories chart data through its **/factories** and **/sprocket** endpoints.
This is a Flask web application that is containerized using Docker. Using SQLAlchemy it can run either on PostgresSQL or Sqlite database.

## Requirements

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository**

    ```bash
    git clone https://github.com/agusalex/sprocket_api.git
    cd sprocket_api
    ```

2. **Build and Run the Docker Containers**

    ```bash
    docker-compose up --build
    ```

3. **First Time Database Setup**

    To initialize the database and apply migrations on the first run.

    ```bash
    docker-compose exec web bash init_db.sh
    ```

## Environment Variables

- `DATABASE_URL` : Connection string for the PostgreSQL database.
- `ENV` : Determines the environment the app is running in. **("development", "testing", "production")**

## Database Migrations

Migrations are handled by Flask-Migrate. To manually apply migrations, run:

```bash
docker-compose exec web flask db migrate -m "Your message here"
docker-compose exec web flask db upgrade
```

## Running Tests

To run tests within the Docker container, execute:

```bash
docker-compose exec web pytest tests
```

