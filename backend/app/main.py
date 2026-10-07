from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import DatabaseManager
from app.routes.prediction import router as prediction_router
from app.routes.diseases import router as diseases_router
from app.routes.history import router as history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Connects to MongoDB upon startup and closes the connection pool upon shutdown.
    """
    await DatabaseManager.connect()
    yield
    await DatabaseManager.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for React frontend (Vite/localhost and deployed origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(prediction_router)
app.include_router(diseases_router)
app.include_router(history_router)


@app.get("/", tags=["General"])
def root():
    """Root status check endpoint."""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "database": "connected" if DatabaseManager.is_connected else "disconnected",
        "docs": "/docs"
    }


@app.get("/health", tags=["General"])
def health():
    """Health check endpoint for monitoring uptime."""
    return {
        "status": "healthy",
        "database": "connected" if DatabaseManager.is_connected else "disconnected"
    }