import pytest

from tools import tools


def test_firecrawl_extractor_requires_api_key(monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="FIRECRAWL_API_KEY"):
        tools.scrape_product_pages(["https://example.com/product/1"])


def test_scrape_product_pages_reads_key_from_environment_and_skips_failures(monkeypatch, capsys):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = []

    class FakeFirecrawlApp:
        def __init__(self, api_key):
            self.api_key = api_key

        def scrape_url(self, url, params):
            calls.append((self.api_key, url, params))
            if url.endswith("/broken"):
                raise RuntimeError("boom")
            return {"json": {"product_name": "Widget", "product_category": "Tennis"}}

    monkeypatch.setattr(tools, "FirecrawlApp", FakeFirecrawlApp)

    results = tools.scrape_product_pages(
        ["https://example.com/product/1", "https://example.com/product/broken"]
    )

    assert results == [{"product_name": "Widget", "product_category": "Tennis"}]
    assert [api_key for api_key, _, _ in calls] == ["test-key", "test-key"]
    schema = calls[0][2]["jsonOptions"]["schema"]
    assert set(schema["properties"]) == {
        "product_name",
        "product_category",
        "barcode_code",
        "seller_name",
        "stock",
    }
    assert "Error processing URL https://example.com/product/broken: boom" in capsys.readouterr().out
