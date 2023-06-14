import requests
import json
import os

# import apiKey from .env
from dotenv import load_dotenv
load_dotenv()

HOST = 'https://prim.iledefrance-mobilites.fr/'
BASE_PATH = 'marketplace/navitia/line_reports'
API_KEY = os.getenv('API_KEY')

# Get all line reports
def get_line_reports():
    url = f'{HOST}{BASE_PATH}/coverage/fr-idf/line_reports'
    headers = {'apiKey': API_KEY} if API_KEY else None
    response = requests.get(url, headers=headers)
    write_to_file(response.json(), 'line_reports.json')
    return response.json()

# Get all traffic information
def get_all_traffic_information():
    path = 'marketplace/stop-monitoring'
    params = {
        'MonitoringRef': 'STIF:StopPoint:Q:463158:'
    }
    url = f'{HOST}{path}'
    response = requests.get(url, params=params, headers={'apiKey': API_KEY})
    write_to_file(response.json(), 'traffic_information.json')

# # write dict to file
def write_to_file(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)
        
        

if __name__ == '__main__':
    # get_line_reports()
    get_all_traffic_information()