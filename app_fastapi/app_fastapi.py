# File: app_fastapi/app_fastapi.py
"""
FastAPI application entry point.

This module configures and runs the FastAPI server for the
Data Science Demo Platform backend.
"""

from fastapi import FastAPI
from app_fastapi.routers import models_router, auth_router, admin_router

app = FastAPI(
    title="Data Science Demo Platform",
    description="Backend API for model training, prediction, and user management.",
    version="1.0.0"
)

app.include_router(models_router.router, prefix="/models", tags=["Models"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router.router, prefix="/auth", tags=["Admin"])


@app.get("/")
def root():
    """Root endpoint returning server status."""
    return {"message": "FastAPI server is running successfully!"}


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}