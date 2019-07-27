import discord
from discord.ext import commands
from discord.utils import get as discget
import os
import psycopg2
import json
import dotenv
dotenv.load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()


class Prison(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.free_roles = ('Immigrant', 'Watchlist')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def imprison(self, ctx, user: discord.Member):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        await ctx.message.delete()
        c.execute(
            f"UPDATE users SET prison = 'True' WHERE user_id = {user.id};")
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass
        role = discget(ctx.guild.roles, name=conf[0][7])
        await user.add_roles(role)
        await ctx.send(f"{user.name} has been imprisoned.", delete_after=5)
        channel = discget(ctx.guild.channels, name=conf[0][8])
        await channel.send(f"Welcome to prison, {user.mention}. Please see your way over to <#599545935172993035> when you are ready to leave.")
        conn.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def free(self, ctx, user: discord.Member):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        await ctx.message.delete()
        c.execute(
            f"UPDATE users SET prison = 'False' WHERE user_id = {user.id};")
        role = discget(ctx.guild.roles, name=conf[0][7])
        await user.remove_roles(role)
        role = discget(ctx.guild.roles, name=conf[0][3])
        await user.add_roles(role)
        await ctx.send(f"You have been freed, {user.mention}.", delete_after=5)
        channel = discget(ctx.guild.channels, name=conf[0][14])
        await channel.send(f"You have been freed, {user.mention}.", delete_after=10)
        conn.commit()

    @commands.command(pass_context=True)
    async def prisoners(self, ctx):
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        em = discord.Embed(color=0xFF0000, title='List of all prisoners:')
        for row in rows:
            if row[1] == 'True ':
                user = discget(self.bot.get_all_members(), id=row[0])
                if user == None:
                    em.add_field(name=row[0], value='Unknown Name')
                else:
                    em.add_field(name=user.name, value=user.mention)
            else:
                pass
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Prison(bot))
