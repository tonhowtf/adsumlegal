import logging
import configparser
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from core.commands.dl import VideoDownloader
from core.commands.observer import Observer


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


config = configparser.ConfigParser()
config.read("token.ini")
token = config["telegram"]["token"]


video_downloader = VideoDownloader(temp_dir="core/commands/downloaded")
observer = Observer(video_downloader)


async def observador(update, context):
    await observer.process_message(update, context)


def main() -> None:
    application = ApplicationBuilder().token(token).build()

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, observador))

    application.run_polling()


if __name__ == "__main__":
    main()
