import telebot
import yt_dlp
import os

# MASUKKIN TOKEN LU DI SINI, LANGSUNG!
TOKEN = '8267618827:AAGYZtuOVCW5xQRAubahLRICkrFISwCzubE'
bot = telebot.TeleBot(TOKEN)

# ==========================================
# 📥 MODULE: VIDEO DOWNLOADER (TELEBOT VERSION)
# ==========================================
@bot.message_handler(commands=['dl', 'download'])
def download_video(message):
    # Cek apakah ada link setelah command
    text_split = message.text.split()
    if len(text_split) < 2:
        return bot.reply_to(message, "❌ Kasih link videonya, t*lol! Contoh: `/dl [link]`")
    
    url = text_split[1]
    msg = bot.reply_to(message, "📥 **Sabar, lagi gue colong videonya...**")

    # Folder buat nyimpen sementara
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        bot.edit_message_text("📤 **Lagi gue kirim, jangan bawel...**", message.chat.id, msg.message_id)
        
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption=f"✅ **Berhasil Colong:** {info.get('title', 'Video')}")
        
        # Hapus file setelah dikirim
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ **GAGAL!**\n`Error: {str(e)}`", message.chat.id, msg.message_id)

print("🐉 BLACK DRAGON SIMPLE DOWNLOADER (TOKEN ONLY) IS RUNNING!")
bot.infinity_polling()