import os
import argparse
from news_agent.news_fetcher import NewsFetcher
from news_agent.summarizer import Summarizer
from news_agent.audio_generator import AudioGenerator
from dotenv import load_dotenv

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Browser Reasoning Agent for Hacker News")
    parser.add_argument("--limit", type=int, default=3, help="Number of articles to process")
    parser.add_argument("--headed", action='store_true', help="Run browser in headed mode (visible)")

    args = parser.parse_args()

    # Initialize components
    fetcher = NewsFetcher(headless=not args.headed)

    summarizer = Summarizer()
    audio_gen = AudioGenerator()

    print(f"Fetching headlines from Hacker News...")
    headlines = fetcher.get_headlines() # Uses default URL

    full_summary = "Here is your news summary. "

    for i, item in enumerate(headlines[:args.limit]):
        print(f"Processing {i+1}/{args.limit}: {item['title']}")

        # Fetch article content
        article_text = fetcher.get_article_text(item['link'])

        if not article_text:
            print("Could not fetch article text. Skipping.")
            continue

        # Summarize
        print("Summarizing...")
        summary = summarizer.summarize(article_text)
        print(f"Summary: {summary}")

        full_summary += f"Article {i+1}: {item['title']}. {summary} "

    print("Generating audio...")
    audio_gen.generate_audio(full_summary, "news_summary.mp3")
    print("Done! Check news_summary.mp3")

if __name__ == "__main__":
    main()
