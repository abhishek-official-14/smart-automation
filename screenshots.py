import os
from playwright.sync_api import Page

class SmartVisionCapturer:
    @staticmethod
    def capture(page: Page, url: str, phase: str, target_dir: str) -> str:
        safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
        path = os.path.join(target_dir, f"{safe_name}_{phase}.png")
        page.screenshot(path=path)
        return path