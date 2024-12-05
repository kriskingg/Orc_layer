import requests
import os

# Load Vault server URL and token from environment variables
VAULT_URL = os.getenv("VAULT_URL", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "default_token")

def write_secret_to_vault(secret_path, secret_data):
    """Writes a secret to the specified path in HashiCorp Vault."""
    url = f"{VAULT_URL}/v1/{secret_path}"
    headers = {
        "Authorization": f"Bearer {VAULT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "data": secret_data
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Secret written successfully.")
        return response.json()
    else:
        print(f"Failed to write secret: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    secret_path = "secret/data/myapp/config"
    secret_data = {"password": "my-super-secret-password"}
    write_secret_to_vault(secret_path, secret_data)
