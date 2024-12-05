import bcrypt
import jwt
from datetime import datetime, timedelta
from os import getenv

SECRET_KEY = getenv("JWT_SECRET_KEY", "default-secret-key")  # Fallback to a default if not set
ALGORITHM = getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRE_MINUTES = int(getenv("JWT_EXPIRE_MINUTES", 60))

def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(username: str) -> str:
    """Generate a JWT token."""
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    """Verify a JWT token."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")
