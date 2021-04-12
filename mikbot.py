import discord
import os
import random
import time
import utils

from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

quotes = utils.load_troels()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def troels(ctx):
    chosen = random.choice(quotes)
    await ctx.send(f'{chosen["quote"]}\n*{chosen["context"]}*')


@bot.command()
async def silke(ctx, member: str = None):
    if member:
        await ctx.send(f'Den her går ud til dig, {member.title()}', tts=True)
        time.sleep(3)
    await utils.play_mp3(ctx, 'silke')


@bot.command()
async def hestene(ctx):
    await utils.play_mp3(ctx, 'hestene')


@bot.command()
async def ja(ctx):
    await utils.play_mp3(ctx, 'ja')


@bot.command()
async def motivation(ctx):
    await utils.play_mp3(ctx, 'motivation')

bot.run(TOKEN)

