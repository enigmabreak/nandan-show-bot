import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Config
BASE_URL = "https://in.bookmyshow.com/cinemas/kolk/nandan-kolkata/buytickets/NNKA/"
MOVIE_NAME = "Dhumketu (UA 13+)"
CHECK_INTERVAL = 900  # 15 min

# Logging setup
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Headless Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": message})
        logging.info(f"Sent Telegram message: {message}")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

def check_date(date_obj):
    date_str = date_obj.strftime("%Y%m%d")
    url = f"{BASE_URL}/{date_str}"
    driver.get(url)
    time.sleep(5)  # Wait for JS to load

    page_source = driver.page_source

    if MOVIE_NAME in page_source:
        btns = driver.find_elements(By.CSS_SELECTOR, "a.__showtime-link")
        available = any(btn.get_attribute("href") and not btn.get_attribute("disabled") for btn in btns)
        if available:
            send_telegram_message(f" {MOVIE_NAME} available on {date_obj.strftime('%d %B %Y')}!\nBook here: {url}")
            logging.info(f"[{date_str}] AVAILABLE — notified user.")
            return True
        else:
            logging.info(f"[{date_str}] Found but not bookable yet.")
    else:
        logging.info(f"[{date_str}] Not listed yet.")
    return False

def check_movie_showtimes():
    """Check the next 7 days for the movie."""
    today = datetime.today()
    for i in range(1, 8):  # next 7 days
        try:
            check_date(today + timedelta(days=i))
        except Exception as e:
            logging.error(f"Error checking date: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        print(" Sending test Telegram message...")
        send_telegram_message(" Test message from nandan-show-bot!")
        print(" Message sent. Check your Telegram.")
    else:
        logging.info(" Dhumketu Ticket Watch Bot started...")
        try:
            while True:
                check_movie_showtimes()
                logging.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n Stopped by user")
