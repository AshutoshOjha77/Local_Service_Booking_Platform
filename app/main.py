from fastapi import FastAPI

from app.database import engine, base
from app.routers import auth, services, providers, bookings, admin

# Create database tables
base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Local Services Booking Platform",
    description="A platform to discover and book local services.",
    version="1.0.0"
)

# Register routers
app.include_router(auth.router)
app.include_router(services.router)
app.include_router(providers.router)
app.include_router(bookings.router)
app.include_router(admin.router)


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Local Services Booking Platform API",
        "status": "Running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }