import discord
from discord.ext import commands
from discord.utils import get as discget


class Prison(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.free_roles = ('Einwanderer', 'Watchlist')

    @commands.command()
    async def imprison(self, ctx, user: discord.Member):
        await ctx.message.delete()
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass
        role = discget(ctx.guild.roles, name="Gefangener")
        await user.add_roles(role)
        await ctx.send(f"{user.name} has been imprisoned.")
        channel = discget(ctx.guild.channels, name='prison-block')
        await channel.send(f"Welcome to prison, {user.mention}. Please see your way over to <#594420084529954848> when you are ready to leave.")

    @commands.command()
    async def free(self, ctx, user: discord.Member):
        await ctx.message.delete()
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


def setup(bot):
    bot.add_cog(Prison(bot))
