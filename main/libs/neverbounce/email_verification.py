import requests
from main.config import config
from main import errors
import json

NEVERBOUNCE_EMAIL_VERFICATION_URL = 'https://api.neverbounce.com/v4/single/check?key={}&email={}'


def validate_email(email):
    try:
        api_response = requests.post(
            NEVERBOUNCE_EMAIL_VERFICATION_URL.format(config.NEVERBOUNCE_API_KEY, email)
        ).content
        api_response = json.loads(api_response)
    except Exception:
        raise Exception('There is an error connnecting to NeverBounce server.')

    if api_response['result'] == 'invalid':
        raise errors.InvalidEmail
