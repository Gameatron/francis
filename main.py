# IMPORTS #
import discord
from discord.ext import commands
import json

# Grabs the token from token.json
with open("token.json", 'r') as f:
    token = json.load(f)['TOKEN']
bot = commands.Bot(command_prefix=">",
                   description="franz bot")
# List of cogs
cogs = ('immigration', 'prison', 'utils', 'events')

# Loads the list of cogs
if __name__ == "__main__":
    for cog in cogs:
        try:
            bot.load_extension(f"cogs.{cog}")
            print(f"Loaded '{cog}' successfully!")
        except Exception as er:
            print(f"{cog} cannot be loaded. [{er}]")


# Runs this before the bot starts
@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game(name="War Preparations"))
    print('------')

# immediately stop the bot
@bot.command(hidden=True, aliases=['restart'])
async def stop(ctx):
    await bot.logout()

# Starts the bot
bot.run(token, reconnect=True)