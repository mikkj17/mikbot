import discord
import time

FFMPEG_OPTIONS = {
    'options': '-vn'
}

def parse_troels():
    with open('resources/citater.txt', encoding='utf-8') as f:
        quotes = f.read().split('\n\n\n')
    return [quote.split('\n\n') for quote in quotes]

async def join(ctx, channel):
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    
    await channel.connect()

async def play_mp3(ctx, filename):
    voice_channel = ctx.author.voice.channel
    await join(ctx, voice_channel)
    ctx.voice_client.play(discord.FFmpegPCMAudio(source=f'resources/{filename}.mp3', **FFMPEG_OPTIONS))
    while ctx.voice_client.is_playing():
        time.sleep(0.1)
    await ctx.voice_client.disconnect()

if __name__ == '__main__':
    quotes = parse_troels()
    print(quotes[-2])
