from typing import Dict

# In-memory user store
user_store: Dict[str, str] = {}

def add_user(username: str, hashed_password: str) -> bool:
    """Add a new user to the database."""
    if username in user_store:
        return False
    user_store[username] = hashed_password
    return True

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user by verifying their credentials."""
    from app.auth.utils import verify_password
    hashed_password = user_store.get(username)
    if not hashed_password:
        return False
    return verify_password(password, hashed_password)
