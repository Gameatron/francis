from conf import Conf
import discord
from discord.ext import commands
from discord.utils import get
import os
import psycopg2
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        await ctx.message.delete()
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = Conf(c.fetchall()[0])
        await ctx.send(embed=conf.embed(ctx, self.bot))


async def setup(bot):
    await bot.add_cog(Config(bot))
