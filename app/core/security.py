from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

# Load sensitive configurations from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")  # Fallback to a default if not set
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

http_bearer = HTTPBearer()

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    """Validate the provided JWT token."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # Return the username embedded in the token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
