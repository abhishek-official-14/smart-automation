import os
from typing import Dict, Any
from playwright.sync_api import Download

class SmartDownloadTracker:
    @staticmethod
    def process_download(download: Download, target_dir: str) -> Dict[str, Any]:
        try:
            path = os.path.join(target_dir, download.suggested_filename)
            download.save_as(path)
            return {"success": True, "filename": download.suggested_filename, "size": os.path.getsize(path)}
        except Exception as e:
            return {"success": False, "error": str(e)}