from typing import Union

import discord
from discord import Intents
from discord.ext import commands
from mikbot.f1 import f1_commands

intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='mikbot ', intents=intents)


@bot.event
async def on_ready() -> None:
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def ping(ctx: commands.Context) -> None:
    await ctx.send('pong')


@bot.command(name='laptimes')
async def lap_times(
        ctx: commands.Context,
        year: int,
        gp: Union[int, str],
        *drivers: str
) -> None:
    plot = f1_commands.lap_times(year, gp, drivers)
    await ctx.reply(file=discord.File(plot, f'{year}-{gp}-{drivers}.png'))
