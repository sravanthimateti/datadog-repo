import os
import requests
from datetime import datetime, timezone

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
    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        print("Metric sent successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"Error sending metric: {e}")
        print(f"Response Content: {response.text}")
        raise

def main():
    api_key = os.getenv('DATADOG_API_KEY')
    if not api_key:
        print("DATADOG_API_KEY is not set.")
        exit(1)

    metric_name = "test.metric"
    value = 1
    tags = ["test:integration"]

    send_metric(api_key, metric_name, value, tags)
    print(f"Sent metric {metric_name} with value {value} and tags {tags}")

if __name__ == "__main__":
    main()
