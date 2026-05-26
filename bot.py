import os
import discord
import feedparser
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1448878999907340290

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_morning = ""
last_evening = ""

NEW_URL = "https://store.steampowered.com/feeds/newreleases.xml"
SALE_URL = "https://store.steampowered.com/feeds/daily_deals.xml"

@bot.event
async def on_ready():
    print(f"{bot.user} 起動")

    if not news_loop.is_running():
        news_loop.start()

@tasks.loop(minutes=1)
async def news_loop():
    global last_morning, last_evening

    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    channel = await bot.fetch_channel(CHANNEL_ID)

    # 朝7時 新作
    if now.hour == 7 and now.minute == 0:
        today = now.strftime("%Y-%m-%d")

        if today != last_morning:
            feed = feedparser.parse(NEW_URL)

            msg = "🆕 Steam新作 TOP3\n\n"

            for i, game in enumerate(feed.entries[:3], 1):
                msg += f"{i}. {game.title}\n{game.link}\n\n"

            await channel.send(msg)
            last_morning = today

    # 夜7時 セール
    if now.hour == 19 and now.minute == 0:
        today = now.strftime("%Y-%m-%d")

        if today != last_evening:
            feed = feedparser.parse(SALE_URL)

            msg = "💸 Steamセール TOP3\n\n"

            for i, game in enumerate(feed.entries[:3], 1):
                msg += f"{i}. {game.title}\n{game.link}\n\n"

            await channel.send(msg)
            last_evening = today

@bot.command()
async def test(ctx):
    await ctx.send("✅ tikubi bot 動作OK")

@bot.command()
async def new(ctx):
    feed = feedparser.parse(NEW_URL)

    msg = "🆕 Steam新作 TOP3\n\n"

    for i, game in enumerate(feed.entries[:3], 1):
        msg += f"{i}. {game.title}\n{game.link}\n\n"

    await ctx.send(msg)

@bot.command()
async def sale(ctx):
    feed = feedparser.parse(SALE_URL)

    msg = "💸 Steamセール TOP3\n\n"

    for i, game in enumerate(feed.entries[:3], 1):
        msg += f"{i}. {game.title}\n{game.link}\n\n"

    await ctx.send(msg)

bot.run(TOKEN)
