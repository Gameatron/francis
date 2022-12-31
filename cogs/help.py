import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="All Current Commands", color=0xff0000)
        embed.add_field(
            name="config", 
            value="Shows you the config of the server currently.", inline=False)
        embed.add_field(
            name="greece", 
            value="Prompts Mussolini to invade Greece.", inline=False)
        embed.add_field(
            name="insult", 
            value="Mussolini insults you.", inline=False)
        embed.add_field(
            name="translate [target language] [text]",
            value="Translate [text] into [target language].", inline=False)
        embed.add_field(
            name="imprison [user mention]", 
            value="Imprisons target user.", inline=False)
        embed.add_field(
            name="free [user mention]",
            value="Frees target user.", inline=False)
        embed.add_field(
            name="prisoners", 
            value="Shows all current prisoners. Anyone that is in this list will be imprisoned upon joining a server with Mussolini in it.", inline=False)
        embed.add_field(
            name="accept [user mention]", 
            value="Removes the immigrant role, and gives the citizen role to target user, as well as deleting one message.")
        embed.add_field(
            name="bots", 
            value="Shows all authorized bots. Any bot that is not in this list will be removed upon joining a server Mussolini is in.", inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))