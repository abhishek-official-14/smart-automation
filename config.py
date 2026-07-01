# import os
# import logging
# from dataclasses import dataclass, field
# from typing import List, Tuple

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler("framework.log", encoding="utf-8")
#     ]
# )

# @dataclass(frozen=True)
# class ViewportSize:
#     width: int
#     height: int

# @dataclass
# class FrameworkConfig:
#     sitemap_url: str = "https://easemytools.com/sitemap.xml"
#     max_workers: int = 1  # Live workflow dekhne ke liye isko 1 rakha hai taaki chaos na ho
#     max_retries: int = 3
#     page_timeout_ms: int = 30000
#     interaction_timeout_ms: int = 5000
#     headless: bool = False  # Live UI window open karne ke liye False rakha hai
    
#     base_artifact_dir: str = "artifacts"
#     downloads_dir: str = "artifacts/downloads"
#     screenshots_dir: str = "artifacts/screenshots"
#     logs_dir: str = "artifacts/logs"
#     reports_dir: str = "artifacts/reports"
#     videos_dir: str = "artifacts/videos"
#     traces_dir: str = "artifacts/traces"
    
#     viewports: List[Tuple[str, ViewportSize]] = field(default_factory=lambda: [
#         ("Desktop", ViewportSize(1920, 1080)),
#         ("Tablet", ViewportSize(768, 1024)),
#         ("Mobile", ViewportSize(375, 812))
#     ])

#     def __post_init__(self) -> None:
#         for directory in [self.base_artifact_dir, self.downloads_dir, self.screenshots_dir, 
#                           self.logs_dir, self.reports_dir, self.videos_dir, self.traces_dir]:
#             os.makedirs(directory, exist_ok=True)

# config = FrameworkConfig()






import os
import logging
import requests
from dataclasses import dataclass, field
from typing import List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("framework.log", encoding="utf-8")
    ]
)

@dataclass(frozen=True)
class ViewportSize:
    width: int
    height: int

@dataclass
class FrameworkConfig:
    sitemap_url: str = "https://easemytools.com/sitemap.xml"
    max_workers: int = 1  
    max_retries: int = 3
    page_timeout_ms: int = 10000  # <--- Ghata kar 10 second kar diya taaki dead proxy par wait na ho
    interaction_timeout_ms: int = 5000
    headless: bool = False  
    
    base_artifact_dir: str = "artifacts"
    downloads_dir: str = "artifacts/downloads"
    screenshots_dir: str = "artifacts/screenshots"
    logs_dir: str = "artifacts/logs"
    reports_dir: str = "artifacts/reports"
    videos_dir: str = "artifacts/videos"
    traces_dir: str = "artifacts/traces"
    
    viewports: List[Tuple[str, ViewportSize]] = field(default_factory=lambda: [
        ("Desktop", ViewportSize(1920, 1080)),
        ("Tablet", ViewportSize(768, 1024)),
        ("Mobile", ViewportSize(375, 812))
    ])

    @staticmethod
    def fetch_live_free_proxies() -> List[str]:
        """Live public APIs se proxies auto-fetch karta hai."""
        logging.info("🌐 Auto-generating fresh free proxy pool...")
        proxy_pool = []
        
        try:
            res = requests.get("https://api.proxyscrape.com/v4/free-proxy-list/http/any/all/all", timeout=6)
            if res.status_code == 200:
                lines = res.text.strip().split("\n")
                for line in lines[:8]:  # Top 8 active channels
                    if ":" in line:
                        proxy_pool.append(f"http://{line.strip()}")
        except Exception:
            pass

        try:
            if len(proxy_pool) < 4:
                res = requests.get("http://pubproxy.com/api/proxy?limit=3&format=json&http=true", timeout=6)
                if res.status_code == 200:
                    for p in res.json().get("data", []):
                        proxy_pool.append(f"http://{p['ip']}:{p['port']}")
        except Exception:
            pass
            
        return list(set(proxy_pool))

    def __post_init__(self) -> None:
        for directory in [self.base_artifact_dir, self.downloads_dir, self.screenshots_dir, 
                          self.logs_dir, self.reports_dir, self.videos_dir, self.traces_dir]:
            os.makedirs(directory, exist_ok=True)

config = FrameworkConfig()