import fortnitepy
import json
import os

from discord.ext import commands

import const

# region initialisation
# ---------------------
def get_device_auth_details():
    if os.path.isfile(const.filename):
        with open(const.filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[const.email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

device_auth_details = get_device_auth_details().get(const.email, {})

fortnite_client = fortnitepy.Client(auth=fortnitepy.AdvancedAuth(
                                            email=const.email,
                                            password=const.password,
                                            prompt_exchange_code=True,
                                            delete_existing_device_auths=True,
                                            **device_auth_details
                                        )
                                    )

discord_bot = commands.Bot(command_prefix=const.PREFIX,
                            description='My discord + fortnite bot!',
                            case_insensitive=True
                    )
# region end 

# region fortnite event
# ---------------------
@fortnite_client.event
async def event_ready():
    print('Fortnite client ready')
    await discord_bot.start(const.discord_bot_token)

@fortnite_client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@fortnite_client.event
async def event_logout():
    await discord_bot.logout()
# region end

# region discord event
# --------------------
@discord_bot.event
async def on_ready():
    user = ctx.message.author

@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user:
        return
    
    if message.channel.name == const.CHANNEL:
        print('Received message from {0.author.display_name} | Content"{0.content}"'.format(message))
        await discord_bot.process_commands(message)
# region end

# region checker
# --------------
def admin(ctx):
    return ctx.message.author.id in const.admins

def moderator(ctx):
    return ctx.message.author.id in const.moderators or admin(ctx)
# region end

# region discord commands
# -----------------------
@discord_bot.command()
async def join(ctx):
    print(ctx.message.content)

@discord_bot.command()
async def up(ctx):
    pass

@discord_bot.command()
@commands.check(moderator)
async def upall(ctx):
    pass

@discord_bot.command()
@commands.check(moderator)
async def rem(ctx):
    print("slt")

@discord_bot.command()
@commands.check(admin)
async def remall(ctx):
    print("delall")
# region end

fortnite_client.run()
