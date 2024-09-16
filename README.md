# o1scraper

o1scraper is a Python-based tool that automatically extracts folded text data from ChatGPT conversations and saves it in JSON format. It features web automation capabilities using Playwright and improves usability by automating environment setup.

## Features

- Extraction of folded text elements from ChatGPT conversations
- JSON output with timestamp-based filenames
- Cleanup functionality for extracted data

## Prerequisites

- Windows 10
- Python 3.7 or higher
- Modern web browser (e.g., Microsoft Edge, Google Chrome)
- Browser must be launched in remote debugging mode

## Setup

1. **Clone or Download the Repository**
   
   Clone this repository to your local machine or download it as a ZIP file and extract it.

2. **Create and Activate a Virtual Environment**
   
   Create and activate a virtual environment:
   ```bash
   python -m venv o1scraper
   .\o1scraper\Scripts\activate  # For Windows
   ```

3. **Install Dependencies**
   
   With the virtual environment activated, run the following command to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Launch Browser in Remote Debugging Mode**
   
   Start your browser with remote debugging enabled. Here's an example using Microsoft Edge. Adjust the browser path and options as needed.
   - **For Microsoft Edge**:
     
     Create a shortcut and add the following to the target field:
     ```
     "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\edge_debug"
     ```
     
     **Note**: This command is an example. Modify the browser executable path and options according to your environment. The important flag is `--remote-debugging-port=9222`.

2. **Prepare ChatGPT Conversation Page**
   
   Open ChatGPT in your browser and navigate to the conversation page you want to extract data from.

3. **Run the Script**
   
   Open a command prompt, navigate to the project directory, and run the script:
   ```bash
   cd path\to\o1scraper
   python toggleopen.py
   ```
   After opening all toggles, run the following command to extract text:
   ```bash
   python text_extraction.py
   ```
   Finally, to clean up the extracted JSON file, run:
   ```bash
   python json_cleaner.py
   ```

## Output

- Extracted data is saved in the `extracted_data/` directory with timestamp-based filenames (e.g., `extracted_data_1726404502.json`).
- Cleaned data is saved in the `extracted_data/cleaned/` directory.

## Troubleshooting

- **If the script can't find the ChatGPT page**:
  - Ensure the browser is launched in remote debugging mode.
  - Check that the ChatGPT conversation page is correctly opened.
- **Dependency-related issues**:
  - After activating the virtual environment, try manually installing:
  ```bash
  pip install playwright
  playwright install chromium
  ```

## Disclaimer

Use this tool for educational purposes only. When using the script, comply with OpenAI's terms of service and applicable laws and regulations.