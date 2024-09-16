import os
import json
import logging
from bs4 import BeautifulSoup

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def clean_html_content(html_content):
    """
    HTMLコンテンツをクリーニングし、pタグ内のテキストを抽出する
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p', class_='text-base')
    cleaned_content = []
    for p in paragraphs:
        cleaned_content.append(p.get_text(strip=True))
    return " ".join(cleaned_content)

def process_json_file(filepath, output_directory):
    """
    JSONファイルを処理し、コンテンツのクリーニングを行う
    """
    logging.info(f"Processing file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_data = []
    for item in data:
        cleaned_item = {
            'title': item['title'],
            'content': clean_html_content(item['content_html'])
        }
        cleaned_data.append(cleaned_item)
    
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 処理後のデータを新しいファイルに保存
    cleaned_filename = f"cleaned_{os.path.basename(filepath)}"
    cleaned_filepath = os.path.join(output_directory, cleaned_filename)
    with open(cleaned_filepath, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    logging.info(f"Cleaned data saved to {cleaned_filepath}")

def process_all_json_files(input_directory, output_directory):
    """
    指定されたディレクトリ内のすべてのJSONファイルを処理し、cleanedディレクトリに保存する
    """
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            filepath = os.path.join(input_directory, filename)
            process_json_file(filepath, output_directory)

if __name__ == "__main__":
    input_directory = 'extracted_data'
    output_directory = os.path.join(input_directory, 'cleaned')

    # extracted_dataディレクトリ内のすべてのJSONファイルを処理し、cleanedディレクトリに保存
    process_all_json_files(input_directory, output_directory)
