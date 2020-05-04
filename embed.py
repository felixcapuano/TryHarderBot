import discord
from discord import Embed


async def embed_stats(stats, author):

    title = "{} statistics".format("TEST")
    des = "This the {} statistique.".format(author.mention)

    embed = discord.Embed(title=title, description=des, color=0xff0000)

    for category, value in stats.items():
        embed.add_field(name=category, value=value, inline=True)

    return embed 
