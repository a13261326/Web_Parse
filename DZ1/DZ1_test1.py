from github import Github
import json

n = 0
repos = {}
username = "a13261326"
g = Github()
user = g.get_user(username)
for repo in user.get_repos():
    n += 1
    repos[repo.name] = n

with open("repos.json", 'w') as fout:
    json_dumps_str = json.dumps(repos, indent=4)
    print(json_dumps_str, file=fout)
