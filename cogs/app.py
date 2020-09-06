import discord
from discord.ext import commands

client = discord.Client()


class Apps(commands.Cog):

    def __init__(self, client):
        self.client = client

    # loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("App.py loaded")

    # command


def setup(client):
    client.add_cog(Apps(client))
