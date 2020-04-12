import discord
import json
import requests

class TryHarderBot(discord.Client):

    CHANNEL = "try-hard"
    PREFIX = "!"
    
    USERS = "users.json"

    admins = [421801671237042176]
    moderators = []

    URL = "https://api.fortnitetracker.com/v1/profile/{platform}/{name}"
    FN_TRACKER_KEY = {"TRN-Api-Key": "2f6a79f8-875f-46b1-aa03-a2a359469c47"}

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))
            
    
    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.channel.name == self.CHANNEL and (message.content)[0] == self.PREFIX:

            print("[{}] {}".format(message.author.name, message.content))
            
            if message.author.id in self.admins + self.moderators:
                await self.admin_command(message)
            
            await self.user_command(message)

    async def user_command(self, message):
        cmd = (message.content)[1:].split(" ")

        if cmd[0] in ["join"]:
            if len(cmd) == 3 and cmd[1] in ["pc","xb1","psn"]:
                # create user profile
                await self.create_user(message, cmd[2], cmd[1])
            else:
                await message.channel.send("format : !join <platform> <in_game_name>")
        elif cmd[0] in ["upgrade", "up"]:
            # update info
            pass
        elif cmd[0] in ["stats"]:
            # display stats
            pass
        elif cmd[0] in ["help"]:
            pass
        elif cmd[0] in ["quit"]:
            await self.delete_user(message)

    async def admin_command(self, message):
        cmd = (message.content)[1:].split(" ")

        if cmd[0] in ["upall", "updateall"]:
            pass
        elif cmd[0] in ["deleteall", "delall"]:
            await self.set_users({})
            await message.channel.send("All users has been deleted!")
        elif cmd[0] in ["stop"]:
            await message.channel.send("Goodbye !")
            await client.logout()
            print("stop")

    async def create_user(self, message, ig_name, platform):
        user = message.author
        
        print("create user {}".format(user.name)) 
        users = await self.get_users()

        # check user existence
        if not str(user.id) in users.keys():
        
            kpg_solo, kpg_duo, kpg_squad, status = await self.get_kpg(platform, ig_name)
            print("status : ", status)

            if not None in [kpg_solo, kpg_duo, kpg_squad]:
                stats = {
                            "ig_name": ig_name,
                            "kpg_solo": kpg_solo,
                            "kpg_duo": kpg_duo,
                            "kpg_squad": kpg_squad,
                        }
        
                users[str(user.id)] = stats
                
                await self.set_users(users)
                await message.channel.send("User number {} has been " \
                        "created.".format(message.author.id))
                await message.channel.send(stats)
            else:
                await message.channel.send("Error : ".format(status))
        else:
            await message.channel.send("User number {} is already " \
                    "created.".format(message.author.id))

    
    async def delete_user(self, message):
        users = await self.get_users()
        
        # check user existence
        if str(message.author.id) in users.keys():
            del users[str(message.author.id)]

            await self.set_users(users)
            await message.channel.send("User number {} has been" \
                        "delete.".format(message.author.id))
        else:
            await message.channel.send("You have to join before")

    async def set_users(self, users):
        with open(self.USERS, "w") as usersJson:
            json.dump(users, usersJson, separators=(',', ':'))

    async def get_users(self):
        with open(self.USERS, "r") as usersJson:
            users = json.load(usersJson)
        return users
    
    async def get_kpg(self, platform, ig_name):
        url = self.URL.format(platform=platform, name=ig_name)

        response = requests.get(url, headers=self.FN_TRACKER_KEY)

        if response.status_code == 200:
            stats = (response.json())["stats"]
            kpg_solo = stats["p2"]["kpg"]["valueDec"]
            kpg_duo = stats["p10"]["kpg"]["valueDec"]
            kpg_squad = stats["p9"]["kpg"]["valueDec"]
        else:
            kpg_solo = None
            kpg_duo = None
            kpg_squad = None
        return kpg_solo, kpg_duo, kpg_squad, response.status_code

discord_key = 'Njk4NjQ2Nzg1MjgyODAxNjc0.XpI5Sw.fmXoM9Ks2ztm_g1coxcVlDWhrDY'

client = TryHarderBot()
client.run(discord_key)

