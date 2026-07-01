from typing import List, Dict, Any
from playwright.sync_api import ConsoleMessage

class ConsoleTelemetryListener:
    def __init__(self) -> None:
        self.logs: List[Dict[str, Any]] = []

    def handle_message(self, message: ConsoleMessage) -> None:
        if message.type in ["error", "warning"]:
            self.logs.append({"type": message.type, "text": message.text})