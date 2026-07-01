import logging
import requests
from typing import List
from bs4 import BeautifulSoup

logger = logging.getLogger("Framework.SitemapParser")

class SitemapParser:
    @staticmethod
    def extract_urls(sitemap_url: str) -> List[str]:
        logger.info(f"Connecting to target sitemap map: {sitemap_url}")
        try:
            headers = {"User-Agent": "Mozilla/5.0 QA Automation Architect Engine"}
            response = requests.get(sitemap_url, headers=headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"Sitemap extraction dropped. Status Code: {response.status_code}")
                return []
            soup = BeautifulSoup(response.content, "xml")
            urls = [tag.text.strip() for tag in soup.find_all("loc") if tag.text]
            return list(set(urls))
        except Exception as e:
            logger.critical(f"Sitemap parsing exception thrown: {str(e)}")
            return []