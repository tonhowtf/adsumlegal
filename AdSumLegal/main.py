import logging
import configparser
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from core.commands.dl import VideoDownloader  # Importa a classe VideoDownloader


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


config = configparser.ConfigParser()
config.read("token.ini")
token = config["telegram"]["token"]


video_downloader = VideoDownloader(temp_dir="core/commands/downloaded")


async def observador(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Observa mensagens enviadas pelo usuário e decide como processá-las.
    """
    user_message = update.message.text
    urls = ["https://www.instagram.com", "https://www.tiktok.com",
            "https://www.reddit.com", "https://x.com", "https://safereddit.com"]

    if any(user_message.startswith(url) for url in urls):
        # Chama o método da classe
        await video_downloader.handle_video_download(update)
    else:
        logging.info(f"Mensagem recebida: {user_message}")


def main() -> None:
    application = ApplicationBuilder().token(token).build()

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, observador))

    application.run_polling()


if __name__ == "__main__":
    main()
