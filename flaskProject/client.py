import requests
import json
from scraper import serialized_players

url = 'http://localhost:5000/players'
response = requests.post(url, json=serialized_players)

if response.status_code == 200:
    print('POST request successful')
    # Handle the processed data as needed
else:
    print('POST request failed')
    # Handle the failed request
