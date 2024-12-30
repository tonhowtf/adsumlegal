import logging
from telegram import Update
from telegram.ext import ContextTypes
from core.commands.dl import VideoDownloader


class Observer:
    def __init__(self, video_downloader: VideoDownloader):
        self.video_downloader = video_downloader
        self.supported_urls = [
            "https://www.instagram.com",
            "https://www.tiktok.com",
            "https://www.reddit.com",
            "https://x.com",
        ]

    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        user = update.effective_user

        if any(user_message.startswith(url) for url in self.supported_urls):
            await self.video_downloader.handle_video_download(update)
        else:
            logging.info(f"{user}: {user_message}")
