import asyncio
import discord
import json
import config
from discord.ext import commands


class CrossLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("'CrossLink' Cog has been loaded!")

    @commands.command(name="add-link")
    async def add_link(self, ctx):
        try:
            message = await ctx.send(f"Adding {ctx.channel.mention} to the link network...")
            config.CROSSLINK_IDS.add_id(ctx.channel_id)
            await message.edit(f"Added {ctx.channel.mention} to `crosslink-ids.json` (CrossLink enabled for this channel)")
        except config.IDAlreadyPresentError:
            await message.edit("Channel is already in the cross-link network")
                
    @commands.command(name="remove-link")
    async def remove_link(self, ctx):
        try:
            message = await ctx.send(f"Removing {ctx.channel.mention} from the link network...")
            config.CROSSLINK_IDS.remove_id(ctx.channel.id)
            await message.edit(f"Removed {ctx.channel.mention} from `crosslink-ids.json` (CrossLink disabled for this channel)")
        except config.IDNotPresentError:
            await message.send("Channel isn't in the cross-link network.")

    @commands.Cog.listener()
    async def on_message(self, message):
        crosslink_user = "{}#{}".format(message.author.name, message.author.discriminator)
        if (not message.author.bot and message.content.lower() != ".remove-link" and message.content.lower() != "/remove-link"):
            crosslink_message = "**{}**-{}: {}".format(message.guild.name, crosslink_user, message.content.replace("@", "(a)"))
            if config.CROSSLINK_IDS.contains(message.channel.id):
                await self.bot.get_channel(int(637949482784260124)).send()
                for channel in config.CROSSLINK_IDS.get_all_but(message.channel.id):
                    await self.bot.get_channel(int(channel)).send(crosslink_message)

        if (message.channel.id == 637949482784260124 and message.author.id != self.bot.user.id):
            for channel in config.CROSSLINK_IDS.get_all_but(637949482784260124):
                await self.bot.get_channel(int(channel)).send(message.content.replace("@", "(a)"))


def setup(bot):
    bot.add_cog(CrossLink(bot))

