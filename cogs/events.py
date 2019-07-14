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
        self.roles = {
            'prisoner': "Prisoner",
            'immigrant': "Immigrant",
            'citizen': "Citizen"
        }
    
    async def remove_all_roles(self, user):
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass
    
    @commands.Cog.listener()
    async def on_member_join(self, ctx):
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
    
    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        channel = get(ctx.guild.channels, name="entry-exit")
        await channel.send(f"{ctx.name} has left.")


def setup(bot):
    bot.add_cog(Events(bot))
