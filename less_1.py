# Задание 1

import requests
from pprint import pprint
import json

url = "https://api.github.com/users/"
user = "Linear777"
response = requests.get(f'{url}{user}/repos')
j_data = response.json()
repos = {'name': []}
for i in j_data:
    repos['name'].append(i['name'])
with open('repos_file.json', 'w') as file:
    json.dump(repos, file)
pprint(repos['name'])
