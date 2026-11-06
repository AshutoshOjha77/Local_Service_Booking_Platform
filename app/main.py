from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, base
from app.routers import auth, services, providers, bookings, admin
# --- IMPORT YOUR REDIS LIFECYCLE FUNCTIONS ---
from app.redis_client import init_redis, close_redis
from app.elasticsearch_client import init_elastic, close_elastic, add_products_index

# Create database tables
base.metadata.create_all(bind=engine)


# --- ADD THE LIFESPAN MANAGEMENT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block executes immediately on application startup
    await init_redis()
    # This block executes cleanly when shutting down the server
    await init_elastic()
    await add_products_index()
    yield
    await close_redis()
    await close_elastic()




# Create FastAPI application
app = FastAPI(
    title="Local Services Booking Platform",
    description="A platform to discover and book local services.",
    version="1.0.0",
    lifespan=lifespan  # <--- ATTACH THE LIFESPAN HERE
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
