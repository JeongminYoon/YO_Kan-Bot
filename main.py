from discord.ext import tasks, commands
import discord
import os
from itertools import cycle


BOT_TOKEN = ""

status_message = ["더블 크래시 ", "[help "]


def main():
    
    bot = commands.Bot(command_prefix="[", intents=discord.Intents.all(), help_command=None)

    

    for filename in os.listdir('./cogs'):
        if'.py'in filename:
            filename = filename.replace('.py','')
            bot.load_extension(f"cogs.{filename}")

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
        bot.unload_extension(f"cogs.{extenseion}")
        bot.load_extension(f"cogs.{extenseion}")
        await ctx.send(f"{extenseion} reloaded")

    

    bot.run(BOT_TOKEN)

if __name__ =='__main__':
    main()
    






