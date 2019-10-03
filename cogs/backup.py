import discord
from discord.ext import commands
import json

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def b_create(self, ctx):
        with open("backups.json", 'r') as f:
            data = json.load(f)
        


def setup(bot):
    bot.add_cog(Backup(bot))