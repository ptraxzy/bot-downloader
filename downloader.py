import telebot
import yt_dlp
import os

TOKEN = "MASUKKAN_TOKEN_ANDA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['dl', 'download'])
def download_video(message):
    text = message.text.split(maxsplit=1)

    if len(text) < 2:
        bot.reply_to(
            message,
            "❌ Link video tidak ditemukan.\nGunakan format:\n`/dl <link>`",
            parse_mode="Markdown"
        )
        return

    url = text[1]

    status_msg = bot.reply_to(
        message,
        "📥 Memproses permintaan, mohon tunggu..."
    )

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.edit_message_text(
            "📤 Mengirim video...",
            message.chat.id,
            status_msg.message_id
        )

        with open(filename, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption=f"✅ {info.get('title', 'Video berhasil dikirim')}"
            )

        os.remove(filename)
        bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Terjadi kesalahan:\n`{str(e)}`",
            message.chat.id,
            status_msg.message_id,
            parse_mode="Markdown"
        )

bot.infinity_polling()
