import discord
import time

def parse_troels():
    with open('resources/citater.txt', encoding='utf-8') as f:
        quotes = f.read().split('\n\n\n')
    return [quote.split('\n\n') for quote in quotes]

async def play_mp3(ctx, filename):
    voice = ctx.author.voice
    if voice is not None:
        vc = await voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=f'resources/{filename}.mp3'))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()

if __name__ == '__main__':
    quotes = parse_troels()
    print(quotes[-2])
