import discord
from discord.ext import commands
from discord.utils import get as discget
import os
import psycopg2
import json

with open("token.json", 'r') as f:
    DATABASE_URL = json.load(f)['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()


class Prison(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.free_roles = ('Einwanderer', 'Watchlist')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def imprison(self, ctx, user: discord.Member):
        await ctx.message.delete()
        c.execute(f"UPDATE users SET prison = 'True' WHERE user_id = {user.id};")
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass
        role = discget(ctx.guild.roles, name="Gefangener")
        await user.add_roles(role)
        await ctx.send(f"{user.name} has been imprisoned.", delete_after=5)
        channel = discget(ctx.guild.channels, name='prison-block')
        await channel.send(f"Welcome to prison, {user.mention}. Please see your way over to <#594420084529954848> when you are ready to leave.")
        conn.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def free(self, ctx, user: discord.Member):
        await ctx.message.delete()
        c.execute(f"UPDATE users SET prison = 'False' WHERE user_id = {user.id};")
        role = discget(ctx.guild.roles, name="Gefangener")
        await user.remove_roles(role)
        for role in self.free_roles:
            role = discget(ctx.guild.roles, name=role)
            await user.add_roles(role)
        await ctx.send(f"You have been freed, {user.mention}.", delete_after=5)
        for channel in ctx.guild.channels:
            if channel.name == "immigration-desk":
                await channel.send(f"You have been freed, and placed on the watchlist, {user.mention}.", delete_after=10)
                break
        conn.commit()


def setup(bot):
    bot.add_cog(Prison(bot))
