import os
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("twitter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Twitter Video Downloader! Send Twitter link")
@app.on_message(filters.text & ~filters.command("start"))
async def download(client: Client, message: Message):
    url = message.text
    if "twitter.com" in url or "x.com" in url or "t.co" in url:
        await message.reply("⏳ Downloading...")
        ydl_opts = {'outtmpl': '%(title)s.%(ext)s', 'format': 'best[height<=720]'}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            if os.path.exists(file_path):
                await message.reply_video(file_path, caption="Twitter Video")
                os.remove(file_path)
            else:
                await message.reply("❌ Download failed.")
        except Exception as e:
            await message.reply(f"❌ Error: {str(e)}")
    else:
        await message.reply("❌ Only Twitter/X links please!")

if __name__ == "__main__":
    app.run()
