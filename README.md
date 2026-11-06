# Local Services Booking Platform

A FastAPI backend for discovering and booking local services (plumbers, cleaners, tutors, etc.).

## Features

- JWT authentication (register, login, logout, refresh, profile)
- Role-based access: `customer`, `provider`, `admin`
- Provider service management (create, list, update, delete)
- Customer bookings with status flow (`pending → confirmed → completed`)
- Redis caching for service listings
- Elasticsearch search for services
- Docker Compose for PostgreSQL, Redis, and Elasticsearch

## Tech Stack

- FastAPI
- SQLAlchemy + PostgreSQL
- Redis
- Elasticsearch
- Docker Compose
- JWT + bcrypt

## Project Structure

```text
app/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── redis_client.py
├── elasticsearch_client.py
└── routers/
    ├── auth.py
    ├── services.py
    ├── bookings.py
    ├── providers.py
    └── admin.py
docker-compose.yml
requirements.txt
README.md