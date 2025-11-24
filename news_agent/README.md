# Browser Reasoning Agent for News

This agent fetches news headlines from Hacker News, summarizes the articles using OpenAI's GPT-3.5, and generates an audio summary using Google Text-to-Speech.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

2.  (Optional) Set up OpenAI API Key:
    Create a `.env` file in the root directory:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```
    If no key is provided, the agent will use a mock summarizer.

## Usage

Run the agent from the repository root:

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 news_agent/main.py
```

### Options

*   `--limit`: Number of articles to process (default: 3).
*   `--headed`: Run the browser in visible mode (default: headless).

Example:
```bash
python3 news_agent/main.py --limit 5 --headed
```

## Output

The agent generates a file `news_summary.mp3` in the current directory.
