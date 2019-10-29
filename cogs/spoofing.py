import discord
import json
import config
import logging
from discord.ext import commands

class Spoof(commands.Cog):
    def __init__(self, client):
        self.client = client
        logging.info("\'Spoof\' Cog has been loaded!")
        
    @commands.command()
    async def spoof(self, ctx, user : discord.Member):
        if config.OIDs.contains(ctx.author.id):
            if config.SPIDS.contains(user.id):
                await ctx.send(f'Removing <@{user.id}> from the spoofing list...')
                config.SPIDS.remove_id(user.id)
            else:
                await ctx.send(f'Adding <@{user.id}> to the spoofing list...')
                config.SPIDS.add_id(user.id)
        
    @commands.command()
    async def announce(self, ctx, *, message : str):
        if config.OIDs.contains(ctx.author.id):
            await ctx.send("Bish please, Master removed the command")

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content
        if config.SPIDS.contains(message.author.id) and message.author.id != self.client.user.id:
            user = message.author.name + '#' + message.author.discriminator
            await self.client.get_channel(638371313576312883).send("**{}** : {}".format(user, message.content))


def setup(client):
    client.add_cog(spoof(client))