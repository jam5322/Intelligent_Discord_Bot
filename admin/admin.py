import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot admin commands are online.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear1any(self, ctx, amount=2):
        await ctx.channel.purge(limit = amount)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear5any(self, ctx, amount=6):
        await ctx.channel.purge(limit = amount)

def setup(client):
    client.add_cog(Admin(client))