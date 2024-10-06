# .github/scripts/send_datadog_logs.py
import os
import sys
import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_log(api_key, log_message, tags=None):
    # Determine the correct endpoint based on region
    region = os.getenv('DATADOG_REGION', 'us')
    if region == 'eu':
        url = "https://http-intake.logs.datadoghq.eu/v1/input"
    else:
        url = "https://http-intake.logs.datadoghq.com/v1/input"

    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key
    }

    payload = {
        "message": log_message,
        "ddsource": "github_actions",
        "service": "github_actions",
        "hostname": "github-actions-runner",
        "ddtags": ','.join(tags) if tags else ""
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    try:
        response.raise_for_status()
        logging.info("Log sent successfully.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error sending log: {e}")
        logging.error(f"Response Content: {response.text}")
        raise

def main():
    api_key = os.getenv('DATADOG_API_KEY')
    if not api_key:
        logging.error("DATADOG_API_KEY is not set.")
        sys.exit(1)

    # Capture logs from environment variables or arguments
    log_message = os.getenv('GITHUB_ACTIONS_LOGS', '')
    if not log_message:
        # Alternatively, capture logs from STDIN or a file
        logging.error("No log message provided to send.")
        sys.exit(1)

    # Example tags; customize as needed
    tags = [
        f"workflow:{os.getenv('GITHUB_WORKFLOW', 'unknown')}",
        f"status:{os.getenv('WORKFLOW_STATUS', 'unknown')}",
        f"run_id:{os.getenv('GITHUB_RUN_ID', 'unknown')}",
        f"run_url:{os.getenv('GITHUB_RUN_URL', '')}"
    ]

    send_log(api_key, log_message, tags)

if __name__ == "__main__":
    main()
