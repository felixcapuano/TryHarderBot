import fortnitepy
import json
import os

from discord.channel import TextChannel
from discord.ext import commands

import const
from engine import *
from embed import *

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

# region checker
# --------------
def admin(ctx):
    return ctx.message.author.id in const.admins

def moderator(ctx):
    return ctx.message.author.id in const.moderators or admin(ctx)

def isTextChannel(channel, name_channel):
    return type(channel) == TextChannel and channel.name == name_channel
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

    if isTextChannel(message.channel, const.CHANNEL):
        print('Received message from {0.author.display_name} | Content"{0.content}"'.format(message))
        await discord_bot.process_commands(message)
# region end

# region discord commands
# -----------------------
@discord_bot.command()
async def join(ctx, *, arg):
    author = ctx.message.author
    
    # get the fornite profile of the user
    profile = await fortnite_client.fetch_profile(arg)
    if profile is not None:
        # get only used data
        formatted_stats = await get_current_stats(profile.id,
                const.platform[1])
        
        # TODO move into create user
        # format data to be stored
        data = {
                "d_id": author.id,
                "f_id": profile.id,
                "plat": const.platform[1],
                "d_w": formatted_stats["duo"]["wins"],
                "d_k": formatted_stats["duo"]["kills"],
                "d_g": formatted_stats["duo"]["games"],
                "s_w": formatted_stats["squad"]["wins"],
                "s_k": formatted_stats["squad"]["kills"],
                "s_g": formatted_stats["squad"]["games"],
                }

        # if user is exist error is not None
        error = await create_user(data)
        if error is None:
            print("create user {}".format(ctx.message.author.name)) 

            # create SUCCESS
            await ctx.send("Welcome in the Try Hard gang {} " \
                    "!".format(author.name))
            await ctx.send(embed=await embed_stats_global(author.id))
        else:
            id_existing = (str(error).split("."))[1]
            if id_existing == "fortnite_id":
                await ctx.send("This fortnite username has already been used")

            elif id_existing == "discord_id":
                await ctx.send("You have already join!")

            else:
                await ctx.send("Something goes wrong. Sorry!")
            
    else:
        await ctx.send("Aborted: Profile not found.")

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
    await remove_users()
    await ctx.send("All users has been deleted!")

@discord_bot.command()
async def stats(ctx):
    stats = await compute_stats(ctx.message.author.id)
    embed = await embed_stats(stats)
    await ctx.send(embed=embed)
# region end

# region stats
async def get_current_stats(profile_id, platform):
    stats = await fortnite_client.fetch_br_stats(profile_id)

    # TODO add platform verif
    s = stats.get_stats()[platform]
    
    user_stats = {
            "duo" : {
                "kills": s["defaultduo"]["kills"],
                "wins" : s["defaultduo"]["wins"],
                "games": s["defaultduo"]["matchesplayed"],
                },
            "squad" : {
                "kills": s["defaultsquad"]["kills"],
                "wins" : s["defaultsquad"]["wins"],
                "games": s["defaultsquad"]["matchesplayed"],
                },
            }
    return user_stats 

async def compute_stats(user_id):
    stats = {}

    user_data = await get_user(user_id)
    current_stats = await get_current_stats(user_data[1], user_data[2]) 

    duo_games_played = current_stats["duo"]["games"] - user_data[5]
    stats["duo_games"] = duo_games_played
    if not duo_games_played == 0:
        duo_killed = current_stats["duo"]["kills"] - user_data[4]

        stats["duo_kpm"] = await compute_kpm(duo_killed, duo_games_played)

    squad_games_played = current_stats["squad"]["games"] - user_data[8]
    stats["squad_games"] = squad_games_played
    if not squad_games_played == 0:
        squad_killed = current_stats["squad"]["kills"] - user_data[7]

        stats["squad_kpm"] = await compute_kpm(squad_killed, squad_games_played)

    return stats

async def compute_kpm(kills, games):
    return kills/games
# end region
fortnite_client.run()
