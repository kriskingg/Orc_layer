from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from app.auth.utils import verify_token
from app.auth.routes import auth_router
from app.secrets.routes import secret_router
from app.core.database import init_db
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import os

# Load log file path from environment variable
LOG_FILE = os.getenv("LOG_FILE_PATH", "vault_integration.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize FastAPI application
app = FastAPI(title="Orchestration Layer API", version="1.0")

# Initialize the database
init_db()

# Security Dependency
security = HTTPBearer()

def authenticate_request(credentials: HTTPBearer = Depends(security)):
    """
    Middleware to authenticate requests using the provided token.
    Tokens are verified using the `verify_token` utility function.
    """
    token = credentials.credentials
    if not token:
        logging.warning("Token missing in request.")
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        verify_token(token)
        logging.info("Token successfully verified.")
    except Exception as e:
        logging.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

# Include Routers
# Authentication routes (do not require token authentication)
app.include_router(auth_router, prefix="/api/v1/orc/auth", tags=["Authentication"])

# Secrets routes (protected by token authentication)
app.include_router(
    secret_router,
    prefix="/api/v1/orc/secrets",
    tags=["Secrets"],
    dependencies=[Depends(authenticate_request)]
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    logging.info("Health check endpoint called.")
    return {"status": "up"}
