import discord
from discord.ext import commands
from discord.utils import get as discget
import os
import psycopg2

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()


class Immigration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def accept(self, ctx, user: discord.Member):
        await ctx.message.delete()
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        role = discget(ctx.guild.roles, id=conf[0][3])
        try:
            await user.remove_roles(role)
        except AttributeError:
            pass
        role = discget(ctx.guild.roles, id=conf[0][12])
        await user.add_roles(role)
        await self.clear(ctx, 1)
        channel = discget(ctx.guild.channels, id=conf[0][11])
        await channel.send(f"{conf[0][10]}".format(user.mention))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deny(self, ctx, user: discord.Member):
        await self.clear(ctx, 2)
        await ctx.send(f"{user.mention} denied.", delete_after=3)


async def setup(bot):
    await bot.add_cog(Immigration(bot))
