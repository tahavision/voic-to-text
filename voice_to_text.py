from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# اطلاعات API
TELEGRAM_TOKEN = '7787377930:AAGm0Bd-p1T0FdYmK1QC3WsiNxAO23EsIRQ'
DEEPGRAM_API_KEY = '6174bda8d250717378808b2b5c9da8dbac2dea7f'

# توابع مربوط به ربات
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! یک فایل صوتی ارسال کن تا متن آن را بهت بدم.')

def voice_handler(update: Update, context: CallbackContext) -> None:
    voice_file = update.message.voice.get_file()
    file_url = voice_file.file_path

    # دانلود فایل صوتی
    audio_response = requests.get(file_url)
    with open("voice.ogg", "wb") as f:
        f.write(audio_response.content)
    
    # آپلود فایل برای تبدیل به متن
    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': 'audio/ogg',
    }
    with open("voice.ogg", "rb") as audio:
        response = requests.post(
            'https://api.deepgram.com/v1/listen',
            headers=headers,
            data=audio
        )
    result = response.json()
    text = result['results']['channels'][0]['alternatives'][0]['transcript']
    
    # ارسال متن به کاربر
    update.message.reply_text(f'متن: {text}')

# راه اندازی ربات
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
