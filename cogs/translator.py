import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES


class Gtranslator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trans = Translator()

    @commands.command()
    async def translate(self, ctx, dest='English', *, content):
        ctx.message.delete()
        try:
            translation = self.trans.translate(content, dest=dest.lower())
        except ValueError:
            await ctx.send("This is not a valid language!")
            return
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Language Destination:",
                        value=LANGUAGES[translation.dest].capitalize(), inline=False)
        embed.add_field(name="Language Detected:",
                        value=LANGUAGES[translation.src].capitalize(), inline=False)
        embed.add_field(name="Translation:",
                        value=translation.text, inline=False)
        embed.set_footer(text="Translation comes directly from google translate. Some of these translations may not be good. Don't bug Koda about it.")
        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gtranslator(bot))
