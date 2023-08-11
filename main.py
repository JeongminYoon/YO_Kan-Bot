from discord.ext import tasks, commands
import discord
import os
from itertools import cycle
import asyncio


BOT_TOKEN = ""

status_message = ["더블 크래시 ", "[help "]


async def main():
    
    bot = commands.Bot(command_prefix="[", intents=discord.Intents.all(), help_command=None)

    

    for filename in os.listdir('./cogs'):
        if'.py'in filename:
            filename = filename.replace('.py','')
            await bot.load_extension(f"cogs.{filename}")

    status = cycle(status_message)

    @tasks.loop(seconds=3)
    async def presence():
        await bot.change_presence(activity=discord.Game(next(status)))

    @bot.event
    async def on_ready():
        print("System: YO_Kan Online")
        presence.start()

    @bot.command(name="reload")
    async def reload(ctx, extenseion):
        await bot.unload_extension(f"cogs.{extenseion}")
        await bot.load_extension(f"cogs.{extenseion}")
        await ctx.send(f"{extenseion} reloaded")

    

    await bot.start(BOT_TOKEN)

asyncio.run(main())
    






