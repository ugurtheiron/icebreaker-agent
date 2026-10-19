"""Tools used by the agents: a Tavily web search and a Firecrawl product-page extractor.

The Tavily helper is derived from tools/tools.py of Eden Marco's LangChain course
(https://github.com/emarco177/langchain-course, Apache-2.0, see NOTICE).
Changed by Uğur Özdemir: added the Firecrawl extractor and moved the Firecrawl API
key to the FIRECRAWL_API_KEY environment variable.
"""

import argparse

from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel

from env_utils import require_env

load_dotenv()


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res


class EcommerceProductSchema(BaseModel):
    product_name: str
    product_category: str
    barcode_code: str
    seller_name: str
    stock: str


# Example product pages used when the script is run without arguments
DEFAULT_URLS = [
    "https://www.propointsports.com/urun/k-swiss-speed-trac-41-5",
    "https://www.decathlon.com.tr/p/yetiskin-tenis-raketi-270-g-tr160-lite/_/R-p-171345?mc=8489539",
]


def scrape_product_pages(urls):
    """Extract structured product data from each URL with Firecrawl.

    Requires FIRECRAWL_API_KEY. Failures are reported per URL and do not stop the loop.
    Returns the list of extracted dicts (one per URL that succeeded).
    """
    app = FirecrawlApp(api_key=require_env("FIRECRAWL_API_KEY"))

    results = []
    for url in urls:
        try:
            data = app.scrape_url(url, {
                'formats': ['json'],
                'jsonOptions': {
                    'schema': EcommerceProductSchema.model_json_schema(),
                }
            })
            print("--------------------")
            print(data["json"])
            results.append(data["json"])
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
    return results


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Extract structured product data (name, category, barcode, seller, stock) with Firecrawl."
    )
    parser.add_argument(
        "urls",
        nargs="*",
        default=DEFAULT_URLS,
        help="product page URLs (default: two example product pages)",
    )
    args = parser.parse_args(argv)
    scrape_product_pages(args.urls)


if __name__ == "__main__":
    main()
