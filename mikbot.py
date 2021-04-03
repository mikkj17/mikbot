import os
import discord
import random
import utils
import time

from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def troels(ctx):
    quote, context = random.choice(utils.parse_troels())
    await ctx.send(f'{quote}\n*{context}*')

@bot.command()
async def silke(ctx, name: str=None):
    if name is not None:
        await ctx.send(f'This one is for you, {name.title()}', tts=True)
        time.sleep(3)
    await utils.play_mp3(ctx, 'silke')

@bot.command()
async def hestene(ctx):
    await utils.play_mp3(ctx, 'hestene')

@bot.command()
async def ja(ctx):
    await utils.play_mp3(ctx, 'ja')



bot.run(TOKEN)
