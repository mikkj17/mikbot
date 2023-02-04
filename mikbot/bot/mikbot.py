from discord import Intents
from discord.ext import commands

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
