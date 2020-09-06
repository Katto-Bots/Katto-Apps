import random
import requests
import youtube_dl
import discord
import json
import os
import dotenv

from discord.ext import commands
from dotenv import load_dotenv

client = discord.Client()
client = commands.Bot(command_prefix="app!")
client.remove_command("help")
load_dotenv()
TOKEN = os.getenv('TOKEN')
os.chdir(r"/Users/tomaslovrant/PycharmProjects/kattoapps")

with open('../../PycharmProjects/tomu/words.txt') as file:
    file = file.read().split()


@client.event  # zaciatok
async def on_ready():
    print("-------------")
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print(client.latency * 1000)
    print("-------------")

    guild_members = len(set(client.get_all_members()))
    await client.change_presence(activity=discord.Game(name='app!help'.format(guild_members)))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title=":x: **Command not found! Try `app!help`**", color=discord.Color.red())
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title=":x: **You don't have enough permissions to execute this command!**",
                              color=discord.Color.red())
        await ctx.send(embed=embed)

    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title=":x: **Bot don't have enough permission to execute this command!**",
                              color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    embed = discord.Embed(title=f'Loaded `{extension}`!', color=discord.Color.gold())
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    embed = discord.Embed(title=f'Unloaded `{extension}`!', color=discord.Color.gold())
    await ctx.send(embed=embed)


@client.command(
    name='reload', description="Reload all/one of the bots cogs!"
)
@commands.is_owner()
async def reload(ctx, cog=None):
    if not cog:
        # No cog, means we reload all cogs
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=discord.Color.blurple(),
                timestamp=ctx.message.created_at
            )
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        client.unload_extension(f"cogs.{ext[:-3]}")
                        client.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`", value='\uFEFF', inline=False)
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`", value=e, inline=False)
                    await asyncio.sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # reload the specific cog
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=discord.Color.gold(),
                timestamp=ctx.message.created_at
            )
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                # if the file does not exist
                embed.add_field(
                    name=f"Failed to reload: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    client.unload_extension(f"cogs.{ext[:-3]}")
                    client.load_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Reloaded: `{ext}`", value='\uFEFF', inline=False)
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`", value=desired_trace, inline=False)
            await ctx.send(embed=embed)


for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
async def editor(ctx, *, link, amount=1):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=f"**We successfully recieved your editor application `{ctx.author.name}`!**",
                          color=0xa890ee)
    await ctx.send(embed=embed)

    channel = client.get_channel(750125684566786168)
    yes = "<:9358_yes_tick:748426928347938897>"
    no = "<:9830_no:748426943766069308>"

    embed = discord.Embed(title="**Editor application**", color=0xa890ee)
    embed.add_field(name="Instagram link: ", value=link, inline=False)
    embed.add_field(name="Discord username: ", value=f"{ctx.message.author.name}", inline=False)

    msg = await channel.send(embed=embed)
    await msg.add_reaction(yes)
    await msg.add_reaction(no)


@editor.error
async def editor_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="<:9830_no:748426943766069308>**You have to input your instagram link!**", color=0xa890ee)
        await ctx.send(embed=embed)


@client.command()
async def artist(ctx, *, link, amount=1):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=f"**<:9358_yes_tick:748426928347938897> We successfully recieved your artist application `{ctx.author.name}`!**",
                          color=0xff35c7)
    await ctx.send(embed=embed)

    channel = client.get_channel(750125684566786168)
    yes = "<:9358_yes_tick:748426928347938897>"
    no = "<:9830_no:748426943766069308>"

    embed = discord.Embed(title="**Artist application**", color=0xff35c7)
    embed.add_field(name="Instagram link: ", value=link, inline=False)
    embed.add_field(name="Discord username: ", value=f"{ctx.message.author.name}", inline=False)

    msg = await channel.send(embed=embed)
    await msg.add_reaction(yes)
    await msg.add_reaction(no)


@artist.error
async def artist_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="<:9830_no:748426943766069308> **You have to input your instagram link!**", color=0xff35c7)
        await ctx.send(embed=embed)


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def accept(ctx, member: discord.Member):
    embed = discord.Embed(title=f"<:9358_yes_tick:748426928347938897> **Successfully accepted {member}**", color=discord.Color.green())
    await ctx.send(embed=embed)

    channel = client.get_channel(717004879947890738)

    embed = discord.Embed(title=f"<:finished_emote_8_1:748969209001803938> **Congratulations {member} for getting accepted!!**", color=0xc70000)
    await channel.send(embed=embed)


@accept.error
async def accept_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="**You have to mention someone first!**", color=discord.Color.blurple())
        await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="**Help**", color=0xc70000)
    embed.add_field(name="**Editor**", value="`app!editor <instagram link>`", inline=False)
    embed.add_field(name="**Artist**", value="`app!artist <instagran link>`", inline=False)

    await ctx.send(embed=embed)


client.run(TOKEN)
