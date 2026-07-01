from typing import Dict, Any
from playwright.sync_api import Page

class PerformanceProfiler:
    @staticmethod
    def capture_metrics(page: Page) -> Dict[str, Any]:
        try:
            timing = page.evaluate("() => JSON.parse(JSON.stringify(window.performance.timing))")
            ttfb = timing.get("responseStart", 0) - timing.get("requestStart", 0)
            dom_ready = timing.get("domContentLoadedEventEnd", 0) - timing.get("navigationStart", 0)
            load_time = timing.get("loadEventEnd", 0) - timing.get("navigationStart", 0)
            return {"load_time_ms": max(load_time, 0), "dom_ready_ms": max(dom_ready, 0), "ttfb_ms": max(ttfb, 0)}
        except Exception:
            return {"load_time_ms": -1, "dom_ready_ms": -1, "ttfb_ms": -1}