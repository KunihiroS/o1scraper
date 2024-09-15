import sys
import os
import venv
import subprocess
import json
import time
import logging
from pathlib import Path
from subprocess import CalledProcessError

VENV_NAME = 'o1scraper'
REQUIREMENTS_FILE = 'requirements.txt'  # 依存関係を明示的に管理

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_venv_path():
    return Path(os.getcwd()) / VENV_NAME


def get_python_path():
    venv_path = get_venv_path()
    if sys.platform == "win32":
        return venv_path / 'Scripts' / 'python.exe'
    return venv_path / 'bin' / 'python'


def get_pip_path():
    venv_path = get_venv_path()
    if sys.platform == "win32":
        return venv_path / 'Scripts' / 'pip.exe'
    return venv_path / 'bin' / 'pip'


def create_venv():
    venv_path = get_venv_path()
    if not venv_path.exists():
        logging.info(f"Creating virtual environment: {VENV_NAME}")
        venv.create(venv_path, with_pip=True)
    else:
        logging.info(f"Virtual environment {VENV_NAME} already exists")


def run_command(command):
    try:
        logging.debug(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with error: {e.stderr}")
        raise


def install_requirements():
    pip_path = get_pip_path()
    if REQUIREMENTS_FILE and Path(REQUIREMENTS_FILE).exists():
        run_command([str(pip_path), 'install', '-r', REQUIREMENTS_FILE])
    else:
        run_command([str(pip_path), 'install', 'playwright'])
    # Playwrightのブラウザをインストール
    run_command([str(pip_path), 'exec', 'playwright', 'install', 'chromium'])
    logging.info("Required libraries installed successfully.")


def check_and_install_requirements():
    python_path = get_python_path()
    try:
        run_command([str(python_path), '-c', 'import playwright'])
        logging.info("Playwright is already installed.")
    except CalledProcessError:
        logging.info("Installing Playwright...")
        install_requirements()


def setup_environment():
    create_venv()
    check_and_install_requirements()


def extract_folded_text(page):
    try:
        folded_elements = page.query_selector_all('div[class*="text-base has-[strong]:mb-1 has-[strong]:mt-3"]')
    except Exception as e:
        logging.error(f"Failed to find folded elements: {e}")
        return []

    extracted_data = []

    for index, element in enumerate(folded_elements):
        try:
            element.click()
            # 動的なコンテンツの読み込みを待機
            page.wait_for_timeout(500)  # 0.5秒待機
            text_content = element.inner_text()
            data = {
                "id": index + 1,
                "content": text_content
            }
            extracted_data.append(data)
        except Exception as e:
            logging.warning(f"Failed to extract text from element {index + 1}: {e}")

    return extracted_data


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"Data saved to {filename}")


def run_scraper():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            logging.error(f"Failed to connect to browser: {e}")
            logging.info("Ensure the browser is running with remote debugging enabled.")
            return

        for context in browser.contexts:
            for page in context.pages:
                if "chatgpt.com" in page.url:
                    logging.info(f"ChatGPT page found: {page.url}")
                    extracted_data = extract_folded_text(page)
                    extracted_data.sort(key=lambda x: x['id'], reverse=True)
                    timestamp = int(time.time())
                    filename = f'extracted_data_{timestamp}.json'
                    save_to_json(extracted_data, filename)
                    return

        logging.info("ChatGPT page not found")


def main():
    setup_environment()
    run_scraper()


def is_venv_active():
    return 'VIRTUAL_ENV' in os.environ


def activate_venv_and_run():
    venv_path = get_venv_path()
    activate_script = venv_path / 'Scripts' / 'activate.bat'

    if sys.platform == "win32":
        # Windowsの場合、新しいCMDウィンドウで仮想環境をアクティベートしてスクリプトを再実行
        cmd_command = f'start cmd.exe /k "{activate_script} && python {os.path.abspath(__file__)}"'
    else:
        # Unix系システムの場合、新しいシェルウィンドウで仮想環境をアクティベートしてスクリプトを再実行
        cmd_command = f'gnome-terminal -- bash -c "source {activate_script} && python {os.path.abspath(__file__)}"'

    logging.info("Launching a new terminal with the virtual environment activated...")
    subprocess.Popen(cmd_command, shell=True)
    sys.exit(0)


if __name__ == "__main__":
    try:
        if not is_venv_active():
            venv_path = get_venv_path()
            if not venv_path.exists():
                logging.info("Setting up virtual environment...")
                setup_environment()
                logging.info("Virtual environment created.")
            else:
                logging.info("Virtual environment already exists.")
            activate_venv_and_run()
        else:
            logging.info("Virtual environment is active.")
            main()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
