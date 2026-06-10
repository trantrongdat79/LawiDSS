from src.agent.tools.web_scraper_tool import WebScraperTool


def test_scraper_extracts_readable_html():
    html = """
    <html>
      <head><title>Case title</title><script>ignored()</script></head>
      <body><nav>Ignore me</nav><article>Main article text about labor law.</article></body>
    </html>
    """
    scraper = WebScraperTool(fetcher=lambda url: html)

    result = scraper.scrape("https://example.com/case")

    assert result["status"] == "success"
    assert result["title"] == "Case title"
    assert "Main article text" in result["content_excerpt"]
    assert "Ignore me" not in result["content_excerpt"]


def test_scraper_rejects_invalid_url():
    scraper = WebScraperTool(fetcher=lambda url: "")

    result = scraper.scrape("not-a-url")

    assert result["status"] == "failed"
    assert "Invalid URL" in result["error"]


def test_scraper_handles_empty_html():
    scraper = WebScraperTool(fetcher=lambda url: "")

    result = scraper.scrape("https://example.com/empty")

    assert result["status"] == "failed"


def test_scraper_truncates_long_content():
    scraper = WebScraperTool(fetcher=lambda url: "<title>T</title>" + ("x" * 100), max_chars=10)

    result = scraper.scrape("https://example.com/long")

    assert result["status"] == "success"
    assert len(result["content_excerpt"]) <= 10
