import discord
from discord.ext import commands
from discord.utils import get
import os
import psycopg2

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def config(self, ctx):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall
        pass

def setup(bot):
    bot.add_cog(Config(bot))