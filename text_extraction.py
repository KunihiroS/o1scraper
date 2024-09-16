import sys
import logging
import json
import time
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def wait_for_page_stability(page):
    """
    ページの読み込みが安定するのを待つ
    """
    page.wait_for_load_state('domcontentloaded')  # DOMが完全に読み込まれたことを確認
    page.wait_for_timeout(5000)  # 5秒待機

def monitor_navigation(page, original_url):
    """
    ページのナビゲーションを監視し、ナビゲーションが発生したら元のページに戻る
    """
    def handle_navigation(url):
        if url != original_url:
            logging.warning(f"Navigation detected to {url}. Attempting to return to original page.")
            page.goto(original_url)
            wait_for_page_stability(page)

    page.on('framenavigated', lambda frame: handle_navigation(frame.url))

def extract_text_with_retry(page, max_retries=3):
    """
    テキスト抽出処理を最大max_retries回試行する
    """
    for attempt in range(max_retries):
        try:
            return extract_text_from_elements(page)
        except playwright._impl._api_types.Error as e:
            if "Execution context was destroyed" in str(e):
                logging.warning(f"Execution context destroyed. Retrying... (Attempt {attempt + 1}/{max_retries})")
                wait_for_page_stability(page)
            else:
                raise
    raise Exception("Max retries reached. Unable to extract text.")

def extract_text_from_elements(page):
    logging.info("Extracting HTML content from opened sections.")
    extracted_data = []
    
    # 全ての article 要素を取得
    articles = page.query_selector_all('article')
    logging.info(f"Found {len(articles)} articles.")
    
    for article in articles:
        try:
            # タイトルを含む要素を探す
            title_element = article.query_selector('strong.font-semibold')
            # コンテンツ部分を特定のクラスを持つ p タグから取得
            content_elements = article.query_selector_all('p.text-base')
            
            if title_element and content_elements:
                title = title_element.inner_text().strip()
                # HTMLそのものを抽出
                content_html = "".join([elem.evaluate('(element) => element.outerHTML') for elem in content_elements])
                
                if title and content_html:
                    extracted_data.append({
                        'title': title,
                        'content_html': content_html
                    })
                    logging.debug(f"Extracted title: {title[:30]}... content: {content_html[:100]}...")
                    
        except Exception as e:
            logging.error(f"Error extracting HTML: {e}")
    
    return extracted_data

def save_to_json(data, filename):
    """
    抽出したデータをJSON形式で保存する
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"Data saved to {filename}")

def run_extraction():
    """
    テキスト抽出のメイン処理
    """
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            logging.info("Connected to browser successfully.")
            
            for context in browser.contexts:
                for page in context.pages:
                    if "chatgpt.com" in page.url:
                        logging.info(f"ChatGPT page found: {page.url}")
                        original_url = page.url
                        
                        wait_for_page_stability(page)
                        monitor_navigation(page, original_url)
                        
                        try:
                            extracted_data = extract_text_with_retry(page)
                            
                            # 出力ディレクトリは extracted_data に保存
                            output_directory = 'extracted_data'
                            if not os.path.exists(output_directory):
                                os.makedirs(output_directory)
                            
                            # 抽出結果を保存 (例: extracted_data/extracted_data_1726487650.json)
                            timestamp = int(time.time())
                            filename = os.path.join(output_directory, f'extracted_data_{timestamp}.json')
                            save_to_json(extracted_data, filename)
                            
                            logging.info("Extraction and saving completed successfully.")
                            return
                        except Exception as e:
                            logging.error(f"Error during text extraction: {e}")
                            
            logging.info("ChatGPT page not found.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    try:
        run_extraction()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
