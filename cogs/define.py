import discord
from discord.ext import commands
import urbandictionary as ud

class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def define(self, ctx, word):
        defs = ud.define("word")
        em = discord.Embed(title=f"All definitions of {word}:")
        a = 1
        for i in defs:
            em.add_field(name=f'Definition {a}:', value=i)
            a += 1
        await ctx.send(embed=em)
    
def setup(bot):
    bot.add_cog(Define(bot))