import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from commands.dl import VideoDownloader


idl = instaloader.Instaloader(download_pictures=True)

post_url = "https://www.instagram.com/p/DCuqIysPMoh/"

try:
    post = instaloader.Post.from_shortcode(idl.context, "DCuqIysPMoh")
    idl.download_post(post, target="downloaded")
    print("Downloaded")
except Exception as e:
    print(f"Erro: {e}")
