import json


usersFile = "users.json"
user = "felix"

stats = {"ig_name": "Mammoth", "tnr": "1"}

with open(usersFile, "r") as usersJson:
    users = json.load(usersJson)
print(users)
with open(usersFile, "w") as usersJson:
    json.dump(users, usersJson, indent=4, sort_keys=True)
