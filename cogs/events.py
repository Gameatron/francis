import discord
from discord.ext import commands
from discord.utils import get
import os
import psycopg2
import asyncio
import json
import dotenv

dotenv.load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
c = conn.cursor()



class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                    # Koda               # Lime              # Brakke
        self.gods = (653983428785733652, 703244120881234011, 267667599666446336)
        self.reactions = ('👍', '👎')

    async def remove_all_roles(self, user):
        for role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass
    
    async def get_chan(self, ctx, uid):
        chan = get(ctx.guild.channels, id=uid)
        return chan

    async def update_chan(self, ctx):
            o, i = self.memcount(ctx)
            ver, uver, total = get(ctx.guild.channels, id=717121186068430948), get(ctx.guild.channels, id=717121228351078611), get(ctx.guild.channels, id=717124441632538734)
            await ver.edit(name=f"Verified Members: {i}")
            await uver.edit(name=f"Unverified Members: {o}")
            await total.edit(name=f"Total Members: {o+i}")

    def memcount(self, ctx):
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        i, o = 0, 0
        for mem in ctx.guild.members:
            ver = get(ctx.guild.roles, id=conf[0][12])
            if ver in mem.roles:
                i += 1
            else:
                o += 1
        return (o, i)

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        try:
            c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
            conf = c.fetchall()
            if ctx.bot:
                channel = get(ctx.guild.channels, id=conf[0][14])
                c.execute(f"SELECT * FROM bots WHERE id = {ctx.id}")
                rows = c.fetchall()
                if rows == []:
                    await channel.send(f"An admin has attempted to add the bot `{ctx.name}`, and it is unauthorised. To authorize it, type `>authorize {ctx.id} {ctx.name}` {ctx.guild.owner.mention} <@{self.gods[0]}>")
                    await ctx.guild.kick(ctx, reason="Unauthorised Bot")
                else:
                    await channel.send(f"An admin has attempted to add the bot `{ctx.name}` to the server succesfully. {ctx.guild.owner.mention} <@{self.gods[0]}>")
                    role = get(ctx.guild.roles, id=conf[0][6])
                    await ctx.add_roles(role)
            else:
                c.execute(f"SELECT * FROM users WHERE id = {ctx.id};")
                rows = c.fetchall()
                if rows == []:
                    c.execute(f"INSERT INTO users VALUES({ctx.id}, 'False');")
                c.execute(f"SELECT prison FROM users WHERE id = {ctx.id};")
                rows = c.fetchall()
                if 'True' in rows[0]:
                    await asyncio.sleep(1)
                    await self.remove_all_roles(ctx)
                    role = get(ctx.guild.roles, id=conf[0][8])
                    await ctx.add_roles(role)
                else:
                    channel = get(ctx.guild.channels, id=conf[0][2])
                    await channel.send(f'{conf[0][1]}'.format(ctx.mention))
                    try:
                        role = get(ctx.guild.roles, id=conf[0][3])
                        await ctx.add_roles(role)
                    except AttributeError:
                        pass
                conn.commit()
            await self.update_chan(ctx)
        except IndexError:
            pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def authorize(self, ctx, uid, *, name):
        await ctx.message.delete()
        c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
        conf = c.fetchall()
        if ctx.author.id in self.gods:
            channel = get(ctx.guild.channels, id=conf[0][14])
            c.execute(f"SELECT * FROM bots WHERE id = {uid}")
            rows = c.fetchall()
            if rows == []:
                c.execute(f"INSERT INTO bots VALUES({uid}, '{name}', '{ctx.author.name}')")
                await channel.send(f"{ctx.author.name} has authorised the bot `{name}` to be allowed into the server.")
            else:
                await channel.send("This bot has already been authorised to enter the server.")
        else:
            await ctx.send("You do not have the permission to use this command.")
        conn.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        try:
            c.execute(f"SELECT * FROM conf WHERE id = {ctx.guild.id}")
            conf = c.fetchall()
            if ctx.bot:
                channel = get(ctx.guild.channels, id=conf[0][14])
                await channel.send(f"An admin has removed the bot `{ctx.name}` from the server.")
            else:
                channel = get(ctx.guild.channels, id=conf[0][5])
                await channel.send(f"{conf[0][4]}".format(ctx.name))
            await self.update_chan(ctx)  
        except IndexError:
            pass


async def setup(bot):
    await bot.add_cog(Events(bot))
