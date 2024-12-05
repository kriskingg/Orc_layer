import logging
import requests
from fastapi import HTTPException
import os

# Setup detailed logging
logging.basicConfig(
    filename="vault_integration.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load the Vault token from environment variables
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "default_vault_token")

def construct_curl_command(url, headers, payload):
    """Constructs a CURL command based on the provided URL, headers, and payload."""
    curl_cmd = f"curl --location --request POST '{url}' "
    for key, value in headers.items():
        curl_cmd += f"--header '{key}: {value}' "
    payload_str = str(payload).replace("'", '"')  # JSON objects use double quotes
    curl_cmd += f"--data-raw '{payload_str}'"
    return curl_cmd

def save_to_hashicorp(team, environment, secret_name, value):
    """Save a secret to HashiCorp Vault."""
    secret_path = f"api_1/{team}/{environment}/{secret_name}"
    url = f"http://127.0.0.1:8200/v1/secret/data/{secret_path}"
    
    headers = {
        "Authorization": f"Bearer {VAULT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"data": {"value": value}}

    expected_curl = construct_curl_command(url, headers, payload)
    logging.debug(f"Expected CURL Command: {expected_curl}")

    try:
        logging.debug("Sending POST request to Vault...")
        response = requests.post(url, headers=headers, json=payload)
        logging.debug(f"Response Status: {response.status_code}")
        logging.debug(f"Response Body: {response.text}")
        response.raise_for_status()
        logging.debug("Secret saved successfully to HashiCorp Vault.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during POST request: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving secret to HashiCorp Vault: {e}")

def fetch_from_hashicorp(team, environment, secret_name):
    """Fetch a secret from HashiCorp Vault."""
    secret_path = f"api_1/{team}/{environment}/{secret_name}"
    url = f"http://127.0.0.1:8200/v1/secret/data/{secret_path}"
    
    headers = {
        "Authorization": f"Bearer {VAULT_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        logging.debug("Sending GET request to Vault...")
        response = requests.get(url, headers=headers)
        logging.debug(f"Response Status: {response.status_code}")
        logging.debug(f"Response Body: {response.text}")
        response.raise_for_status()
        logging.debug("Secret fetched successfully from HashiCorp Vault.")
        return response.json()["data"]["data"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during GET request: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching secret from HashiCorp Vault: {e}")
