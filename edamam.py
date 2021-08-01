import requests
from flask import make_response, Response
import dotenv
import os

BASE_URL = 'https://api.edamam.com'

def get_upc(upc: str) -> Response:
    res = requests.request(
      method='GET',
      url=f'{BASE_URL}/api/food-database/v2/parser',
      params={
        'app_id': os.getenv('EDAMAM_FOOD_APP_ID'),
        'app_key': os.getenv('EDAMAM_FOOD_APP_IP_KEY'),
        'upc': upc,
      }
    )
    return make_response(
        {
          'upc': upc,
          'content': res.json(),
        },
        res.status_code
    )