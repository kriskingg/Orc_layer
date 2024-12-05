import os

# Load Vault token from environment variable
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "default_token_if_none_provided")

print(f"Loaded Vault Token: {VAULT_TOKEN}")
