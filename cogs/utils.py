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
        self.leaders = [599507281226367006, 585722582565781521, 606614408709537806,
                        412017598763630594, 525589663310807040, 596413516680790017,
                        580594776013930497, 294567582969757696]

    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    async def mod_message(self, ctx, author, type, amount, user=None, reason="No reason specified."):
        em = discord.Embed(title=f"{type} report:", color=0xFF0000)
        if not user == None:
            em.add_field(name="User:", value=user.name)
        em.add_field(name="Action:", value=type)
        em.add_field(name="Moderator:", value=author.name)
        if not reason == None:
            em.add_field(name="Reason:", value=reason)
        if type == 'Deletion':
            em.add_field(name='Messages Cleared:', value=amount)
        channel = discget(ctx.guild.channels, name="mod-log")
        await channel.send(embed=em)

    @commands.command(aliases=('purge', 'clean', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount: int):
        await ctx.message.delete()
        await self.clear(ctx, amount)
        await ctx.send(f"Cleared {amount} messages!", delete_after=5)
        await self.mod_message(ctx, ctx.author, 'Deletion', amount, reason=None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx, *, role: discord.Role):
        await ctx.message.delete()
        try:
            await role.edit(reason='Temp ping.', mentionable=True)
            await ctx.send(role.mention)
            await role.edit(reason="Temp ping.", mentionable=False)
        except discord.ext.commands.errors.BadArgument:
            await ctx.send(f"That is not a valid role name. (Capitilization matters!)", delete_after=5)

    @commands.command()
    async def coalition(self, ctx):
        em = discord.Embed(
            color=0xFF0000, title="List of all Coalition Serves:")
        for item in self.bot.guilds:
            em.add_field(
                name=item.name, value=f"{len(list(item.members))} members", inline=False)
        em.add_field(name="Total number of Coalition members currently:",
                     value=len(list(self.bot.get_all_members())))
        await ctx.send(embed=em)

    @commands.command()
    async def add_server(self, ctx, id: int, invite, *, name):
        c.execute(f"INSERT INTO coalition VALUES({id}, {name}, {invite})")
        conn.commit()

    @commands.command()
    async def update_coalition(self, ctx):
        await ctx.message.delete()
        if ctx.author.id in self.leaders:
            c.execute(f"SELECT * FROM coalition")
            coalition = c.fetchall()
            em = discord.Embed(color=0xFF0000)
            for guild in coalition:
                em.add_field(
                    name=guild[1], value=f"Server ID: {guild[0]}\nServer Invite: {guild[2]}", inline=False)
            em.set_footer(
                text=f"There are currently {len(list(self.bot.get_all_members()))} members in the Coalition, out of {len(list(self.bot.guilds))} states.")
            em.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/608452530384404483/608548001048428544/The_Coalition_logo.jpg')
            for guild in self.bot.guilds:
                channel = discget(guild.channels, name='coalition')
                if not channel == None:
                    await channel.purge(limit=100)
                    await channel.send(embed=em)
        else:
            await ctx.send("You lack the permissions to use this command.")

    @commands.command()
    async def directories(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(
            color=0xFF0000, title="All Current Leader of the Coalition:")
        for user in self.leaders:
            user = self.bot.get_user(user)
            em.add_field(name=user.name,
                         value=f"User: {user.mention}\nUser ID: {user.id}")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Utils(bot))
