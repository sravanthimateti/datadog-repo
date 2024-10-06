import os
import requests
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_metric(api_key, metric_name, value, tags=None):
    url = "https://api.datadoghq.com/api/v1/series"  # Update if using EU
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key
    }
    payload = {
        "series": [
            {
                "metric": metric_name,
                "points": [
                    [int(datetime.now(timezone.utc).timestamp()), value]
                ],
                "type": "count",
                "tags": tags or []
            }
        ]
    }
    logging.info(f"Sending metric: {metric_name} with value: {value} and tags: {tags}")
    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        logging.info("Metric sent successfully.")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error sending metric: {e}")
        logging.error(f"Response Content: {response.text}")
        raise

def main():
    api_key = os.getenv('DATADOG_API_KEY')
    if not api_key:
        logging.error("DATADOG_API_KEY is not set.")
        exit(1)

    workflow_name = os.getenv('GITHUB_WORKFLOW', 'unknown_workflow')
    workflow_status = os.getenv('WORKFLOW_STATUS', 'unknown_status')
    run_id = os.getenv('GITHUB_RUN_ID', 'unknown_run_id')
    run_url = os.getenv('GITHUB_RUN_URL', 'unknown_run_url')

    metric_name = "github_actions.workflow_status"
    value = 1 if workflow_status == "failure" else 0
    tags = [
        f"workflow:{workflow_name}",
        f"status:{workflow_status}",
        f"run_id:{run_id}",
        f"run_url:{run_url}"
    ]

    logging.info(f"Preparing to send metric: {metric_name}")
    send_metric(api_key, metric_name, value, tags)
    logging.info(f"Sent metric {metric_name} with value {value} and tags {tags}")

if __name__ == "__main__":
    main()
