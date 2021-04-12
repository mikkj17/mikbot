import discord
import functools
import json
import time

from typing import Dict
from typing import List

FFMPEG_OPTIONS = {
    'options': '-vn'
}

def log(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(f'{func.__name__} command was issued')
        print(f'arguments: {args[1:]}')
        return func(*args, **kwargs)
    return inner

def load_troels() -> List[Dict[str, str]]:
    with open('resources/citater.json', encoding='utf-8') as f:
        return json.load(f)

@log
async def play_mp3(ctx, filename):
    voice = ctx.author.voice
    if voice is not None:
        vc = await voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=f'resources/{filename}.mp3'))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
    else:
        await ctx.reply(
            f"Hey {ctx.author.name}!\nGå lige ind i en voice channel inden du be'r mig spille **{filename}** :wink:.",
            mention_author=False
        )

if __name__ == '__main__':
    quotes = load_troels()
    quote = quotes[-2]
    print(quote['quote'])
