import discord
from discord.ext import commands

TOKEN = "あとで入れる"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("tikubi bot 起動")

bot.run(TOKEN)
