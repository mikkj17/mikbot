import discord
import os
import random
import time
import utils
from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv
from typing import Optional

import livescore

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
async def troels(ctx: Context):
    chosen = random.choice(quotes)
    await ctx.send(f'{chosen["quote"]}\n*{chosen["context"]}*')


@bot.command()
async def silke(ctx: Context, channel: Optional[discord.channel.VoiceChannel], member: str = None):
    if member:
        await ctx.send(f'Den her går ud til dig, {member.title()}', tts=True)
        time.sleep(3)
    await utils.play_mp3(ctx, 'silke', channel)


@bot.command()
async def hestene(ctx: Context, channel: Optional[discord.channel.VoiceChannel]):
    await utils.play_mp3(ctx, 'hestene', channel)


@bot.command()
async def ja(ctx: Context, channel: Optional[discord.channel.VoiceChannel]):
    await utils.play_mp3(ctx, 'ja', channel)


@bot.command()
async def motivation(ctx: Context, channel: Optional[discord.channel.VoiceChannel]):
    await utils.play_mp3(ctx, 'motivation', channel)


#TODO: make equivalent unsubscribe function, or better, merge both into one function calling right functions with getattr etc.
@bot.command()
async def subscribe(ctx: Context, team_name: str):
    possible_teams = livescore.search_for_team(team_name)

    if possible_teams.count() == 0:
        message = 'Team not found!'

    elif possible_teams.count() > 1:
        formatted_teams = '\n'.join(team['name'] for team in possible_teams)
        message = f'Multiple teams found. Please specify one of the following:\n{formatted_teams}'

    else:
        team = possible_teams[0]
        update = livescore.subscribe(ctx.author.id, team)
        if update.upserted_id is None and update.modified_count == 0:
            message = f"You're already subscribed to {team['name']} :soccer:"
        else:
            message = f"You're now subscribed to {team['name']} :soccer:"

    await ctx.send(message)


bot.run(TOKEN)
