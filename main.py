import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Replace the text below with your BotFather token
TOKEN = '8219016374:AAG_IWiB2Xu3EkNEdJ1tviFeJ4bU8jZqKlI'

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "x.com" in url or "twitter.com" in url:
        await update.message.reply_text("Downloading... ⏳")
        try:
            ydl_opts = {'outtmpl': 'video.mp4', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            await update.message.reply_video(video=open('video.mp4', 'rb'))
            os.remove('video.mp4')
        except Exception as e:
            await update.message.reply_text(f"Something went wrong. Make sure the link is public.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()
