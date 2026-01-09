"""
Main FastAPI application for the wine inventory management system
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api import router
from .config.settings import settings
from .database import init_db
import uvicorn
import logging
from loguru import logger
import time


# Create FastAPI app with settings
app = FastAPI(
    title=settings.app_name,
    description="Wine Inventory Management System API with Admin Panel",
    version=settings.app_version,
    debug=settings.debug,
    openapi_url="/api/v1/openapi.json" if settings.debug else None,
    docs_url="/api/v1/docs" if settings.debug else None,
    redoc_url="/api/v1/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Additional security headers
    allow_origin_regex=r"https?://.*",
)

# Include API router
app.include_router(router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Middleware to handle database sessions
    """
    start_time = time.time()
    request.state.start_time = start_time
    
    try:
        response = await call_next(request)
    finally:
        # Log request info
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
    
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all requests
    """
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup
    """
    logger.info("Starting up Wine Inventory Management System...")
    
    # Initialize database
    init_db()
    
    # Additional startup tasks can be added here
    logger.info("Application startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown
    """
    logger.info("Shutting down Wine Inventory Management System...")


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Wine Inventory Management System API",
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )