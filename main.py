# IMPORTS #
import discord
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
token = os.environ.get('MUSS')
inv = os.environ.get('INVITE')
bot = commands.Bot(command_prefix=">",
                   description="franz bot")
# List of cogs
cogs = ('immigration', 'prison', 'utils', 'events',
        'error', 'fun', 'translator', 'economy', 'config',
        'nuke', 'rainbow')

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
    await bot.change_presence(activity=discord.Game(name="| >help | Made by Koda#8495"))
    print('------')


@bot.command(hidden=True)
async def invite(ctx):
    if ctx.author.id == 599507281226367006:
        await ctx.message.delete()
        await ctx.author.send(inv)
    else:
        await ctx.send("You must be Koda to use this command.")

# immediately stop the bot
@bot.command(hidden=True, aliases=['restart'])
async def stop(ctx):
    await bot.logout()

# Starts the bot
bot.run(token, reconnect=True)
