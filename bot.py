import os, re, requests, logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a Twitter/X link! 📹")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if 'x.com' not in url and 'twitter.com' not in url:
        await update.message.reply_text("Please send a Twitter/X link!")
        return
    
    # Extract tweet ID
    tweet_id = re.search(r'/status/(d+)', url).group(1)
    
    # Get tweet data with bearer token
    headers = {'Authorization': f'Bearer {os.getenv("TWITTER_BEARER")}'}
    json_data = requests.get(f'https://api.twitter.com/2/tweets/{tweet_id}?expansions=attachments.media_keys&media.fields=type,url,variants', headers=headers).json()
    
    # Find best video URL
    media = json_data.get('includes', {}).get('media', [])
    for m in media:
        if m['type'] == 'video':
            video_url = max((v['url'] for v in m['variants']), key=lambda x: int(x.get('bitrate', 0) or 0))
            await context.bot.send_video(update.effective_chat.id, video_url)
            return
    
    await update.message.reply_text("No video found or invalid link!")

if __name__ == '__main__':
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()
