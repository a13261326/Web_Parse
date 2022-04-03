import requests
from pprint import pprint
import json

user_id = '143181516'
access_token = ''
url = f'https://api.vk.com/method/groups.get?user_ids={user_id}&fields=bdate&extended=1&access_token={access_token}&v=5.131'


response = requests.get(url)
j_data = response.json()
pprint(j_data)
with open("groups.json", 'w') as fout:
    json_dumps_str = json.dumps(j_data, indent=4)
    print(json_dumps_str, file=fout)
