# AdsumLegal - Media Content Downloader

![Logo](https://img.shields.io/badge/Telegram-Bot-blue.svg)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**AdsumLegal** is a Telegram bot designed to help you download media content (videos and images) from popular social media platforms such as Instagram, TikTok, Reddit, and X (Twitter). Just send the link of any content, and the bot will take care of the rest: download the file and send it back to you.

## 🚀 Features

- **Support for Instagram, TikTok, Reddit, and X (Twitter)**: Send the link to any media content, and the bot will fetch and download the corresponding file for you.
- **Download videos and images**: The bot supports high-quality videos and images.
- **Hassle-free downloads**: With just a single click, the bot does all the work and sends the file back to you.
- **Content descriptions**: If available, the bot will also send the content description along with the media.

## 📦 How It Works

This project leverages the **Telegram API** and libraries like **Instaloader** and **yt-dlp** to download videos and images from the social platforms mentioned.

### Workflow:
1. The bot receives a message containing a media link (Instagram, TikTok, Reddit, or X).
2. The bot processes the content, downloads the corresponding file, and sends the media back to the user.
3. If the content has a description, it will be sent as well.

---

## 🔧 Running Locally

Follow the steps below to run **AdsumLegal** on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/Antonioreverso/adsumlegal.git
cd adsumlegal
```

### 2. Install dependencies

Create a virtual environment and install the necessary dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure the Telegram token

Create a file named `token.ini` in the project’s root directory with the following content:

```ini
[telegram]
token=YOUR_BOT_TOKEN_HERE
```

You can get the token by creating a bot via [BotFather](https://core.telegram.org/bots#botfather).

### 4. Run the bot

Once everything is configured, simply run the `main.py` script:

```bash
python main.py
```

Now, your bot will be up and running, ready to respond to the links you send it!

---

## 💡 How the Code Works

### 1. `main.py`
This file is the entry point for the bot. It configures and starts the **ApplicationBuilder** from the `python-telegram-bot` library, defines message handlers, and calls the `run_polling()` function to start listening for new messages.

### 2. `downloader.py`
This module contains the logic for **downloading** the videos and images. It uses the **Instaloader** library to download Instagram content and **yt-dlp** to download videos from other platforms (such as TikTok and Reddit).

### 3. `observer.py`
The **Observer** monitors incoming messages. It checks if the message contains a link to a supported platform (Instagram, TikTok, Reddit, X) and calls the `VideoDownloader` to process the content.

### 4. **Processing Flow**
   - **Receiving the link**: The bot receives a message containing a link.
   - **Identifying the platform**: The Observer checks whether the link belongs to a supported platform.
   - **Downloading**: The VideoDownloader downloads the video/image.
   - **Sending media**: The bot sends the file back to the user, along with the description if available.

---

## ⚡ Technologies Used

- [Python 3](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/)
- [Instaloader](https://instaloader.github.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [logging](https://docs.python.org/3/library/logging.html)
  
## 🔑 License

This project is licensed under the **MIT** license. See the [LICENSE](LICENSE) file for more details.

---

## 🤝 Contributing

Contributions are welcome! If you want to improve or add new features, feel free to open an **issue** or submit a **pull request**.

---

## 📝 Usage Examples

- **Instagram**: Send a link to any Instagram post and the bot will return the video or image.
  
  Example link:  
  `https://www.instagram.com/p/xyzabc123/`

- **TikTok**: Send a link to any TikTok video.
  
  Example link:  
  `https://www.tiktok.com/@username/video/1234567890`

- **Reddit**: The bot can also download videos and images from Reddit posts.
  
  Example link:  
  `https://www.reddit.com/r/funny/comments/abc123/`

- **X (Twitter)**: Send a link to a tweet with media, and the bot will download it.
  
  Example link:  
  `https://x.com/username/status/1234567890`

---

### 💬 Frequently Asked Questions

- **What if the bot doesn’t respond?**  
  Check if the token is correct and if the bot has been successfully started. If the issue persists, open an issue.

- **Can I add more social media platforms?**  
  Yes! The code is modular and easy to extend. Simply add the URL of other platforms in the `Observer`.

