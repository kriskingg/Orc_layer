from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.core.load_balancer import assign_backend
from app.core.database import store_metadata, get_backend
from app.secrets.backends import save_to_hashicorp, fetch_from_hashicorp
import os

# APIRouter for secrets
secret_router = APIRouter()

# Request model for creating a secret
class SecretPayload(BaseModel):
    value: str

@secret_router.post("/{api_name}/{team}/{environment}/{secret_name}")
async def create_secret(
    api_name: str,  # Adjust to include API name in the path
    team: str,
    environment: str,
    secret_name: str,
    payload: SecretPayload,
    request: Request  # For additional logging
):
    """
    Create a secret in HashiCorp Vault.
    """
    try:
        # Log incoming request details for debugging
        print(f"Incoming POST Request Path: {request.url.path}")

        # Decide backend dynamically based on load balancer or other logic
        backend = assign_backend()

        # Create a path for the secret to store metadata
        path = f"{api_name}/{'app_1' if backend == 'hashi' else 'app_2'}/{team}/{environment}/{secret_name}"

        # Handle HashiCorp Vault
        if backend == "hashi":
            result = save_to_hashicorp(team, environment, secret_name, payload.value)
        else:
            raise HTTPException(
                status_code=400,
                detail="Currently, only HashiCorp Vault is supported for secret storage"
            )

        # Store metadata (secret path and backend)
        store_metadata(path, backend)

        return {
            "path": path,
            "message": "Secret created successfully",
            "backend_response": result,
        }
    except HTTPException as http_err:
        # Reraise HTTPException for known errors
        print(f"HTTP Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        # Catch any other errors and return a 500 internal server error
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating secret: {e}")

@secret_router.get("/{api_name}/{path:path}")
async def get_secret(api_name: str, path: str, request: Request):
    """
    Fetch a secret from HashiCorp Vault.
    """
    try:
        # Log incoming request details for debugging
        print(f"Incoming GET Request Path: {request.url.path}")

        # Get backend from metadata
        backend = get_backend(path)

        # If backend is not found, raise 404 error
        if not backend:
            raise HTTPException(status_code=404, detail="Secret not found")

        # Handle fetching the secret from HashiCorp Vault
        if backend == "hashi":
            result = fetch_from_hashicorp(path)
        else:
            raise HTTPException(
                status_code=400,
                detail="Currently, only HashiCorp Vault is supported for secret retrieval"
            )

        return result
    except HTTPException as http_err:
        # Reraise HTTPException for known errors
        print(f"HTTP Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        # Catch any other errors and return a 500 internal server error
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching secret: {e}")
