import fortnitepy
import json
import os
import asyncio
from datetime import datetime
import time

from datetime import datetime
import discord
from discord.channel import TextChannel
from discord.ext import commands

import auth
import db
import const
from embed import embed_stats

# region initialisation
# ---------------------
def get_device_auth_details():
    if os.path.isfile(const.AUTH_FILE):
        with open(const.AUTH_FILE, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[auth.email] = details

    with open(const.AUTH_FILE, 'w') as fp:
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

discord_bot = commands.Bot(command_prefix=const.CMD_PREFIX,
                            description='My discord + fortnite bot!',
                            case_insensitive=True
                    )

setting = db.load_setting()

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
    return ctx.message.author.id in setting["admins"]

def moderator(ctx):
    return ctx.message.author.id in settings["moderators"] or admin(ctx)

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

    if isTextChannel(message.channel, const.BOT_CHANNEL):
        print('Received message from {0.author.display_name} | Content"{0.content}"'.format(message))
        await discord_bot.process_commands(message)
# region end

# region discord commands
# -----------------------
@discord_bot.command()
async def join(ctx, *, arg):
    if arg is None:
        await ctx.send("help")
        return

    profile = await fortnite_client.fetch_profile(arg)
    if profile is None:
        await ctx.send("Profile {} not found!".format(arg))
        return

    author = ctx.message.author
    msg = await ctx.send("{} select your platform :".format(author.mention))

    for emoji in const.PLATFORM.keys():
        await msg.add_reaction(emoji)

    try:
        reaction, user = await discord_bot.wait_for("reaction_add", timeout=60.0, \
                check=reply_react)
    except asyncio.TimeoutError:
        await ctx.send("Too late, retry !join command!")
        return
    finally:
        await msg.delete()
    
    if reaction.emoji not in const.PLATFORM.keys():
        await ctx.send("Sorry this platform does'nt exist, retry !join command !")
        return

    user = {
            "discord_id": author.id,
            "fornite_id": profile.id,
            "platform": const.PLATFORM[reaction.emoji]["api_key"]
        }
    
    # store in db here
    error = await db.create_user(user)
    if error is not None:
        await ctx.send(error)
        return

    await ctx.send("Welcome in the gang {}!".format(author.mention))

@join.error
async def join_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Format : !join <fortnite_username>")

@discord_bot.command()
async def up(ctx):
    user = await db.get_user(ctx.author.id)

    stats = await get_stats(*user)
    
    await rank(ctx, stats)

@discord_bot.command()
@commands.check(moderator)
async def upall(ctx, arg):
    pass

@discord_bot.command()
@commands.check(moderator)
async def rem(ctx, arg):
    await db.remove_users(arg)
    await ctx.send("User with id {} as been removed from the" \
            "database".format(arg))

@discord_bot.command()
@commands.check(admin)
async def remall(ctx):
    await db.remove_users()
    await ctx.send("All user has been removed")

@discord_bot.command()
async def stats(ctx):
    # display and update rank
    user = await db.get_user(ctx.author.id)
    if user is None:
        await ctx.send("You have to !join before {}.".format(ctx.author.mention))
        return

    date_season = datetime(*setting["season"])

    print(date_season)
    stats = await get_stats(*user, date_season=date_season)
    mbed = await embed_stats(stats, ctx.author)

    await ctx.send(embed=embed)

@discord_bot.command()
@commands.check(admin)
async def season(ctx, *arg):
    date = (int(arg[0]), int(arg[1]), int(arg[2]))
    setting["season"] = date

    await db.save_setting(setting)

async def get_stats(discord_id, profile_id, platform, date_season=None):
    stats = await fortnite_client.fetch_br_stats(profile_id, start_time=date_season)
    
    stats_raw = stats.get_stats()

    stats_formatted = {
            "KD Duo": stats.get_kd(stats_raw[platform]["defaultduo"]),
            "Matches played in duo": stats_raw[platform]["defaultduo"]["matchesplayed"],
            "KD Squad": stats.get_kd(stats_raw[platform]["defaultsquad"]),
            "Matches played in squad": stats_raw[platform]["defaultsquad"]["matchesplayed"],
            }

    print(stats_formatted)
    return stats_formatted

async def rank(ctx, stats):
    author = ctx.author
    role_squad = ""

    if stats["Matches played in squad"] >= 50:
        if 5 <= stats["KD Squad"]:
            role_squad = "Squad++++"
    elif stats["Matches played in squad"] >= 30:
        if 3.5 <= stats["KD Squad"] < 5:
            role_squad = "Squad+++"
        elif 2 <= stats["KD Squad"] < 3.5:
            role_squad = "Squad++"
        elif stats["KD Squad"] < 2:
            role_squad = "Squad+"

    if not role_squad == "":
        role = discord.utils.get(ctx.guild.roles, name=role_squad)
        if role == None:
            await author.add_roles(role)

fortnite_client.run()
