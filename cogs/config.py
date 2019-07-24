import discord
from discord.ext import commands
from discord.utils import get
import os
import psycopg2

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def config(self, ctx, field=None, *, v=None):
        print(v)
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        rows = c.fetchall()
        if rows == []:
            c.execute(f"INSERT INTO conf VALUES({ctx.guild.id}, 'None', 'None')")
            c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
            rows = c.fetchall()
            print(rows)
        if field == None:
            em = discord.Embed(color=0xFF0000)
            em.add_field(name="welcomechannel:", value=rows[0][1])
            em.add_field(name='prisonerrole:', value=rows[0][2])
            return await ctx.send(embed=em)
        elif field == 'welcomechannel':
            if isinstance(v, discord.TextChannel):
                c.execute(f"UPDATE conf SET welc = '{v.name}' WHERE id = {ctx.guild.id}")
                return await ctx.send(f"I have changed the welcome channel to `{v}`.")
            else:
                channel = get(ctx.guild.channels, name=v)
                if isinstance(channel, discord.TextChannel):
                        c.execute(f"UPDATE conf SET welc = '{v}' WHERE id = {ctx.guild.id}")
                        return await ctx.send(f"I have changed the welcome channel to `{v}`.")
                else:
                    return await ctx.send("That is not a proper channel.")
            await ctx.send(f"The current welcome channel is `{rows[0][1]}`.")
        elif field == 'prisonerrole':
            if not v == None:
                c.execute(f"UPDATE conf SET pris = '{v}' WHERE id = {ctx.guild.id}")
                await ctx.send(f"I have changed the prisoner role to `{v}`.")
            else:
                return await ctx.send(f"The current prisoner role is `{rows[0][2]}`.")
        conn.commit()


def setup(bot):
    bot.add_cog(Config(bot))