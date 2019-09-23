import discord
from discord.ext import commands
import urbandict as ud


class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def define(self, ctx, *, word):
        try:
            defs = ud.define(word)
            em = discord.Embed(title=f"Definition of {word}:", description=defs[0]['def'])
            await ctx.send(embed=em)
        except:
            await ctx.send(f"Word ({word}) not found.")


def setup(bot):
    bot.add_cog(Define(bot))
