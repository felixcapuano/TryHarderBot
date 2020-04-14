import pprint
import fortnitepy
import json
import os

email = 'felix.capuano@gmail.com'
password = 'FelixDouce2615'
filename = 'device_auths.json'

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)


device_auth_details = get_device_auth_details().get(email,{})
client = fortnitepy.Client(
            auth=fortnitepy.AdvancedAuth(
                email=email,
                password=password,
                prompt_exchange_code=True,
                delete_existing_device_auths=True,
                **device_auth_details
            )
        )
@client.event
async def event_device_auth_generate(details,email):
    store_device_auth_details(email, details)

@client.event
async def event_ready():
    print('----------------')
    print('Client ready as')
    print(client.user.display_name)
    print(client.user.id)
    print('----------------')

    await get_ninja_kd()

@client.event
async def event_friend_request(request):
    await request.accept()

@client.event
async def event_friend_message(message):
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))
    await message.reply('Thanks for your message!')

async def get_ninja_kd():
    profile = await client.fetch_profile("M\u039bMMOTH")
    stats = await client.fetch_br_stats(profile.id)

#     pprint.pprint((stats.get_stats())["keyboardmouse"])
    s = (stats.get_stats())["keyboardmouse"]
    
    for wins in s.keys():
        if "squads" in wins:
            try:
                print(s[wins]['wins'])
            except:
                pass

client.run()


