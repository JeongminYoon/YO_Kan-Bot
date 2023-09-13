from discord.ext import tasks, commands
import discord
import asyncio
from yt_dlp import YoutubeDL
import datetime










################# Setup ###################
###########################################
ffmpeg_options = {
            'options': '-vn',
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }

ffmpeg_location = "./ffmpeg/bin/ffmpeg" 


url_quick = ["https://youtu.be/YCZqgujSYUs", "https://youtu.be/51GIxXFKbzk", "https://youtu.be/ttVUZOkTxuM"]
###########################################
###########################################
        




################ Functions ################
##########################################
async def leave(self, num):
    self.server.pop(num)
    await self.bot.voice_clients[num].disconnect()

def server_check(self, channel: discord.VoiceChannel):
    server_num = None
    for server_num in range(0, len(self.bot.voice_clients)):
                if channel == self.bot.voice_clients[server_num].channel:
                    break
                else:
                    server_num = None
    return server_num

async def time_sum(result:datetime, a: datetime = datetime.timedelta(seconds=0), b: datetime = datetime.timedelta(seconds=0)):
    result += a + b
    return result
###########################################
###########################################





################# Class ###################
###########################################
class player():
    def __init__(self):
        
        self.q_list = []
        self.np_dic = {'title':'', 'duration':'', 'url':'', 'author':''}
        

    def queue_set(self, y_link, y_title, y_duration, o_url, o_author):
        q_dic = {'link':'', 'title':'', 'duration':'', 'url':'', 'author':''}
        q_dic['link'] = y_link
        q_dic['title'] = y_title
        q_dic['duration'] = datetime.timedelta(seconds=y_duration)
        q_dic['url'] = o_url
        q_dic['author'] = o_author
        self.q_list.append(q_dic)

        return self.q_list
    
    def nowplaying_set(self):

        self.np_dic['title'] = self.q_list[0]['title']
        self.np_dic['duration'] = self.q_list[0]['duration']
        self.np_dic['url'] = self.q_list[0]['url']
        self.np_dic['author'] = self.q_list[0]['author']

        return self.np_dic
    
    def channel_set(self, channel: discord.TextChannel):
        self.channel = channel

        return self.channel
        
###########################################
###########################################





################## DJ #####################
###########################################
class DJ(commands.Cog):

    
    
    def __init__(self, bot):
        self.bot = bot
        option = {
                'format':'bestaudio/best', 
                'noplaylist':True
                }
        self.DL = YoutubeDL(option)
        self.server = []

        self.out.start()



    

    ################# Methods #################
    ###########################################
    async def left(self):
        try:
            if self.bot.voice_clients is None:
                pass
            else:
                for i in range(0, len(self.bot.voice_clients)):
                    if self.bot.voice_clients[i].is_connected() is True and len(self.bot.voice_clients[i].channel.members) == 1:
                        await self.server[i].channel.send("*Never left without saying goodbye...*")
                        await leave(self, i)
                        
        except:
            pass
    ###########################################
    ###########################################





    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog: DJ is ready")


    @tasks.loop(seconds=0.1)
    async def out(self):
        await self.left()





    ################ Commands #################
    ###########################################

    @commands.command(name="play", aliases=["p", "P", "ㅔ"])
    async def play(self, ctx, url):

        
        
        server_0 = player()
        
        

        #단축키
        for i in range(0, len(url_quick)):
            if url == f"{i+1}":
                url = url_quick[i]
            else:
                pass

        
        #접속
        try:
            channel = ctx.author.voice.channel
        except:
            await ctx.reply("You are not in voice channel")
            return

        try:
            await channel.connect()
            server_num = server_check(self, channel)
            self.server.append(server_0)
            self.server[server_num].channel_set(ctx.channel)
        except:
            server_num = server_check(self, channel)

        
        
            
        
        #큐
        try:
            q_info = self.DL.extract_info(url, download=False)
        except:
            await ctx.reply("ERROR: URL invalid")


        if ctx.author.nick == None:
            author = ctx.author.name
        else:
            author = ctx.author.nick

        
        self.server[server_num].queue_set(q_info['url'], q_info['title'], q_info['duration'], url, author)

        queue_list = self.server[server_num].q_list

        q_num = len(queue_list) -1


        #큐 임베드
        if not ctx.voice_client.is_playing():
            pass
        else: 
            embed=discord.Embed(title='Queued', description=f'[{queue_list[q_num]["title"]}]({queue_list[q_num]["url"]})', color=discord.Color.from_rgb(255, 0, 0))
            embed.add_field(name='Position', value=f'{q_num + 1}')
            embed.add_field(name='Duration', value=f'{queue_list[q_num]["duration"]}', inline=True)
            embed.add_field(name='Requested by', value=f'{queue_list[q_num]["author"]}', inline=True)
            await ctx.send(embed=embed)
            return


        #재생 루프
        while True:

            try:
            
                if not ctx.voice_client.is_playing():

                    link = queue_list[0]['link']
                    title = queue_list[0]['title']
                    o_url = queue_list[0]['url'] 
                    o_author = queue_list[0]['author']
                    o_duration = queue_list[0]['duration']
                    
                    self.server[server_num].nowplaying_set()
                    queue_list.pop(0)

                    track = discord.FFmpegPCMAudio(link, **ffmpeg_options, executable=ffmpeg_location)
                    ctx.voice_client.play(track)

                    embed=discord.Embed(title='Play', description=f'[{title}]({o_url})', color=discord.Color.from_rgb(255, 0, 0))
                    embed.add_field(name='Duration', value=f'{o_duration}', inline=True)
                    embed.add_field(name='Requested by', value=f'{o_author}', inline=True)
                    await ctx.send(embed=embed)
                    


                else:
                    await asyncio.sleep(0.1)
                    
            
            except:
                break





    ###########################################
    ###########################################

    @commands.command(name="queue", aliases=["q", "Q", "ㅂ"])
    async def queue(self, ctx, num:int = 1):

        try:
            a_voice = ctx.author.voice.channel
        except:
            await ctx.reply("You are not in voice channel")
            return

        server_num = server_check(self, a_voice)

        

        embed = discord.Embed(title="Queue Info")
        q_num = len(self.server[server_num].q_list)
        playlist = ""
        playlist_page = []
        playlist_duration = []
        playlist_duration_t = datetime.timedelta(seconds=0)
        index = num-1
        count = 0

        if q_num == 0:
            embed.add_field(name='Empty', value='')
        
        else:
            for i in range(0, q_num):
                p_title = self.server[server_num].q_list[i]['title']
                p_url = self.server[server_num].q_list[i]['url']
                p_author = self.server[server_num].q_list[i]['author']
                p_duration = self.server[server_num].q_list[i]['duration']

                playlist_duration.append(p_duration)
        
                playlist += f"{i+1}. [{p_title}]({p_url}) | {p_duration} | {p_author}\n"
                count += 1
                
                #페이지당 7곡, 임베드 용량 초과하지 않도록 잘라냄
                if len(playlist) > 800 or count == 7:
                    playlist_page.append(playlist)
                    playlist = ""
                    count = 0
                #마지막 곡
                elif i+1 == q_num:
                    playlist_page.append(playlist)
            

            #총 재생시간 계산기 / 곡 갯수의 홀짝에 따라 다름
            p_list_len = len(playlist_duration) - 1
            
            if len(playlist_duration) % 2 == 0: #짝
                for i in range(0, len(playlist_duration)):
                    if i * 2 == len(playlist_duration):
                        break
                    playlist_duration_t = await time_sum(playlist_duration_t, playlist_duration[i], playlist_duration[p_list_len-i])
                    
            
            else: #홀
               for i in range(0, len(playlist_duration)):
                    if i * 2 == p_list_len:
                        playlist_duration_t = await time_sum(playlist_duration_t, playlist_duration[i])
                        break
                    playlist_duration_t = await time_sum(playlist_duration_t, playlist_duration[i], playlist_duration[p_list_len-i])
                    
                    
            embed.add_field(name=f'Lists {playlist_duration_t}', value=f"{playlist_page[index]}\n{num} / {len(playlist_page)}")

        await ctx.send(embed=embed)
    




    ###########################################
    ###########################################

    @commands.command(name="skip", aliases=["s", "S", "ㄴ"])
    async def skip(self, ctx):

        try:
            a_voice = ctx.author.voice.channel
        except:
            await ctx.reply("You are not in voice channel")
            return
        
        server_num = server_check(self, a_voice)
        
        if ctx.voice_client.is_playing():
            self.bot.voice_clients[server_num].stop()
            await ctx.send("Skipping...")
        elif not ctx.voice_client.is_playing():
            await ctx.send("Nothing to skip")
        




    ###########################################
    ###########################################
    
    @commands.command(name="leave", aliases=["l", "L", "ㅣ"])
    async def leave(self, ctx):

        try:
            a_voice = ctx.author.voice.channel
        except:
            await ctx.reply("You are not in voice channel")
            return

        server_num = server_check(self, a_voice)

        channel_id = self.bot.voice_clients[server_num].channel.id
        
        await leave(self, server_num)
        await ctx.send(f"Leave from <#{channel_id}>")
    

        


    ###########################################
    ###########################################

    @commands.command(name="delete", aliases=["d", "D", "ㅇ"]) 
    async def delete(self, ctx, num:int):

        index = num - 1

        try:
            a_voice = ctx.author.voice.channel
        except:
            await ctx.reply("You are not in voice channel")
            return

        server_num = server_check(self, a_voice)

        queue_list = self.server[server_num].q_list

        q_title = queue_list[index]['title']
        q_duration = queue_list[index]['duration']
        q_url = queue_list[index]['url']
        q_author = queue_list[index]['author']
        
        queue_list.pop(index)

        embed=discord.Embed(title='Deleted', description=f'[{q_title}]({q_url})', color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name='Position', value=f'{num}')
        embed.add_field(name='Duration', value=f'{q_duration}', inline=True)
        embed.add_field(name='Requested by', value=f'{q_author}', inline=True)
        await ctx.send(embed=embed)
    

        


    ###########################################
    ###########################################

    @commands.command(name="nowplaying", aliases=["np", "Np", "NP", "ㅞ"])
    async def now_playing(self, ctx):

        try:
            a_voice = ctx.author.voice.channel
        except:
            await ctx.reply("You are not in voice channel")
            return

        server_num = server_check(self, a_voice)
        
        nowplaying = self.server[server_num].np_dic

        if ctx.voice_client.is_playing():
            title = nowplaying['title']
            url = nowplaying['url']
            author = nowplaying['author']
            duration = nowplaying['duration']

            embed=discord.Embed(title='Now Playing', description=f'[{title}]({url})', color=discord.Color.from_rgb(255, 0, 0))
            embed.add_field(name='Duration', value=f'{duration}', inline=True)
            embed.add_field(name='Requested by', value=f'{author}', inline=True)
            await ctx.send(embed=embed)

        elif not ctx.voice_client.is_playing():
            await ctx.send("Nothing is playing")
            
            nowplaying['url'] = ''
            nowplaying['title'] = ''
            nowplaying['author'] = ''
            nowplaying['duration'] = ''
    




    ###########################################
    ###########################################

    @commands.command(name="quicknumber", aliases=["qn"])
    async def quick_number(self, ctx, num:int = 1):
        
        quicklist_page = []
        playlist = ""
        count = 0

        embed = discord.Embed(title="Quick Numbers")
        
        for i in range(0, len(url_quick)):
        
                playlist += f"{i+1}. {url_quick[i]}\n"
                count += 1
                
                #페이지당 7곡, 임베드 용량 초과하지 않도록 잘라냄
                if len(playlist) > 800 or count == 7:
                    quicklist_page.append(playlist)
                    playlist = ""
                    count = 0
                #마지막 곡
                elif i+1 == len(url_quick):
                    quicklist_page.append(playlist)
        
        embed.add_field(name=f'Lists', value=f"{quicklist_page[num-1]}\n{num} / {len(quicklist_page)}")

        await ctx.send(embed=embed)






if __name__ =='__main__':
    option = {
                'format':'bestaudio/best', 
                'noplaylist':True
                }
    self = YoutubeDL(option)
    url = "https://youtu.be/51GIxXFKbzk"
    data = self.extract_info(url, download=False)
    print(data.keys())

    


async def setup(bot):
    await bot.add_cog(DJ(bot))
