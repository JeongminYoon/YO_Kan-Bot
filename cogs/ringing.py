from discord.ext import commands
import discord
import random
import glob
import asyncio

################ Message ##################
###########################################

message_success = ""
message_fail = ""
time = 3

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
        path = './mp3/*.mp3'
        link = glob.glob(path)
        ffmpeg_location = "./ffmpeg/bin/ffmpeg"
        check = [77, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 5, 2, 12, 22, 32, 42, 52, 62, 72, 82, 92]
        
        player = discord.FFmpegPCMAudio(executable=ffmpeg_location, source=link[0])

        # failed
        if rng in check:
            await ctx.send(f"{ctx.author.mention} tried ringing <#{channel.id}>.\n{message_fail}")
            return

        #succeed
        if self.bot.voice_clients == []:
            await channel.connect()
            ctx.voice_client.play(player)
            await ctx.send(f"{message_success}")
            await asyncio.sleep(time) 
            await self.bot.voice_clients[0].disconnect()
        else: 
            await ctx.send(f"I'm busy to ringing somewhere.")
        
        
        
def setup(bot):
    bot.add_cog(ringing(bot))
