
## Barber Appointment Backend - FastAPI
This repository contains the backend service for managing barber appointments using FastAPI. The service integrates with PostgreSQL to store appointment details and provides RESTful APIs for users and barbers to manage appointments.

## Features

FastAPI-based backend with asynchronous support.
PostgreSQL integration for data persistence.
RESTful API for booking, updating, and canceling barber appointments.
Secure storage and management of appointment data.
Authentication and authorization for barbers and users.
Environment variable support with .env files.
Setup and Installation

## Tools and Libraries

- Python 3.9
- FastAPI (modern, fast (high-performance), web framework for building APIs with Python 3.7+)
- asyncpg (asyncio PostgreSQL driver)
- alembic (database migration tool)
- SQLAlchemy (SQL toolkit and Object-Relational Mapping)
- PostgreSQL14

## Clone the repository:

```bash
git clone https://github.com/anishkarn33/Barber_base_API.git
``` 

### Create and activate a virtual environment:
   
    python -m venv .venv

    .venv\Scripts\Activate.ps1  # On Windows: .venv\Scripts\activate

### Install the required packages
   
```bash
pip install -r requirements.txt
```


### Create a new migration repository

```bash
alembic init alembic
```

### Configure the database connection

Edit the `.env` file and set the database parameters


### Apply the migration

```bash
alembic upgrade head
```

### Apply the migration with data included

```bash
alembic -x data=true upgrade head
```

### Downgrade the migration

```bash
alembic downgrade -1
```

### Show the migration history

```bash
alembic history
```

### Show the migration status

```bash
alembic current
```

### Show the migration branches

```bash
alembic branches
```

### Run the FastAPI server:
```bash
   uvicorn main:app --reload
```