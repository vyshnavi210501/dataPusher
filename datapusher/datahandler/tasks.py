from celery import shared_task
import requests

@shared_task
def send_data_to_destination(url, headers, payload):
    """
    Sends JSON data to the given destination URL.
    """
    try:
        response = requests.post(url, json=payload, headers=headers)
        return {"status_code": response.status_code, "response": response.text}
    except Exception as e:
        return {"error": str(e)}
