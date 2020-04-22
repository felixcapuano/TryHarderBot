import const
from discord import Embed
from engine import get_user


async def embed_stats_global(user_id):
    u = await get_user(user_id)

    title = "Global Statistics [{}]".format(u[2])
    description = "This is your globals statistics."
    embed = Embed(title=title, description=description)

    embed.add_field(name="Duo wins:", value=u[3], inline=True)
    embed.add_field(name="Duo kills:", value=u[4], inline=True)
    embed.add_field(name="Duo matches played:", value=u[5], inline=True)
    embed.add_field(name="Squad wins:", value=u[6], inline=True)
    embed.add_field(name="Squad kills:", value=u[7], inline=True)
    embed.add_field(name="Squad matches played:", value=u[8], inline=True)

    return embed 

async def embed_stats(stats):

    title = "Statistics"
    description = "These are your statistics since you joined us!" \
                "You have to play {} get a grade.".format(const.min_game)
    embed = Embed(title=title, description=description)
    
    try:
        embed.add_field(name="Duo kill per matches:", value=stats["duo_kpm"], inline=False)
    except KeyError:
        embed.add_field(name="Duo kill per matches:", value="NULL", inline=False)

    embed.add_field(name="Duo matches played:", value=stats["duo_games"], inline=True)

    try:
        embed.add_field(name="Squad kill per matches:", value=stats["squad_kpm"], inline=False)
    except KeyError:
        embed.add_field(name="Squad kill per matches:", value="NULL", inline=False)

    embed.add_field(name="Squad matches played:", value=stats["squad_games"], inline=True)

    return embed 
