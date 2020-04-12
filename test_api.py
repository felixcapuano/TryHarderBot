import requests
import json


nickname = "ninja"
platform = "pc"

url = "https://api.fortnitetracker.com/v1/profile/"
id = "{platform}/{nickname}".format(platform=platform, nickname=nickname)
header = {"TRN-Api-Key": "2f6a79f8-875f-46b1-aa03-a2a359469c47"}

store = "https://api.fortnitetracker.com/v1/store"

request = url + id
# request = store

print(request)
response = requests.get(request, headers=header)

print(response.status_code)

stats = response.json()# ["stats"]["p2"]
data = json.dumps(stats, indent=4)
print(data)
