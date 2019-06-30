import discord
from discord.ext import commands
from discord.utils import get as discget

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def _clear(self, ctx, amount: int):
        await ctx.message.delete()
        await self.clear(ctx, amount)
        await ctx.send(f"Cleared {amount} messages!", delete_after=5)
        await self.mod_message(ctx, ctx.author, 'Deletion', amount, reason=None)

def setup(bot):
    bot.add_cog(Utils(bot))