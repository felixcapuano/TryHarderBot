import fortnitepy
import json
import os

from discord.channel import TextChannel
from discord.ext import commands

import auth
import setup

import user


# region initialisation
# ---------------------


def get_device_auth_details():
    if os.path.isfile(setup.AUTH_FILE):
        with open(setup.AUTH_FILE, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=setup.CMD_PREFIX,
                                description='My discord + fortnite bot!',
                                case_insensitive=True
                        )
        # load extension
        for ext in startup_extensions:
            discord.load_extension(ext)

    async def on_ready():
        print("Discord bot ready to go")
    
    async def on_message(message):
        if message.author == discord.user:
            return
    
        if isTextChannel(message.channel, setup.BOT_CHANNEL):
            print('Received message from {0.author.display_name} | Content"{0.content}"'.format(message))
            await discord.process_commands(message)
    
    # region checker
    # --------------
    def admin(ctx):
        return ctx.message.author.id in setup.ADMINS
    
    def moderator(ctx):
        return ctx.message.author.id in setup.MODERATORS or admin(ctx)
    
    def isTextChannel(channel, name_channel):
        return type(channel) == TextChannel and channel.name == name_channel
    # region end

if __name__ == "__main__":
    startup_extensions = ["user"]
    
    device_auth_details = get_device_auth_details().get(auth.email, {})
    
    fortnite = fortnitepy.Client(auth=fortnitepy.AdvancedAuth(
                                                email=auth.email,
                                                password=auth.password,
                                                prompt_exchange_code=True,
                                                delete_existing_device_auths=True,
                                                **device_auth_details
                                            )
                                        )
    
    discord = commands.Bot(command_prefix=setup.CMD_PREFIX,
                                description='My discord + fortnite bot!',
                                case_insensitive=True
                        )
    
    for ext in startup_extensions:
        discord.load_extension(ext)

# region end 

# region fortnite event
# ---------------------
@fortnite.event
async def event_ready():
    print('Fortnite client ready')
    await discord.start(auth.discord_bot_token)

@fortnite.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@fortnite.event
async def event_logout():
    await discord.logout()
# region end

# region discord event
# --------------------
@discord.event
async def on_ready():
    print("Discord bot ready to go")

@discord.event
async def on_message(message):
    if message.author == discord.user:
        return

    if isTextChannel(message.channel, setup.BOT_CHANNEL):
        print('Received message from {0.author.display_name} | Content"{0.content}"'.format(message))
        await discord.process_commands(message)
# region end

# region checker
# --------------
def admin(ctx):
    return ctx.message.author.id in setup.ADMINS

def moderator(ctx):
    return ctx.message.author.id in setup.MODERATORS or admin(ctx)

def isTextChannel(channel, name_channel):
    return type(channel) == TextChannel and channel.name == name_channel
# region end

if __name__ == "__main__":
    fortnite.run()
