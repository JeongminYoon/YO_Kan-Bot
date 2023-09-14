from discord.ext import commands
import discord
import os


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog: help is ready")
    
    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="Commands", description = "Prefix: [",color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name=":exclamation: Caution", value="Don't kick him manually in voicechannel \nplease use ' [l ' when make him leave" ,inline=False)
        embed.add_field(name=":musical_note: Music", value="***Play music***\nplay, p, P (url or quick number) (*selective* insert number)\n\n***Quick number list***\nquicknumber, qn\n\n***Skip music***\nskip, s, S\n\n***Queue list***\nqueue, q, Q (page number/without, it shows first page)\n\n***Leave channel***\nleave, l, L\n\n***Delete music***\ndelete, d, D (queue number of music)\n\n***Now playing***\nnowplaying, np, Np, NP\n" ,inline=False)
        embed.add_field(name=":bell: Ringing / Ringing to designated channel\n", value="ringing (voice channel mention)", inline=False)
        

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))