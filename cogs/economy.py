import discord
from discord.ext import commands
from discord.utils import get as discget
import random
import time
import os
import psycopg2

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def balance(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        c.execute(f"SELECT * FROM eco WHERE id = {user.id}")
        rows = c.fetchall()
        if rows == []:
            c.execute(f"INSERT INTO eco VALUES({user.id}, 100, 0)")
            c.execute(f"SELECT * FROM eco WHERE id = {user.id}")
            rows = c.fetchall()
        emoji = discget(ctx.guild.emojis, name='guilder')
        em = discord.Embed(color=0xFF0000)
        em.add_field(name=f"{user.name}'s balance:", value=f"{emoji}{str(rows[0][1])}")
        await ctx.send(embed=em)

    @commands.command(pass_context=True)
    async def work(self, ctx):
        c.execute(f"SELECT * FROM eco WHERE id = {ctx.author.id}")
        rows = c.fetchall()
        if rows == []:
            c.execute(f"INSERT INTO eco VALUES({ctx.author.id}, 100, 0)")
            c.execute(f"SELECT * FROM eco WHERE id = {ctx.author.id}")
            rows = c.fetchall()
        amount = random.randint(20, 100)
        emoji = discget(ctx.guild.emojis, name='guilder')
        if int(time.time() - float(rows[0][2])) > 30:
            await ctx.send(f'You worked for {emoji}{amount}, {ctx.author.mention}')
            c.execute(f"UPDATE eco SET lastworked = {time.time()}, amount = {rows[0][1] + amount} WHERE id = {ctx.author.id}")
        else:
            await ctx.send(f"You need to wait {int(30 - (time.time() - float(rows[0][2])))} more seconds to work, {ctx.author.mention}")
        conn.commit()

def setup(bot):
    bot.add_cog(Economy(bot))
        