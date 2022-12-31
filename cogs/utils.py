import discord
from discord.ext import commands
from discord.utils import get as discget
import psycopg2
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaders = (653983428785733652, 703244120881234011)

    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=('purge', 'clean', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount: int):
        await ctx.message.delete()
        await self.clear(ctx, amount)
        await ctx.send(f"Cleared {amount} messages!", delete_after=5)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx, message, *, role: discord.Role):
        await ctx.message.delete()
        try:
            await role.edit(reason='Temp ping.', mentionable=True)
            await ctx.send(f"{role.mention}\n{message}")
            await role.edit(reason="Temp ping.", mentionable=False)
        except discord.ext.commands.errors.BadArgument:
            await ctx.send(f"That is not a valid role name. (Capitilization matters!)", delete_after=5)

    @commands.command()
    async def servers(self, ctx):
        em = discord.Embed(
            color=0xFF0000, title="List of all Serves:")
        for item in self.bot.guilds:
            em.add_field(
                name=item.name, value=f"{len(list(item.members))} members", inline=False)
        em.add_field(name="Total number of members currently seen:",
                     value=len(list(self.bot.get_all_members())))
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bots(self, ctx):
        em = discord.Embed(color=0xFF0000, title="All authorised bots:")
        c.execute("SELECT * FROM bots")
        rows = c.fetchall()
        if rows == []:
            await ctx.send("No bots have been authorised.")
            return
        for row in rows:
            em.add_field(
                name=row[1], value=f"Bot ID: {row[0]}\nAuthorised by: {row[2]}", inline=False)
        await ctx.send(embed=em)

    @commands.command()
    async def ab(self, ctx, *, role: discord.Role):
        for user in ctx.guild.members:
             try:
                 await user.add_roles(role)
             except:
                 pass              
                

async def setup(bot):
    await bot.add_cog(Utils(bot))
