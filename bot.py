import fortnitepy
import json
import os
import asyncio

from datetime import datetime
from discord.channel import TextChannel
from discord.ext import commands

import auth
import db
import setup

# region initialisation
# ---------------------

def get_device_auth_details():
    if os.path.isfile(setup.AUTH_FILE):
        with open(setup.AUTH_FILE, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[auth.email] = details

    with open(setup.AUTH_FILE, 'w') as fp:
        json.dump(existing, fp)

device_auth_details = get_device_auth_details().get(auth.email, {})

fortnite_client = fortnitepy.Client(auth=fortnitepy.AdvancedAuth(
                                            email=auth.email,
                                            password=auth.password,
                                            prompt_exchange_code=True,
                                            delete_existing_device_auths=True,
                                            **device_auth_details
                                        )
                                    )

discord_bot = commands.Bot(command_prefix=setup.CMD_PREFIX,
                            description='My discord + fortnite bot!',
                            case_insensitive=True
                    )
# region end 

# region fortnite event
# ---------------------
@fortnite_client.event
async def event_ready():
    print('Fortnite client ready')
    await discord_bot.start(auth.discord_bot_token)

@fortnite_client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@fortnite_client.event
async def event_logout():
    await discord_bot.logout()
# region end

# region checker
# --------------
def admin(ctx):
    return ctx.message.author.id in setup.ADMINS

def moderator(ctx):
    return ctx.message.author.id in setup.MODERATORS or admin(ctx)

def isTextChannel(channel, name_channel):
    return type(channel) == TextChannel and channel.name == name_channel

def reply_react(reaction, user):
    return user.id == reaction.message.mentions[0].id
# region end

# region discord event
# --------------------
@discord_bot.event
async def on_ready():
    print("Discord bot ready to go")

@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user:
        return

    if isTextChannel(message.channel, setup.BOT_CHANNEL):
        print('Received message from {0.author.display_name} | Content"{0.content}"'.format(message))
        await discord_bot.process_commands(message)
# region end

# region discord commands
# -----------------------
@discord_bot.command()
async def join(ctx, *, arg):
    profile = await fortnite_client.fetch_profile(arg)
    if profile is None:
        await ctx.send("Profile {} not found!")
        return

    author = ctx.message.author
    msg = await ctx.send("{} select your platform :".format(author.mention))

    for emoji in setup.PLATFORM.keys():
        await msg.add_reaction(emoji)

    try:
        reaction, user = await discord_bot.wait_for("reaction_add", timeout=60.0, \
                check=reply_react)
    except asyncio.TimeoutError:
        await ctx.send("Too late, retry !join command!")
        return
    finally:
        await msg.delete()
    
    user = {
            "discord_id": author.id,
            "fornite_id": profile.id,
            "platform": setup.PLATFORM[reaction]["index"]
        }
    
    # store in db here
    print(user)
    error = await db.create_user(user)
    if error is not None:
        await ctx.send(error)
        return

    await ctx.send(await db.get_user(author.id))

@discord_bot.command()
async def up(ctx, arg):
    # display and update rank
    pass

@discord_bot.command()
@commands.check(moderator)
async def upall(ctx):
    pass

@discord_bot.command()
@commands.check(moderator)
async def rem(ctx):
    pass

@discord_bot.command()
@commands.check(admin)
async def remall(ctx):
    pass

@discord_bot.command()
async def stats(ctx):
    pass
# region end

fortnite_client.run()
