import os
import discord
import feedparser
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1448878999907340290

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_yahoo = ""
last_steam = ""

@bot.event
async def on_ready():
    print(f"{bot.user} 起動")
    news_loop.start()

    news_loop.start()

@tasks.loop(minutes=1)
async def news_loop():
    global last_yahoo, last_steam

    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        return

    # 朝7時 Yahooニュース
    if now.hour == 7 and now.minute == 0:
        today = now.strftime("%Y-%m-%d")

        if today != last_yahoo:
            feed = feedparser.parse(
                "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
            )

            msg = "☀️ Yahooニュース TOP3\n\n"

            for i, news in enumerate(feed.entries[:3], 1):
                msg += f"{i}. {news.title}\n{news.link}\n\n"

            await channel.send(msg)
            last_yahoo = today

    # 夜7時 Steamニュース
    if now.hour == 19 and now.minute == 0:
        today = now.strftime("%Y-%m-%d")

        if today != last_steam:
            feed = feedparser.parse(
                "https://store.steampowered.com/feeds/news.xml"
            )

            msg = "🌙 Steamニュース\n\n"

            for i, news in enumerate(feed.entries[:3], 1):
                msg += f"{i}. {news.title}\n{news.link}\n\n"

            await channel.send(msg)
            last_steam = today

bot.run(TOKEN)
