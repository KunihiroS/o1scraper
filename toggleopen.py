import sys
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.DEBUG,  # ログレベルをDEBUGに設定
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_simple.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def click_toggle_buttons(page):
    # 記載されたセレクタでボタンを選択してクリック
    try:
        toggle_buttons = page.query_selector_all('div > button > div > svg')
        if toggle_buttons:
            for button in toggle_buttons:
                try:
                    if button.is_visible():
                        logging.info("Button found, attempting to click.")
                        button.click()
                        page.wait_for_timeout(1000)  # クリック後に待機
                    else:
                        logging.info("Button is not visible, skipping.")
                except Exception as e:
                    logging.error(f"Error clicking button: {e}")
        else:
            logging.info("No toggle buttons found.")
    except Exception as e:
        logging.error(f"Error during toggle button selection: {e}")

def run_scraper():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            logging.info("Connected to browser successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to browser: {e}")
            return

        try:
            contexts = browser.contexts
            for context in contexts:
                pages = context.pages
                for page in pages:
                    if "chatgpt.com" in page.url:
                        logging.info(f"ChatGPT page found: {page.url}")
                        page.set_viewport_size({"width": 1280, "height": 800})
                        page.wait_for_load_state('networkidle')
                        page.wait_for_timeout(5000)

                        click_toggle_buttons(page)  # トグルボタンをクリック

                        logging.info("Toggle button clicking completed.")
                        return
            logging.info("ChatGPT page not found.")
        finally:
            browser.close()

if __name__ == "__main__":
    try:
        run_scraper()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
