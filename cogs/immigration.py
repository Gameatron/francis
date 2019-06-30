import discord
from discord.ext import commands
from discord.utils import get as discget


class Immigration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def accept(self, ctx, user: discord.Member):
        await ctx.message.delete()
        role = discget(ctx.guild.roles, name="Bewohner")
        await user.add_roles(role)
        role = discget(ctx.guild.roles, name="Einwanderer")
        await user.remove_roles(role)
        await self.clear(ctx, 1)
        await ctx.send(f"{user.mention} accepted.", delete_after=3)

    @commands.command()
    async def deny(self, ctx, user: discord.Member):
        await self.clear(ctx, 2)
        await ctx.send(f"{user.mention} denied.", delete_after=3)


def setup(bot):
    bot.add_cog(Immigration(bot))
