from discord.ext import commands
import discord
import random
import glob
import asyncio
from mutagen.mp3 import MP3

################ Message ##################
###########################################

message_success = "ding-dong"
message_fail = "You IDIOT!"


###########################################
###########################################

class ringing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        option = {
                'format':'bestaudio/best', 
                'noplaylist':True
                }
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog: ringing is ready")
    

    @commands.command(name="ringing")
    async def ringing(self, ctx, channel: discord.VoiceChannel):
        await ctx.message.delete()
        rng = random.randint(0,100)
        path = "./mp3/*.mp3"
        link = glob.glob(path)
        audio = MP3(link[0])
        
        ffmpeg_location = "./ffmpeg/bin/ffmpeg"
        
        
        player = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=link[0])

        # failed
        if rng in range(1,31): # 30%
            await ctx.send(f"{ctx.author.mention} tried ringing <#{channel.id}>.\n{message_fail}")
            return

        #succeed
        if self.bot.voice_clients == []:
            await channel.connect()
            ctx.voice_client.play(player)
            await ctx.send(f"{message_success}")
            await asyncio.sleep(audio.info.length) 
            await self.bot.voice_clients[0].disconnect()
        else: 
            await ctx.send(f"I'm busy to ringing somewhere.")
        
        
        
async def setup(bot):
    await bot.add_cog(ringing(bot))
