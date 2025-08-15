# Specific Movie Ticket Watch Bot

A Python bot that checks BookMyShow's Nandan Cinema page for (exmp:"Dhumketu (UA 13+)") availability and sends instant Telegram alerts when tickets are bookable.

## Features
- Checks next 7 days for listings
- Detects if booking button is clickable
- Sends Telegram message instantly when tickets are available
- Logs activity to `bot.log`

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
