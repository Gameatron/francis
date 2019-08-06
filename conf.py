import discord
from discord.utils import get

class Conf:
    def __init__(self, conf):
        self.conf = conf
        self.id = conf[0]
        self.joinmessage = conf[1]
        self.joinmessagechannel = conf[2]
        self.joinrole = conf[3]
        self.botrole = conf[4]
        self.leavemessage = conf[5]
        self.leavemessagechannel = conf[6]
        self.prisonrole = conf[7]
        self.prisonchannel = conf[8]
        self.muterole = conf[9]
        self.modlog = conf[10]
        self.acceptedrole = conf[11]
        self.mainchat = conf[12]
        self.acceptmessage = conf[13]
        self.firstchannel = conf[14]
    
    def embed(self, ctx, bot):
        em = discord.Embed(color=0xFF0000)
        em.add_field(name="Server Name:", value=get(bot.guilds, id=self.id).name, inline=False)
        em.add_field(name="Join Message:", value=self.joinmessage, inline=False)
        em.add_field(name="Join Message Channel:", value=get(ctx.guild.channels, id=self.joinmessagechannel).mention, inline=False)
        em.add_field(name="Join Role:", value=get(ctx.guild.roles, id=self.joinrole).mention, inline=False)
        em.add_field(name="Bot Role:", value=get(ctx.guild.roles, id=self.botrole).mention, inline=False)
        em.add_field(name="Leave Message:", value=self.leavemessage, inline=False)
        em.add_field(name="Leave Message Channel:", value=get(ctx.guild.channels, id=self.leavemessagechannel).mention, inline=False)
        em.add_field(name="Prisoner Role:", value=get(ctx.guild.roles, id=self.prisonrole).mention, inline=False)
        em.add_field(name="Prison Channel:", value=get(ctx.guild.channels, id=self.prisonchannel).mention, inline=False)
        em.add_field(name="Mute Role:", value=get(ctx.guild.roles, id=self.muterole).mention, inline=False)
        em.add_field(name="Mod Log:", value=get(ctx.guild.channels, id=self.modlog).mention, inline=False)
        em.add_field(name="Citizen Role:", value=get(ctx.guild.roles, id=self.acceptedrole).mention, inline=False)
        em.add_field(name="Main Chat:", value=get(ctx.guild.channels, id=self.mainchat).mention, inline=False)
        em.add_field(name="Accepted Message:", value=self.acceptmessage, inline=False)
        em.add_field(name="Immigrant Channel:", value=get(ctx.guild.channels, id=self.firstchannel).mention, inline=False)
        return em

    def __str__(self):
        return self.conf