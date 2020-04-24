from discord.ext import commands

import bot


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hey(self, ctx, arg):
        # profile = await bot.bot_fn.fetch_profile(arg)
        print(profile)
#        profile = await bot.fn_client.fetch_profile(arg)
#        await ctx.send(profile.id)


# @bot.discord.command()
# async def join(ctx, *, arg):
#     author = ctx.message.author
#     
#     # get the fornite profile of the user
#     profile = await bot.fortnite.fortnite_client.fetch_profile(arg)
#     if profile is not None:
#         # get only used data
#         formatted_stats = await bot.fortnite.get_current_stats(profile.id,
#                  "keyboardmouse")
#         
#         # TODO move into create user
#         # format data to be stored
#         data = {
#                 "d_id": author.id,
#                 "f_id": profile.id,
#                 "plat": "keyboardmouse",
#                 "d_w": formatted_stats["duo"]["wins"],
#                 "d_k": formatted_stats["duo"]["kills"],
#                 "d_g": formatted_stats["duo"]["games"],
#                 "s_w": formatted_stats["squad"]["wins"],
#                 "s_k": formatted_stats["squad"]["kills"],
#                 "s_g": formatted_stats["squad"]["games"],
#                 }
# 
#         # if user is exist error is not None
#         error = await create_user(data)
#         if error is None:
#             print("create user {}".format(ctx.message.author.name)) 
# 
#             # create SUCCESS
#             await ctx.send("Welcome in the Try Hard gang {} " \
#                     "!".format(author.name))
#             await ctx.send(embed=await embed_stats_global(author.id))
#         else:
#             id_existing = (str(error).split("."))[1]
#             if id_existing == "fortnite_id":
#                 await ctx.send("This fortnite username has already been used")
# 
#             elif id_existing == "discord_id":
#                 await ctx.send("You have already join!")
# 
#             else:
#                 await ctx.send("Something goes wrong. Sorry!")
#             
#     else:
#         await ctx.send("Aborted: Profile not found.")
# 
# @bot.discord.command()
# @commands.check(moderator)
# async def rem(ctx):
#     print("slt")
# 
# @bot.discord.command()
# @commands.check(admin)
# async def remall(ctx):
#     await remove_users()
#     await ctx.send("All users has been deleted!")

def setup(bot):
    bot.add_cog(User(bot))
