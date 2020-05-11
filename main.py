# IMPORTS #
import discord
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
token, inv = os.environ.get('TOKEN'), os.environ.get('INVITE')
bot = commands.Bot(command_prefix=">",
                   description="muss bot")
admins = (653983428785733652, 703244120881234011)
# List of cogs
cogs = ['config', 'define', 'economy', 'error',
        'events', 'fun', 'help', 'immigration',
        'nuke', 'prison', 'rainbow', 'ranks',
        'translator', 'utils']

bot.remove_command('help')


@bot.command()
async def load(ctx, cog):
    if ctx.author.id in admins:
        try:
            bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Loaded '{cog}' successfully!")
        except Exception as er:
            await ctx.send(f"{cog} cannot be loaded. [{er}]")
    else:
        raise commands.CommandNotFound('error')


@bot.command()
async def unload(ctx, cog):
    if ctx.author.id in admins:
        try:
            bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Unloaded '{cog}' successfully!")
        except Exception as er:
            await ctx.send(f"{cog} cannot be unloaded. [{er}]")
    else:
        raise commands.CommandNotFound("error")


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
    await bot.change_presence(activity=discord.Game(name="| >help | Nukes Loaded..."))
    print('------')


@bot.command()
async def invite(ctx):
    if ctx.author.id in admins:
        await ctx.message.delete()
        await ctx.author.send(inv)
    else:
        await ctx.send("You do not have permission to use this command.")

# immediately stop the bot
@bot.command(aliases=['restart'])
async def stop(ctx):
    await bot.logout()

# Starts the bot
while True:
    bot.run(token, reconnect=True)
