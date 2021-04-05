import discord
import time

FFMPEG_OPTIONS = {
    'options': '-vn'
}

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
    else:
        await ctx.reply(
            f"Hey {ctx.author.name}!\nGå lige ind i en voice channel inden du be'r mig spille **{filename}** :wink:.",
            mention_author=False
        )

if __name__ == '__main__':
    quotes = parse_troels()
    print(quotes[-2])
