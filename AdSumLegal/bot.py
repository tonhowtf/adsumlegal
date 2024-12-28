import logging
import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Configuração de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def download_video(update: Update):
    video_url = update.message.text.strip()

    temp_dir = "."
    os.makedirs(temp_dir, exist_ok=True)
    video_path = os.path.join(temp_dir, "teste.mp4")
    image_path = os.path.join(temp_dir, "imagem.jpg")

    try:
        ytdlp_command = [
            "yt-dlp", video_url, "-o", video_path, "--format", "best[ext=mp4]"
        ]
        subprocess.run(ytdlp_command, check=True)

        await update.message.reply_video(video=open(video_path, "rb"))

    except subprocess.CalledProcessError as e:
        await update.message.reply_text("link errado")
    except Exception as e:
        await update.message.reply_text("Erro, contatar admin @picassoneves")

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

token = ""


async def observador(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_message = update.message.text
    user = update.message.from_user

    urls = ["https://www.instagram.com",
            "https://www.tiktok.com", "https://www.reddit.com"]

    if any(user_message.startswith(url) for url in urls):
        await download_video(update)
    else:
        logging.info(f"Mensagem ignorada de {user.first_name}: {user_message}")


"""                                            """


def main() -> None:

    application = ApplicationBuilder().token(token).build()

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, observador))

    application.run_polling()


if __name__ == "__main__":
    main()
