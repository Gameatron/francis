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
        self.gods = (267667599666446336, 599507281226367006)
        self.reactions = ('👍', '👎')

    async def remove_all_roles(self, user):
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        if ctx.bot:
            channel = get(ctx.guild.channels, name='mod-log')
            c.execute(f"SELECT * FROM bots WHERE id = {ctx.id}")
            rows = c.fetchall()
            if rows == []:
                channel = get(ctx.guild.channels, name='mod-log')
                await channel.send(f"An admin has attempted to add the bot `{ctx.name}` to this server that is unauthorised. To authorize it, type `>authorize {ctx.id} {ctx.name}` <@599507281226367006> <@267667599666446336>")
                await ctx.guild.kick(ctx, reason="Unauthorised Bot")
            else:
                await channel.send(f"An admin has attempted to add the bot `{ctx.name}` to the server succesfully. <@599507281226367006> <@267667599666446336>")
                role = get(ctx.guild.roles, name='Bot')
                await ctx.add_roles(role)
        else:
            channel = get(ctx.guild.channels, name="entry-exit")
            c.execute(f"SELECT * FROM users WHERE user_id = {ctx.id};")
            rows = c.fetchall()
            if rows == []:
                c.execute(f"INSERT INTO users VALUES({ctx.id}, 'False');")
            c.execute(f"SELECT prison FROM users WHERE user_id = {ctx.id};")
            rows = c.fetchall()
            if 'True ' in rows[0]:
                await asyncio.sleep(1)
                await self.remove_all_roles(ctx)
                role = get(ctx.guild.roles, name='Immigrant')
                await ctx.add_roles(role)
            else:
                await channel.send(f"{ctx.mention} has joined.")
                role = get(ctx.guild.roles, name='Immigrant')
                await ctx.add_roles(role)
            conn.commit()
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def authorize(self, ctx, uid, *, name):
        if ctx.author.id in self.gods:
            channel = get(ctx.guild.channels, name="mod-log")
            c.execute(f"SELECT * FROM bots WHERE id = {uid}")
            rows = c.fetchall()
            if rows == []:
                c.execute(f"INSERT INTO bots VALUES({uid}, '{name}', '{ctx.author.name}')")
                await channel.send(f"{ctx.author.name} has authorised the bot `{name}` to be allowed into the server.")
            else:
                await channel.send("This bot has already been authorised to enter the server.")
        else:
            await ctx.send("You do not have the permission to use this command.")
        conn.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        if ctx.bot:
            channel = get(ctx.guild.channels, name='mod-log')
            await channel.send(f"An admin has removed the bot `{ctx.name}` from the server. <@599507281226367006> <@267667599666446336>")
        channel = get(ctx.guild.channels, name="entry-exit")
        await channel.send(f"{ctx.name} has left.")


def setup(bot):
    bot.add_cog(Events(bot))
