import discord


class TryHarderBot(discord.Client):

    PREFIX = "!"

    admins = [421801671237042176]
    moderators = []

    async def on_ready(self):
            print('We have logged in as {0.user}'.format(client))
    
    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.channel.name == "try-hard" and (message.content)[0] == self.PREFIX:
            print(type(message.author.id))
            print(message.author.name == self.admins[0])

            print("message : ", message.content)
            
            if message.author.id in self.admins + self.moderators:
                await self.admin_command(message)
            
            await self.user_command(message)

    async def user_command(self, message):
        cmd = (message.content)[1:].split(" ")

        if cmd[0] in ["add"]:
            pass
        elif cmd[0] in ["upgrade", "up"]:
            pass
        elif cmd[0] in ["info"]:
            pass
        elif cmd[0] in ["help"]:
            pass

    async def admin_command(self, message):
        cmd = (message.content)[1:].split(" ")

        if cmd[0] in ["upall", "updateall"]:
            pass
        elif cmd[0] in ["quit", "q"]:
            await client.logout()
            print("quit")

client = TryHarderBot(command_prefix=":")
client.run('Njk4NjQ2Nzg1MjgyODAxNjc0.XpI5Sw.fmXoM9Ks2ztm_g1coxcVlDWhrDY')
