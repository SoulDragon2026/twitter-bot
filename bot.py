import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

# Get these: my.telegram.org/apps & @BotFather
API_ID = 12345678  # Replace with YOUR API_ID
API_HASH = "your_api_hash_here"  # Replace
BOT_TOKEN = "your_bot_token_here"  # Replace

app = Client("twitter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("🔥 Send Twitter/X video link! Supports threads too.")

@app.on_message(filters.text & ~filters.command("start"))
async def handle_message(client: Client, message: Message):
    url = message.text
    if "twitter.com" in url or "x.com" in url or "t.co" in url:
        await message.reply("⏳ Downloading video...")
        
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best[height<=720]'
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            
            if os.path.exists(file_path):
                await message.reply_video(file_path, caption=info.get('title', 'Twitter Video'))
                os.remove(file_path)  # Clean up
            else:
                await message.reply("❌ Download failed.")
        except Exception as e:
            await message.reply(f"Error: {str(e)}")
    else:
        await message.reply("❌ Only Twitter/X links please!

Example: https://x.com/username/status/123456")

if __name__ == "__main__":
    app.run()
