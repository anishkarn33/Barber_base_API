
Barber Appointment Backend - FastAPI
This repository contains the backend service for managing barber appointments using FastAPI. The service integrates with PostgreSQL to store appointment details and provides RESTful APIs for users and barbers to manage appointments.

Features

FastAPI-based backend with asynchronous support.
PostgreSQL integration for data persistence.
RESTful API for booking, updating, and canceling barber appointments.
Secure storage and management of appointment data.
Authentication and authorization for barbers and users.
Environment variable support with .env files.
Deployment with Docker (optional).
Setup and Installation

1. Clone the repository:
git clone https://github.com/anishkarn33/Barber_base_API.git
cd Barber_base_API

2. Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up environment variables:
Create a .env file in the root directory and add the following details:
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key

5. Apply database migrations:
alembic upgrade head

6. Run the FastAPI server:
uvicorn main:app --reload

API Endpoints
Register Salon - POST /salons/register/
List Salons - GET /salons/
Get Salon Details - GET /salons/{id}/
Book Appointment - POST /appointments/
List Appointments - GET /appointments/
For detailed API documentation, visit /docs in the running server.