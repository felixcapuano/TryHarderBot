

async def create_user(ctx, ig_name, platform):
    user = ctx.message.author
    
    print("create user {}".format(user.name)) 
    users = await discord.get_users()

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

