import discord
from discord import Embed


async def embed_stats(stats, author):

    title = "{} statistics".format("TEST")
    des = "This the {} statistique.".format(author.mention)

    embed = discord.Embed(title=title, description=des, color=0xff0000)

    for category, value in stats.items():
        embed.add_field(name=category, value=value, inline=True)

    return embed 

async def embed_help():
    embed = discord.Embed(title="Help")
    
    embed.add_field(name="!join <pseudo_fortnite>", value="Used to register " \
            "your fortnite account.", inline=False)

    embed.add_field(name="!up", value="Used to update your rank.", inline=False)

    embed.add_field(name="!upall", value="Used to update rank to all users.", inline=False)

    embed.add_field(name="!stats", value="Used to display your stats.", inline=False)
    
    embed.add_field(name="!rem <discord_id>", value="Use to remove a user from the database.", inline=False)

    embed.add_field(name="!remall", value="Used to remove all user from the" \
            "database", inline=False)

    embed.add_field(name="!season <year> <month> <day>", value="Used to modify the season date", inline=False)

    return embed

