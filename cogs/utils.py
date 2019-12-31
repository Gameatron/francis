import discord
from discord.ext import commands
from discord.utils import get as discget
from conf import Conf
import psycopg2
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaders = [599507281226367006, 267667599666446336]

    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=('purge', 'clean', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount: int):
        await ctx.message.delete()
        await self.clear(ctx, amount)
        await ctx.send(f"Cleared {amount} messages!", delete_after=5)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx, message, *, role: discord.Role):
        await ctx.message.delete()
        try:
            await role.edit(reason='Temp ping.', mentionable=True)
            await ctx.send(f"{role.mention}\n{message}")
            await role.edit(reason="Temp ping.", mentionable=False)
        except discord.ext.commands.errors.BadArgument:
            await ctx.send(f"That is not a valid role name. (Capitilization matters!)", delete_after=5)

    @commands.command()
    async def servers(self, ctx):
        em = discord.Embed(
            color=0xFF0000, title="List of all Serves:")
        for item in self.bot.guilds:
            em.add_field(
                name=item.name, value=f"{len(list(item.members))} members", inline=False)
        em.add_field(name="Total number of members currently seen:",
                     value=len(list(self.bot.get_all_members())))
        await ctx.send(embed=em)

    @commands.command()
    async def server(self, ctx):
        if ctx.author.id in self.leaders:
            await ctx.message.delete()
            c.execute("SELECT * FROM guilds")
            rows = c.fetchall()
            allowed = rows[0]
            for guild in self.bot.guilds:
                if not guild.id in allowed:
                    await guild.leave()
                    await ctx.send(f"Left the server `{guild.name}'")
        else:
            print("You do not have the permission to use this command.")

    @commands.command()
    async def add_server(self, ctx, sid):
        await ctx.message.delete()
        if ctx.author.id in self.leaders:
            c.execute(f"INSERT INTO guilds VALUES({int(sid)})")
            conn.commit()
        else:
            print("You do not have the permission to use this command.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bots(self, ctx):
        em = discord.Embed(color=0xFF0000, title="All authorised bots:")
        c.execute("SELECT * FROM bots")
        rows = c.fetchall()
        if rows == []:
            await ctx.send("No bots have been authorised.")
            return
        for row in rows:
            em.add_field(
                name=row[1], value=f"Bot ID: {row[0]}\nAuthorised by: {row[2]}", inline=False)
        await ctx.send(embed=em)

    @commands.command()
    async def mortis_update(self, ctx):
        if ctx.author.id in self.leaders:
            for guild in self.bot.guilds:
                channel = discget(guild.channels, name='mortis-imperium')
                await channel.send("Test Message.")
        else:
            print("You do not have permission to use this command.")

    @commands.command()
    async def directors(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(
            color=0xFF0000, title="All Current Leaders of Mortis Imperium:")
        for user in self.leaders:
            user = self.bot.get_user(user)
            em.add_field(name=user.name,
                         value=f"User: {user.mention}")
        await ctx.send(embed=em)

    @commands.command()
    async def mortis_announce(self, ctx,  *, message):
        if ctx.author.id in self.leaders:
            for guild in self.bot.guilds:
                channel = discget(guild.channels, name='mortis-imperium')
                await channel.send(f"New Mortis Announcement!\n\nSent By: {ctx.author.mention}\nMessage:\n{message}")
        else:
            await ctx.send("You lack the permissions to use this command.")

    @commands.command()
    async def ab(self, ctx, *, role: discord.Role):
        for user in ctx.guild.members:
             try:
                 await user.add_roles(role)
             except:
                 pass
    
    @commands.command()
    async def ppurge(self, ctx):
        if ctx.author.id in self.leaders:
            for member in ctx.guild.members:
    #            roles = []
                for role in member.roles:
                    if not member.id in self.leaders:
                        try:
                            await member.remove_roles(role)
                        except:
                            pass
      #              roles.append(role.id)
      #              c.execute("INSERT INTO eco VALUES(member.id, roles, 0)")
            await ctx.send("done, now purge and type >readd to add everyone's roles back.")

    @commands.command()
    async def readd(self, ctx):
        try:
            if ctx.author.id in self.leaders:
                c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
                conf = Conf(c.fetchall()[0])
                role = discget(ctx.guild.roles, id=conf.joinrole)
                for member in ctx.guild.members:
                    try:
                        member.add_roles(role) 
                    except:
                        pass
                await ctx.send("Done.", delete_after=5)
        except:
            await ctx.send("there was an error while i was readding roles.", delete_after=5)
                

def setup(bot):
    bot.add_cog(Utils(bot))
