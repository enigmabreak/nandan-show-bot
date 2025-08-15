# Nandan Show Bot

A Python bot to monitor show listings for (MY usecase: **Dhumketu**) at Nandan Cinema on BookMyShow and notify via Telegram when tickets are available.

---

## Features

- Checks the next 7 days for show availability.
- Sends notifications via Telegram.
- Headless Chrome using Selenium for automated browsing.
- Logging to `bot.log`.

---

## Prerequisites

- Python 3.10+
- Google Chrome(Or any Compatible browser based on Chromium) installed
- Install ChromeDriver and place it in project folder (Go to setting and in the bottom Abot Chrome there find the version of u r install and select matching ChromeDriver from https://googlechromelabs.github.io/chrome-for-testing/)
- Telegram bot and chat ID

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/enigmabreak/nandan-show-bot.git
cd nandan-show-bot
````

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:


```bash
cp .env.example .env
```

* Fill in your `TELEGRAM_TOKEN` and `CHAT_ID`.

---

## Usage

### Run normally:

```bash
python bot.py
```

* The bot will check the next 7 days repeatedly (every 15 minutes by default) for ticket availability.
* Logs are written to `bot.log`.

### Test setup:

```bash
python bot.py test
```

* Opens a test webpage (`example.com`) via Selenium.
* Sends a test Telegram message to confirm your setup works.

---

## Stopping the Bot

* Press **Ctrl + C** in the terminal to stop manually.
* Closing the terminal will also stop the bot.

---

## Stuffs to keep on mind...

* Do **not** commit your `.env` file to GitHub.
* Ensure your Chrome version matches the ChromeDriver version.
* `requirements.txt` contains all necessary Python packages.
* Telegram test messages help verify your bot and chat ID configuration.
