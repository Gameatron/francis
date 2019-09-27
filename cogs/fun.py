import discord
from discord.ext import commands
from random import randint, choice
import asyncio
from time import sleep


insults = ("You're even more incompetent than me!",
           "You lost that harder than I did in Africa!",
           "You're so stupid even Albania wouldn't want to work with you.",
           "I'd change sides just so I dont have to put up you.",
           "I'm beginning to look like an acceptable ally compared to you.",
           "You're as rusty as my navy!",
           "Your brain has less function than my tanks!",
           "You are even less prepared than my soldiers!",
           "Your brain cells remind me of the planes in my air force. Low in number and missing components.",
           "Your chromosomes remind me of my men's equipment: Something's always missing.",
           "You're as fragile as my defenses!",
           "You are even more undefended than how we left Rome!")


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def greece(self, ctx):
        await asyncio.sleep(1)
        await ctx.send("Can I invade Greece?")
        msg = await self.bot.wait_for("message", timeout=30)
        msg = msg.content.lower()
        if msg == 'yes':
            await ctx.send("YES! Will do! Heil Hitler!")
        else:
            await ctx.send("Fuck you, I'm invading Greece!")
        await asyncio.sleep(10)
        await ctx.send("I lost...")

    @commands.command()
    async def insult(self, ctx, user: discord.Member = None):
        try:
            if user == None:
                user = ctx.message.author
            else:
                pass
            await ctx.message.delete()
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name="Insult",
                            value=f"{choice(insults)} {user.mention}")
            await ctx.send(embed=embed)
        except discord.ext.commands.errors.BadArgument:
            await ctx.send("That is not a proper user mention.")


def setup(bot):
    bot.add_cog(Fun(bot))
