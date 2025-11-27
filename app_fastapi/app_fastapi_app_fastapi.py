# File: Final_Project_v003/app_fastapi/app_fastapi_app_fastapi.py
# uvicorn app_fastapi.app_fastapi:app --reload --port 8000
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app_fastapi.routers import models_router, auth_router

# Create FastAPI instance
app = FastAPI(
    title="Data Science Demo Platform",
    description="Backend API for model training, prediction, and user management.",
    version="1.0.0"
)

# Define custom OpenAPI schema to add security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token from /auth/login"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(models_router.router, prefix="/models", tags=["Models"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI server is running successfully!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}