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
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        rows = c.fetchall()
        colnames = [desc[0] for desc in c.description]
        em = discord.Embed(color=0xFF0000)
        for i in range(1000):
            if i == 0:
                em.add_field(name=colnames[i], value=ctx.guild.name, inline=False)
            else:
                try:
                    if type(rows[0][i]) == int:
                        item = get(ctx.guild.channels, id=rows[0][i])
                        if item == None:
                            item = get(ctx.guild.roles, id=rows[0][i])
                            if item == None:
                                em.add_field(name=colnames[i], value="None")
                            else:
                                em.add_field(name=colnames[i], value=item.name, inline=False)
                        else:
                            em.add_field(name=colnames[i], value=item.name, inline=False)
                    else:
                        em.add_field(name=colnames[i], value=rows[0][i], inline=False)
                except IndexError:
                    break
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Config(bot))