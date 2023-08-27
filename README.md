# Sprocket API 
Flask Web Application running on Docker.
Tests automated using GitHub CI


## Overview
It handles Sprocket and sprocket factories chart data through its **/factories** and **/sprocket** endpoints.
This is a Flask web application that is containerized using Docker. Using SQLAlchemy it can run either on PostgreSQL or Sqlite database.

## Features
- Docker and docker-compose
- SQLAlchemy ORM
- **v1/factories** and **v1/sprocket** endpoints
  - Create Read and Update for sprockets and Create/Read for factories
- Tests for routes and utils
- Gunicorn/Postgres deployment for prod
- Flask run/ Sqlite for development

## Design Decisions and Future Considerations
- Decided on storing the chart_data as a String inside a single column on the DB
    - As it seems chart data is read-only for now, and we won't access individual data points it made more sense to bundle it all in a JSON blob
    - This allows us to be flexible if we need to change this spec in the future
    - Data validation if we had to update would be harder. Search would be though, it does not seem like we would need that.
    - If we did change this approach would be necessary if we want to achieve write performance, read performance is better as is if you need the whole chart_data
- Went with a single-layer design, since the project is so small separating routes from the internal CRUD logic of the model into a service layer would be overkill.
    - If the logic for the routes gets more complex this should be done.
    The same would apply to creating a repository layer if we needed custom queries. Though using an ORM is solving this for us.
- Proper error handling would be nice with more time
    - This would take the form of adding try catch in crucial parts of the code
    - Having typed errors for ease of maintenance, e.g. "class ValidationError(Exception)" 
- Proper logging integrated with request ID for tracking, (so having a request context passed around)
- Auth if needed
- Kubernetes and deployment to the cloud if needed
- Status and health endpoints
- Adding typings to this project, though python does not require it, making it typed helps with ease of debugging and hardening

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

## Testing the servie

Inside the postman folder there is a postman collection for testing this service.
I will be spun up by default on port 8080

