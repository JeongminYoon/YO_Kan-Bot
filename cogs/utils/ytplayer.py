from discord.ext import commands
import discord
import asyncio
from youtube_dl import YoutubeDL

ffmpeg_options = {
            'options': '-vn',
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }

async def player(ctx, voice: discord.VoiceClient, ffmpeg_location):
    with open('./cogs/utils/playlists.txt', "r") as pl:
        
        i = 0
        
        while True:

            if not voice.is_playing():
                break

            
            queue = pl.readlines()
            data = YoutubeDL.extract_info(f"{queue[i]}")
            link = data['url']
            title = data['title']
        
            #재생
            track = discord.FFmpegPCMAudio(link, **ffmpeg_options, executable=ffmpeg_location)
            ctx.voice_client.play(track)

            embed=discord.Embed(title=title, url=f'{queue[i]}', description=f'by {ctx.author.name}', color=discord.Color.from_rgb(255, 0, 0))
            await ctx.send(embed=embed)
            i += 1

            
                     