
def test_news_fetcher():
    from news_agent.news_fetcher import NewsFetcher
    fetcher = NewsFetcher()
    headlines = fetcher.get_headlines()
    assert len(headlines) > 0
    assert 'title' in headlines[0]
    assert 'link' in headlines[0]
