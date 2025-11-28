from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

class NewsFetcher:
    def __init__(self, headless=True):
        self.headless = headless

    def get_headlines(self, url="https://news.ycombinator.com/"):
        """Fetches top headlines from Hacker News."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            print(f"Navigating to {url}...")
            page.goto(url)
            page.wait_for_selector(".titleline")
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        headlines = []
        for item in soup.select('.titleline > a'):
            link = item['href']
            # Handle relative links (though HN usually has absolute external links)
            if not link.startswith('http'):
                link = url + link
            headlines.append({
                'title': item.get_text(),
                'link': link
            })
        return headlines[:5]

    def get_article_text(self, url):
        """Fetches text content from a given URL."""
        print(f"Fetching article: {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            try:
                page.goto(url, timeout=30000)
                # specific handling for some common sites could go here
                # for now, getting all paragraph text is a reasonable heuristic
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                # Get text
                text = soup.get_text()

                # Break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # Drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)

            except Exception as e:
                print(f"Error fetching {url}: {e}")
                text = ""
            browser.close()
        return text
