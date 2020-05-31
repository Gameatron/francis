import asyncio
from colorsys import hls_to_rgb

import discord
from discord.ext import commands

class Rainbow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.step = 7
        self.delay = 0.1
        self.hue = 0
        self.cock = "yes"

    @commands.command()
    async def start(self, ctx: commands.Context, role: discord.Role):
        self.cock = "yes"
        await ctx.message.delete()
        await ctx.send("rainbow time")
        if ctx.author.id == 653983428785733652:
            while self.cock == "yes":
                print(role.name, role.colour)
                self.hue = (self.hue + self.step) % 360
                rgb = [int(x * 255) for x in hls_to_rgb(self.hue / 360, 0.5, 1)]
                clr = discord.Colour(((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
                await role.edit(color=clr, reason='Automatic rainbow color change')
                await asyncio.sleep(self.delay)
    
    @commands.command()
    async def end(self, ctx):
        await ctx.message.delete()
        await ctx.send('ok', delete_after=5)
        self.cock = 'no'

     
def setup(bot):
    bot.add_cog(Rainbow(bot))