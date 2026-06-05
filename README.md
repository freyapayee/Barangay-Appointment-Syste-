# Barangay Appointment System

A Django project with three apps:

- `residents` - add, edit, delete, view, and search barangay resident/user info.
- `services` - manage barangay certificates, barangay registration, and permits.
- `appointments` - record and manage appointment schedules.

## Features

- Homepage dashboard with counts for Documents, Registration, Permits, Residents, and Appointments.
- User info fields: last name, first name, middle name, age, address, gender, previous address, marital status, occupation, and year of residency.
- Barangay document applications: Indigency, Residency, Clearance.
- Barangay registration applications.
- Permit applications: Building and Business.
- Add, edit, delete, view, search, and filter records.

## Setup

Create and activate the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a PostgreSQL database named `barangay_appointment`, then update `.env` if your username, password, host, or port is different.

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Docker PostgreSQL Setup

This project includes a Docker Compose service for Django. It connects to your PostgreSQL container published as `5434:5432`.

Start the app:

```bash
docker compose up --build
```

In another terminal, run migrations:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open `http://127.0.0.1:8000/`.

PostgreSQL connection:

- Database: `barangay_appointment`
- User: `postgres`
- Password: `postgres`
- Host inside Docker: `host.docker.internal`
- Host from your Mac: `localhost`
- Port from your Mac: `5434`
- PostgreSQL container port: `5432`

## MySQL Option

The project supports MySQL through `DATABASE_ENGINE=mysql` in `.env`, but the `mysqlclient` package requires MySQL/MariaDB client headers and `pkg-config` on macOS. After installing those system tools, install:

```bash
pip install mysqlclient>=2.2
```
