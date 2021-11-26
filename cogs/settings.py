import discord
from discord.ext import commands
from discord.utils import get as discget
import os
import psycopg2
import json
import dotenv
dotenv.load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def find(self, ctx, query):
        c.execute(f"SELECT * FROM ser_info WHERE id={ctx.server.id}")
        row = c.fetchall()
        print(row)

def setup(bot):
    bot.add_cog(Settings(bot))
