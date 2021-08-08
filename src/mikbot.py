import discord
import random
import time
from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context
from typing import Optional

from . import livescore
from . import utils

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

quotes = utils.load_troels()

@bot.event
async def on_ready() -> None:
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def troels(ctx: Context) -> None:
    chosen = random.choice(quotes)
    await ctx.send(f'{chosen["quote"]}\n*{chosen["context"]}*')


@bot.command()
async def silke(ctx: Context, channel: Optional[discord.channel.VoiceChannel], member: str = None) -> None:
    if member:
        await ctx.send(f'Den her går ud til dig, {member.title()}', tts=True)
        time.sleep(3)
    await utils.play_mp3(ctx, 'silke', channel)


@bot.command()
async def hestene(ctx: Context, channel: Optional[discord.channel.VoiceChannel]) -> None:
    await utils.play_mp3(ctx, 'hestene', channel)


@bot.command()
async def ja(ctx: Context, channel: Optional[discord.channel.VoiceChannel]) -> None:
    await utils.play_mp3(ctx, 'ja', channel)


@bot.command()
async def motivation(ctx: Context, channel: Optional[discord.channel.VoiceChannel]) -> None:
    await utils.play_mp3(ctx, 'motivation', channel)


@bot.command()
async def subscribe(ctx: Context, team_name: str) -> None:
    message = livescore.sub_unsub(ctx.author.id, team_name, True)
    await ctx.send(message)


@bot.command()
async def unsubscribe(ctx: Context, team_name: str) -> None:
    message = livescore.sub_unsub(ctx.author.id, team_name, False)
    await ctx.send(message)
