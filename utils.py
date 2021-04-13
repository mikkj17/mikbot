import discord
import json
import time

from string import Template
from typing import Dict
from typing import List

MP3_ERROR_MSG = Template(
"""Hey $name. Du er noob!
Gå ind i en voice channel eller skriv \
navnet på den kanal hvor jeg skal \
afspille **$filename** :wink:.""")

def log(func):
    def inner(*args, **kwargs):
        print(f'{func.__name__} command was issued')
        print(f'arguments: {args[1:]}')
        return func(*args, **kwargs)
    return inner

def load_troels() -> List[Dict[str, str]]:
    with open('resources/citater.json', encoding='utf-8') as f:
        return json.load(f)

async def connect_and_play(stream, channel):
    vc = await channel.connect()
    vc.play(stream)
    while vc.is_playing():
        time.sleep(.1)
    await vc.disconnect()

@log
async def play_mp3(ctx, filename, channel):
    stream = discord.FFmpegPCMAudio(source=f'resources/{filename}.mp3')
    voice = ctx.author.voice
    if channel:
        await connect_and_play(stream, channel)
    elif voice:
        await connect_and_play(stream, voice.channel)
    else:
        await ctx.reply(
            MP3_ERROR_MSG.substitute(name=ctx.author.name, filename=filename),
            mention_author=False
        )

if __name__ == '__main__':
    quotes = load_troels()
    quote = quotes[-2]
    print(quote['quote'])
