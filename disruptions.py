import requests
import json
import os
import datetime

# import apiKey from .env
from dotenv import load_dotenv
load_dotenv()

HOST = 'https://prim.iledefrance-mobilites.fr/'
BASE_PATH = 'marketplace/navitia/'
API_KEY = os.getenv('API_KEY')

# Get all line reports
def get_line_reports(page=0):
    url = f'{HOST}{BASE_PATH}coverage/fr-idf/lines'
    params = {
        'disable_disruption': 'true',
        'count': 1000,
        'start_page': page
    }
    headers = {'apiKey': API_KEY} if API_KEY else None
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)
    line_list = []
    for line in response.json()['lines']:
        if line['physical_modes'][0]['name'] == 'Métro':
            # details = {
            #     'id': line['id'],
            #     'name': line['name'],
            #     'code': line['code']
            # }
            details = line
            line_list.append(details)
    return line_list

# Get all traffic information
def get_message_info_traffic():
    path = 'v1/tr-messages-it'
    params = {
        'LineRef': 'ALL'
    }
    headers = {'apiKey': API_KEY} if API_KEY else None
    url = f'{HOST}{path}'
    response = requests.get(url, params=params, headers=headers)
    print(response)
    write_to_file(response.json(), 'message_info_traffic.json')


def get_real_time_stop():
    path = 'marketplace/stop-monitoring'
    params = {
        'MonitoringRef': 'STIF:StopPoint:Q:463158:'
    }
    url = f'{HOST}{path}'
    headers = {'apiKey': API_KEY} if API_KEY else None
    response = requests.get(url, params=params, headers=headers)
    write_to_file(response.json(), 'traffic_information.json')

def get_reports_by_line(lines):
    disruptions = []

    for line in lines:
        url = f'{HOST}{BASE_PATH}coverage/fr-idf/lines/{line["id"]}/line_reports'
        headers = {'apiKey': API_KEY} if API_KEY else None
        response = requests.get(url, headers=headers)
        print(response.status_code)

        
        for disruption in response.json()['disruptions']:
            if disruption['status'] == 'active':
                if not any(tag in disruption['tags'] for tag in ['Ascenseur']):
                    disruptions.append(disruption)
    
    return disruptions

# write dict to file
def write_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False))
            file.write('\n')
        
        

if __name__ == '__main__':
    lines = get_line_reports()
    lines += get_line_reports(1)
    write_to_file(lines, 'lines.json')
    disruptions = get_reports_by_line(lines)
    print("nb d'incidents: ", len(disruptions))
    file_name = f'/app/data/disruptions_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.ndjson'
    write_to_file(disruptions, file_name)
    # get_message_info_traffic()