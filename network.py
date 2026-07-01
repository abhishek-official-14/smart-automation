from typing import List, Dict, Any
from playwright.sync_api import Response

class NetworkObserver:
    def __init__(self) -> None:
        self.errors: List[Dict[str, Any]] = []

    def handle_response(self, response: Response) -> None:
        if response.status >= 400:
            self.errors.append({"url": response.url, "status": response.status, "text": response.status_text})