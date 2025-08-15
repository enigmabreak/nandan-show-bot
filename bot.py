import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = "https://in.bookmyshow.com/cinemas/kolk/nandan-kolkata/buytickets/NNKA/"
MOVIE_NAME = "Dhumketu"
CHECK_INTERVAL = 900

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": message})
        logging.info(f"Sent Telegram message: {message}")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

def check_date(driver, date_obj):
    date_str = date_obj.strftime("%Y%m%d")
    url = f"{BASE_URL}/{date_str}"
    driver.get(url)
    time.sleep(120)

    try:
        movie_link = driver.find_element(By.LINK_TEXT, MOVIE_NAME)
        movie_container = movie_link.find_element(By.XPATH, './ancestor::div[contains(@class, "sc-lswCgP")]')
        btns = movie_container.find_elements(By.CSS_SELECTOR, "a.__showtime-link")

        available = any(btn.get_attribute("href") and not btn.get_attribute("disabled") for btn in btns)
        
        if available:
            send_telegram_message(f"{MOVIE_NAME} available on {date_obj.strftime('%d %B %Y')}!\nBook here: {url}")
            logging.info(f"[{date_str}] AVAILABLE — notified user.")
            return True
        else:
            logging.info(f"[{date_str}] Found but not bookable yet.")
            return False

    except NoSuchElementException:
        logging.info(f"[{date_str}] Not listed yet.")
        return False
    except Exception as e:
        logging.error(f"Error checking date {date_str}: {e}")
        return False

def check_movie_showtimes():
    today = datetime.today()
    driver = create_driver()
    try:
        for i in range(1, 8):
            try:
                check_date(driver, today + timedelta(days=i))
            except Exception as e:
                logging.error(f"Error checking date: {e}")
    finally:
        driver.quit()

def selenium_test():
    driver = create_driver()
    driver.get("https://example.com")
    print("Test page title:", driver.title)
    driver.quit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        selenium_test()
        print("Sending test Telegram message...")
        send_telegram_message("Test message from nandan-show-bot!")
        print("Message sent. Check your Telegram.")
    else:
        logging.info("Dhumketu Ticket Watch Bot started...")
        try:
            while True:
                check_movie_showtimes()
                logging.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopped by user")