# o1scraper

o1scraper is a Python-based tool designed to automatically extract folded text data from ChatGPT conversations and save it in a JSON format. It utilizes Playwright for web automation and includes an environment setup for ease of use.

## Features

- Automatic virtual environment setup
- Playwright installation and management
- Extraction of folded text elements from ChatGPT conversations
- JSON output with timestamp-based filenames
- Sorting of extracted data in reverse chronological order

## Prerequisites

- Windows 10
- Python 3.7 or higher
- A modern web browser (e.g., Microsoft Edge, Google Chrome)
- The browser must be started in debug mode with remote debugging enabled

## Setup

1. Clone or download this repository to your local machine.

2. Open Command Prompt and navigate to the project directory:
   ```
   cd path\to\o1scraper
   ```

3. Run the script:
   ```
   python main.py
   ```

   The script will automatically set up a virtual environment named `o1scraper`, activate it, and install the necessary dependencies.

## Usage

1. Start your browser with remote debugging enabled. Here's an example using Microsoft Edge (note that this is just an example and you may need to adjust the path or use a different browser):

   Create a shortcut to Edge and add the following to the target field:
   ```
   "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\edge_debug"
   ```

   Note: This is an example command. You may need to adjust the path to your browser executable or use a different browser altogether. The important part is the `--remote-debugging-port=9222` flag.

2. Open ChatGPT in the browser and navigate to the conversation you want to extract data from.

3. Open a new Command Prompt, navigate to the project directory, and run the script:
   ```
   cd path\to\o1scraper
   python main.py
   ```

4. The script will automatically find the ChatGPT tab, extract the folded text data, and save it to a JSON file in the current directory.

## Output

The extracted data will be saved in a file named `extracted_data_[timestamp].json` in the current directory. The JSON file will contain an array of objects, each with an `id` and `content` field.

## Troubleshooting

- If the script fails to find the ChatGPT page, ensure that you have an active ChatGPT conversation open in your browser started with the debug port.
- If you encounter any permission issues, try running Command Prompt as an administrator.
- For any dependency-related issues, try removing the `o1scraper` folder from the project directory and running the script again to recreate it.
- If you encounter issues with Playwright, you can try installing it manually:
  ```
  pip install playwright
  playwright install chromium
  ```
- If you're using a browser other than Microsoft Edge, make sure to adjust the browser launch command accordingly.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Be sure to comply with OpenAI's terms of service and any applicable laws and regulations when using this script.