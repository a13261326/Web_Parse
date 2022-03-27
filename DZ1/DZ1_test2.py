import requests
from pprint import pprint
import json

user_id = '143181516'
access_token = '7f39788b56e80b8a3b5f394081aec4fa877ae4560c23cf916f1d3f1ac2e52ab3b2de338a81480c46720f0'
url = f'https://api.vk.com/method/groups.get?user_ids={user_id}&fields=bdate&extended=1&access_token={access_token}&v=5.131'


response = requests.get(url)
j_data = response.json()
pprint(j_data)
with open("groups.json", 'w') as fout:
    json_dumps_str = json.dumps(j_data, indent=4)
    print(json_dumps_str, file=fout)
