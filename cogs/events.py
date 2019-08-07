import discord
from discord.ext import commands
from discord.utils import get
import os
import psycopg2
import asyncio
import json
import dotenv

dotenv.load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gods = (267667599666446336, 490275541413265409,
                     599507281226367006, 580593494469640207)
        self.reactions = ('👍', '👎')

    async def remove_all_roles(self, user):
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        if ctx.bot:
            channel = get(ctx.guild.channels, id=conf[0][10])
            c.execute(f"SELECT * FROM bots WHERE id = {ctx.id}")
            rows = c.fetchall()
            if rows == []:
                channel = get(ctx.guild.channels, id=conf[0][10])
                await channel.send(f"An admin has attempted to add the bot `{ctx.name}` to this server that is unauthorised. To authorize it, type `>authorize {ctx.id} {ctx.name}` {ctx.guild.owner.mention} <@599507281226367006>")
                await ctx.guild.kick(ctx, reason="Unauthorised Bot")
            else:
                await channel.send(f"An admin has attempted to add the bot `{ctx.name}` to the server succesfully. {ctx.guild.owner.mention} <@599507281226367006>")
                role = get(ctx.guild.roles, id=conf[0][4])
                await ctx.add_roles(role)
        else:
            channel = get(ctx.guild.channels, id=conf[0][2])
            c.execute(f"SELECT * FROM users WHERE user_id = {ctx.id};")
            rows = c.fetchall()
            if rows == []:
                c.execute(f"INSERT INTO users VALUES({ctx.id}, 'False');")
            c.execute(f"SELECT prison FROM users WHERE user_id = {ctx.id};")
            rows = c.fetchall()
            if 'True ' in rows[0]:
                await asyncio.sleep(1)
                await self.remove_all_roles(ctx)
                role = get(ctx.guild.roles, id=conf[0][7])
                await ctx.add_roles(role)
            else:
                await channel.send(f'{conf[0][1]}'.format(ctx.mention))
                role = get(ctx.guild.roles, id=conf[0][3])
                await ctx.add_roles(role)
            conn.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def authorize(self, ctx, uid, *, name):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        if ctx.author.id in self.gods:
            channel = get(ctx.guild.channels, id=conf[0][10])
            c.execute(f"SELECT * FROM bots WHERE id = {uid}")
            rows = c.fetchall()
            if rows == []:
                c.execute(
                    f"INSERT INTO bots VALUES({uid}, '{name}', '{ctx.author.name}')")
                await channel.send(f"{ctx.author.name} has authorised the bot `{name}` to be allowed into the server.")
            else:
                await channel.send("This bot has already been authorised to enter the server.")
        else:
            await ctx.send("You do not have the permission to use this command.")
        conn.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        if ctx.bot:
            channel = get(ctx.guild.channels, id=conf[0][10])
            await channel.send(f"An admin has removed the bot `{ctx.name}` from the server.")
        else:
            channel = get(ctx.guild.channels, id=conf[0][6])
            await channel.send(f"{conf[0][5]}".format(ctx.name))

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


def setup(bot):
    bot.add_cog(Events(bot))
