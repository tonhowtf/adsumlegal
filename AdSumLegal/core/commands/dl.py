import os
import re
import subprocess
import instaloader
import logging
from telegram import Update


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class VideoDownloader:
    def __init__(self, temp_dir="."):
        self.temp_dir = temp_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        logger.info(f"Diretório temporário configurado: {self.temp_dir}")

    def clear_temp_dir(self):
        logger.info("Limpando o diretório temporário...")
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                os.remove(os.path.join(root, file))
                logger.info(f"Arquivo removido com sucesso :3")

    def download_content(self, content_url: str) -> dict:
        self.clear_temp_dir()

        if "instagram.com" in content_url:
            shortcode = content_url.split("?", 1)[0].rsplit("/")[-2]
            # match = re.search(   r"instagram\.com\/p\/([A-Za-z0-9_-]+)", content_url)

            if not content_url:
                raise ValueError("Culpa do rato")

            # shortcode = match.group(1)
            target_dir = os.path.join(self.temp_dir, "instagram_download")
            os.makedirs(target_dir, exist_ok=True)

            idl = instaloader.Instaloader(
                download_pictures=True,
                download_videos=True,
                download_comments=False,
                save_metadata=False,
                dirname_pattern=target_dir,
            )
            idl.context.log = lambda *args, **kwargs: None

            try:
                logger.info(
                    f"shortcode: {shortcode}")
                post = instaloader.Post.from_shortcode(idl.context, shortcode)
                idl.download_post(post, target=target_dir)

                files = [os.path.join(target_dir, f)
                         for f in os.listdir(target_dir)]
                media_files = [
                    f for f in files if f.endswith((".jpg", ".mp4"))]
                description_file = next(
                    (f for f in files if f.endswith(".txt")), None
                )

                description = ""
                if description_file and os.path.exists(description_file):
                    with open(description_file, 'r', encoding="utf-8") as f:
                        description = f.read().strip()
                        logger.info(f"Descrição: {
                                    description_file}")
                if not media_files:
                    raise RuntimeError("Nenhum arquivo de mídia foi baixado.")

                return {"media_files": media_files, "description": description}
            except Exception as e:
                raise RuntimeError(f"Erro durante o download: {e}")

        else:
            video_path = os.path.join(self.temp_dir, "video.mp4")
            try:
                ytdlp_command = [
                    "yt-dlp",
                    content_url,
                    "-o",
                    os.path.join(self.temp_dir, "video.%(ext)s"),
                    "--merge-output-format",
                    "mp4",
                ]
                subprocess.run(ytdlp_command, check=True)
                if not os.path.exists(video_path):
                    raise RuntimeError("Erro na criação.")
                return {"media_files": [video_path], "description": ""}
            except subprocess.CalledProcessError:
                raise ValueError("Erro na URL.")
            except Exception as e:
                raise RuntimeError(f"Erro durante o download: {e}")

    async def handle_video_download(self, update: Update):
        content_url = update.message.text.strip()
        try:
            result = self.download_content(content_url)
            media_files = result["media_files"]
            description = result["description"]

            if description:
                formatted_description = f"```{description}```"
                await update.message.reply_text(formatted_description, parse_mode="Markdown")

            for media in media_files:
                if media.endswith(".mp4"):
                    await update.message.reply_video(video=open(media, "rb"))
                elif media.endswith(".jpg"):
                    await update.message.reply_photo(photo=open(media, "rb"))

            self.clear_temp_dir()

        except ValueError as e:
            await update.message.reply_text(f"Erro: {e}")
        except RuntimeError as e:
            await update.message.reply_text(f"Erro: {e}")
