# import logging
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from typing import Dict, Any, List
# from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

# from config import config
# from sitemap import SitemapParser
# from detector import PageTypeDetector
# from executor import SmartInteractionExecutor
# from validators import AutomationValidator
# from performance import PerformanceProfiler
# from seo import SEOLintEngine
# from accessibility import AccessibilityAuditor
# from network import NetworkObserver
# from console import ConsoleTelemetryListener
# from downloads import SmartDownloadTracker
# from screenshots import SmartVisionCapturer
# from report import EnterpriseReportAggregator

# logger = logging.getLogger("Framework.CoreEngine")

# class EnterpriseAutomationEngine:
#     def __init__(self) -> None:
#         self.urls = SitemapParser.extract_urls(config.sitemap_url)
#         self.master_records: List[Dict[str, Any]] = []

#     def execute_framework(self) -> None:
#         if not self.urls:
#             logger.critical("Framework shutdown: sitemap extraction failed or 0 targets loaded.")
#             return

#         logger.info(f"Starting parallel engine sweep. Active processes: {config.max_workers}")
#         with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
#             futures = {executor.submit(self._process_url_with_retry, url): url for url in self.urls}
#             for f in as_completed(futures):
#                 res = f.result()
#                 if res: self.master_records.append(res)

#         reporter = EnterpriseReportAggregator(self.master_records, config.reports_dir)
#         reporter.generate_all()
#         logger.info("Automation workflow executed completely. System reports finalized inside artifacts/reports/ folder.")

#     def _process_url_with_retry(self, url: str) -> Dict[str, Any]:
#         for attempt in range(1, config.max_retries + 1):
#             try:
#                 return self._execute_page_lifecycle(url)
#             except Exception as e:
#                 if attempt == config.max_retries:
#                     return {"url": url, "status": "FAILED", "page_classification": "Crash", "failure_reason": str(e)}
#         return {}

#     def _execute_page_lifecycle(self, url: str) -> Dict[str, Any]:
#         with sync_playwright() as p:
#             # LIVE Browser Engine Window setup (slow_mo controls execution pace)
#             browser: Browser = p.chromium.launch(
#                 headless=config.headless, 
#                 slow_mo=800, 
#                 args=["--no-sandbox"]
#             )
            
#             vp = config.viewports[0][1]
#             context: BrowserContext = browser.new_context(viewport={"width": vp.width, "height": vp.height}, accept_downloads=True)
#             page: Page = context.new_page()

#             net_spy = NetworkObserver()
#             con_spy = ConsoleTelemetryListener()
#             page.on("response", net_spy.handle_response)
#             page.on("console", con_spy.handle_message)

#             try:
#                 page.goto(url, wait_until="networkidle", timeout=config.page_timeout_ms)
#                 raw_html = page.content()
                
#                 dom = PageTypeDetector.analyze_dom(raw_html)
#                 perf = PerformanceProfiler.capture_metrics(page)
#                 seo = SEOLintEngine.audit_page(raw_html)
#                 a11y = AccessibilityAuditor.run_audit(page)
                
#                 SmartVisionCapturer.capture(page, url, "initial", config.screenshots_dir)
                
#                 validator = AutomationValidator(page)
#                 initial_state = validator.capture_state_snapshot()
                
#                 executor_engine = SmartInteractionExecutor(page)
#                 actions = executor_engine.interact_with_page(dom["metrics"])
                
#                 page.wait_for_timeout(1000) # Settle down time frame
#                 SmartVisionCapturer.capture(page, url, "final", config.screenshots_dir)
                
#                 is_valid, errs, fix = validator.validate_runtime_mutations(initial_state)
                
#                 return {
#                     "url": url, "status": "PASSED" if is_valid else "FAILED", "page_classification": dom["classification"],
#                     "performance": perf, "seo": seo, "accessibility": a11y, "actions": actions, "failure_reason": " | ".join(errs)
#                 }
#             finally:
#                 context.close()
#                 browser.close()

# if __name__ == "__main__":
#     engine = EnterpriseAutomationEngine()
#     engine.execute_framework()








# import logging
# import random
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from typing import Dict, Any, List
# from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

# from config import config
# from sitemap import SitemapParser
# from detector import PageTypeDetector
# from executor import SmartInteractionExecutor
# from validators import AutomationValidator
# from performance import PerformanceProfiler
# from seo import SEOLintEngine
# from accessibility import AccessibilityAuditor
# from network import NetworkObserver
# from console import ConsoleTelemetryListener
# from downloads import SmartDownloadTracker
# from screenshots import SmartVisionCapturer
# from report import EnterpriseReportAggregator

# logger = logging.getLogger("Framework.CoreEngine")

# class EnterpriseAutomationEngine:
#     def __init__(self) -> None:
#         self.urls = SitemapParser.extract_urls(config.sitemap_url)
#         self.master_records: List[Dict[str, Any]] = []
#         self.proxy_pool = config.fetch_live_free_proxies()

#     def execute_framework(self) -> None:
#         if not self.urls:
#             logger.critical("Framework shutdown: sitemap extraction failed or 0 targets loaded.")
#             return

#         logger.info(f"Starting parallel engine sweep. Active processes: {config.max_workers}")
#         with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
#             futures = {executor.submit(self._process_url_with_retry, url): url for url in self.urls}
#             for f in as_completed(futures):
#                 res = f.result()
#                 if res: self.master_records.append(res)

#         reporter = EnterpriseReportAggregator(self.master_records, config.reports_dir)
#         reporter.generate_all()
#         logger.info("Automation workflow executed completely. System reports finalized inside artifacts/reports/ folder.")

#     def _process_url_with_retry(self, url: str) -> Dict[str, Any]:
#         # Har page ke liye retry loop control configuration
#         for attempt in range(1, config.max_retries + 1):
#             try:
#                 # Pehle attempt me proxy use karega, agar fail hua toh attempt > 1 me direct direct run chalega
#                 use_proxy = True if attempt == 1 else False
#                 return self._execute_page_lifecycle(url, use_proxy=use_proxy, attempt=attempt)
#             except Exception as e:
#                 logger.warning(f"⚠️ Exception hit on {url} (Attempt {attempt}/{config.max_retries}): {str(e)}")
#                 if attempt == config.max_retries:
#                     return {"url": url, "status": "FAILED", "page_classification": "Network Error", "failure_reason": str(e)}
#         return {}

#     def _execute_page_lifecycle(self, url: str, use_proxy: bool, attempt: int) -> Dict[str, Any]:
#         with sync_playwright() as p:
#             selected_proxy = None
            
#             if use_proxy and self.proxy_pool:
#                 proxy_url = random.choice(self.proxy_pool)
#                 selected_proxy = {"server": proxy_url}
#                 logger.info(f"🔄 Proxy Route: Opening browser window via dynamic IP proxy: {proxy_url}")
#             else:
#                 logger.info(f"⚡ High-Speed Fallback: Connecting via Direct Local Network pipe (Attempt {attempt})")

#             browser: Browser = p.chromium.launch(
#                 headless=config.headless, 
#                 slow_mo=800, 
#                 args=["--no-sandbox"]
#             )
            
#             vp = config.viewports[0][1]
#             context: BrowserContext = browser.new_context(
#                 viewport={"width": vp.width, "height": vp.height}, 
#                 accept_downloads=True,
#                 proxy=selected_proxy
#             )
#             page: Page = context.new_page()

#             net_spy = NetworkObserver()
#             con_spy = ConsoleTelemetryListener()
#             page.on("response", net_spy.handle_response)
#             page.on("console", con_spy.handle_message)

#             try:
#                 # Navigate layout view
#                 page.goto(url, wait_until="networkidle", timeout=config.page_timeout_ms)
#                 raw_html = page.content()
                
#                 dom = PageTypeDetector.analyze_dom(raw_html)
#                 perf = PerformanceProfiler.capture_metrics(page)
#                 seo = SEOLintEngine.audit_page(raw_html)
#                 a11y = AccessibilityAuditor.run_audit(page)
                
#                 SmartVisionCapturer.capture(page, url, "initial", config.screenshots_dir)
                
#                 validator = AutomationValidator(page)
#                 initial_state = validator.capture_state_snapshot()
                
#                 executor_engine = SmartInteractionExecutor(page)
#                 actions = executor_engine.interact_with_page(dom["metrics"])
                
#                 page.wait_for_timeout(1500)
#                 SmartVisionCapturer.capture(page, url, "final", config.screenshots_dir)
                
#                 is_valid, errs, fix = validator.validate_runtime_mutations(initial_state)
                
#                 return {
#                     "url": url, "status": "PASSED" if is_valid else "FAILED", "page_classification": dom["classification"],
#                     "performance": perf, "seo": seo, "accessibility": a11y, "actions": actions, "failure_reason": " | ".join(errs)
#                 }
#             finally:
#                 context.close()
#                 browser.close()

# if __name__ == "__main__":
#     engine = EnterpriseAutomationEngine()
#     engine.execute_framework()





















# import logging
# import random
# import time
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from typing import Dict, Any, List
# from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
# from playwright_stealth import stealth  # Pure and direct safe reference import

# from config import config
# from sitemap import SitemapParser
# from detector import PageTypeDetector
# from executor import SmartInteractionExecutor
# from validators import AutomationValidator
# from performance import PerformanceProfiler
# from seo import SEOLintEngine
# from accessibility import AccessibilityAuditor
# from network import NetworkObserver
# from console import ConsoleTelemetryListener
# from downloads import SmartDownloadTracker
# from screenshots import SmartVisionCapturer
# from report import EnterpriseReportAggregator

# logger = logging.getLogger("Framework.CoreEngine")

# class EnterpriseAutomationEngine:
#     def __init__(self) -> None:
#         self.urls = SitemapParser.extract_urls(config.sitemap_url)
#         self.master_records: List[Dict[str, Any]] = []
#         self.proxy_pool = config.fetch_live_free_proxies()

#     def execute_framework(self) -> None:
#         if not self.urls:
#             logger.critical("Framework shutdown: sitemap extraction failed or 0 targets loaded.")
#             return

#         logger.info(f"Starting parallel engine sweep. Active processes: {config.max_workers}")
#         with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
#             futures = {executor.submit(self._process_url_with_retry, url): url for url in self.urls}
#             for f in as_completed(futures):
#                 res = f.result()
#                 if res: self.master_records.append(res)

#         reporter = EnterpriseReportAggregator(self.master_records, config.reports_dir)
#         reporter.generate_all()
#         logger.info("Automation workflow executed completely. System reports finalized inside artifacts/reports/ folder.")

#     def _process_url_with_retry(self, url: str) -> Dict[str, Any]:
#         for attempt in range(1, config.max_retries + 1):
#             try:
#                 return self._execute_page_lifecycle(url, attempt=attempt)
#             except Exception as e:
#                 logger.warning(f"⚠️ Exception hit on {url} (Attempt {attempt}/{config.max_retries}): {str(e)}")
#                 if attempt == config.max_retries:
#                     return {"url": url, "status": "FAILED", "page_classification": "Network Error", "failure_reason": str(e)}
#         return {}

#     def _execute_page_lifecycle(self, url: str, attempt: int) -> Dict[str, Any]:
#         with sync_playwright() as p:
#             selected_proxy = None
            
#             if self.proxy_pool:
#                 proxy_url = random.choice(self.proxy_pool)
#                 selected_proxy = {"server": proxy_url}
#                 logger.info(f"🔄 Proxy Route: Opening browser window via dynamic IP proxy: {proxy_url}")

#             browser: Browser = p.chromium.launch(
#                 headless=config.headless, 
#                 slow_mo=800, 
#                 args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
#             )
            
#             vp = config.viewports[0][1]
#             context: BrowserContext = browser.new_context(
#                 viewport={"width": vp.width, "height": vp.height}, 
#                 accept_downloads=True,
#                 proxy=selected_proxy,
#                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#             )
#             page: Page = context.new_page()

#             # --- 100% FIXED STEALTH LAYER CALL ---
#             try:
#                 stealth(page)
#                 logger.info("🕵️ Stealth Layer Enabled: Automation controlled signatures completely hidden.")
#             except Exception as stealth_err:
#                 logger.warning(f"Stealth bypass skip hook alert: {stealth_err}")

#             net_spy = NetworkObserver()
#             con_spy = ConsoleTelemetryListener()
#             page.on("response", net_spy.handle_response)
#             page.on("console", con_spy.handle_message)

#             try:
#                 # --- REFERER LINKING VIA GOOGLE ORGANIC CHANNEL ---
#                 logger.info("🎯 Injecting Organic Search Headers: Referer set to google.com")
#                 page.goto(url, wait_until="networkidle", timeout=config.page_timeout_ms, referer="https://www.google.com/")
                
#                 # --- SMART SMOOTH HUMAN READING SCROLL PATTERN ---
#                 logger.info("📜 Simulating human reading pattern: Scrolling down page...")
#                 for i in range(1, 5):
#                     page.evaluate(f"window.scrollTo({{top: {i * 200}, behavior: 'smooth'}})")
#                     page.wait_for_timeout(700)
#                 page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
#                 page.wait_for_timeout(500)

#                 raw_html = page.content()
#                 dom = PageTypeDetector.analyze_dom(raw_html)
#                 perf = PerformanceProfiler.capture_metrics(page)
#                 seo = SEOLintEngine.audit_page(raw_html)
#                 a11y = AccessibilityAuditor.run_audit(page)
                
#                 SmartVisionCapturer.capture(page, url, "initial", config.screenshots_dir)
                
#                 validator = AutomationValidator(page)
#                 initial_state = validator.capture_state_snapshot()
                
#                 executor_engine = SmartInteractionExecutor(page)
#                 actions = executor_engine.interact_with_page(dom["metrics"])
                
#                 SmartVisionCapturer.capture(page, url, "final", config.screenshots_dir)
#                 is_valid, errs, fix = validator.validate_runtime_mutations(initial_state)
                
#                 # --- LONG ENGAGEMENT DWELL RETENTION TIMEOUT HOLD (15-30s) ---
#                 hold_duration = random.randint(15, 30)
#                 logger.info(f"⏳ Dynamic Engagement Mode: Keeping session active for {hold_duration} seconds with micro-mouse movements...")
                
#                 start_time = time.time()
#                 while time.time() - start_time < hold_duration:
#                     page.mouse.move(random.randint(150, 600), random.randint(150, 600))
#                     page.wait_for_timeout(3000)
                
#                 return {
#                     "url": url, "status": "PASSED" if is_valid else "FAILED", "page_classification": dom["classification"],
#                     "performance": perf, "seo": seo, "accessibility": a11y, "actions": actions, "failure_reason": " | ".join(errs)
#                 }
#             finally:
#                 context.close()
#                 browser.close()

# if __name__ == "__main__":
#     engine = EnterpriseAutomationEngine()
#     engine.execute_framework()















import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from config import config
from sitemap import SitemapParser
from detector import PageTypeDetector
from executor import SmartInteractionExecutor
from validators import AutomationValidator
from performance import PerformanceProfiler
from seo import SEOLintEngine
from accessibility import AccessibilityAuditor
from network import NetworkObserver
from console import ConsoleTelemetryListener
from downloads import SmartDownloadTracker
from screenshots import SmartVisionCapturer
from report import EnterpriseReportAggregator

logger = logging.getLogger("Framework.CoreEngine")

class EnterpriseAutomationEngine:
    def __init__(self) -> None:
        self.urls = SitemapParser.extract_urls(config.sitemap_url)
        self.master_records: List[Dict[str, Any]] = []
        self.proxy_pool = config.fetch_live_free_proxies()

    def execute_framework(self) -> None:
        if not self.urls:
            logger.critical("Framework shutdown: sitemap extraction failed or 0 targets loaded.")
            return

        logger.info(f"Starting parallel engine sweep. Active processes: {config.max_workers}")
        with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
            futures = {executor.submit(self._process_url_with_retry, url): url for url in self.urls}
            for f in as_completed(futures):
                res = f.result()
                if res: self.master_records.append(res)

        reporter = EnterpriseReportAggregator(self.master_records, config.reports_dir)
        reporter.generate_all()
        logger.info("Automation workflow executed completely.")

    def _process_url_with_retry(self, url: str) -> Dict[str, Any]:
        for attempt in range(1, config.max_retries + 1):
            try:
                # Sirf pehle attempt me free proxy test karega. Agar fail hua toh baki 2 retries direct local premium net se chalenge!
                use_proxy = True if attempt == 1 else False
                return self._execute_page_lifecycle(url, use_proxy=use_proxy, attempt=attempt)
            except Exception as e:
                logger.warning(f"⚠️ Exception hit on {url} (Attempt {attempt}/{config.max_retries}): {str(e)}")
                if attempt == config.max_retries:
                    return {"url": url, "status": "FAILED", "page_classification": "Network Error", "failure_reason": str(e)}
        return {}

    def _execute_page_lifecycle(self, url: str, use_proxy: bool, attempt: int) -> Dict[str, Any]:
        with sync_playwright() as p:
            selected_proxy = None
            
            if use_proxy and self.proxy_pool:
                proxy_url = random.choice(self.proxy_pool)
                selected_proxy = {"server": proxy_url}
                logger.info(f"🔄 Proxy Route: Opening browser window via dynamic IP proxy: {proxy_url}")
            else:
                logger.info(f"⚡ High-Speed Fallback: Connecting via Direct Clean Local Network pipe (Attempt {attempt}/3)")

            browser: Browser = p.chromium.launch(
                headless=config.headless, 
                slow_mo=800, 
                args=[
                    "--no-sandbox", 
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars"
                ]
            )
            
            vp = config.viewports[0][1]
            context: BrowserContext = browser.new_context(
                viewport={"width": vp.width, "height": vp.height}, 
                accept_downloads=True,
                proxy=selected_proxy,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page: Page = context.new_page()

            # --- HARDCORE BUILT-IN JAVASCRIPT STEALTH INJECTION ---
            # Yeh bina kisi library ke navigator.webdriver property ko permanently uda dega
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            logger.info("🕵️ Native Internal Stealth Activated: Webdriver signatures masked completely.")

            net_spy = NetworkObserver()
            con_spy = ConsoleTelemetryListener()
            page.on("response", net_spy.handle_response)
            page.on("console", con_spy.handle_message)

            try:
                # --- REFERER LINKING VIA GOOGLE ORGANIC CHANNEL ---
                logger.info("🎯 Injecting Organic Search Headers: Referer set to google.com")
                page.goto(url, wait_until="networkidle", timeout=config.page_timeout_ms, referer="https://www.google.com/")
                
                # --- SMART SMOOTH HUMAN READING SCROLL PATTERN ---
                logger.info("📜 Simulating human reading pattern: Scrolling down page...")
                for i in range(1, 5):
                    page.evaluate(f"window.scrollTo({{top: {i * 200}, behavior: 'smooth'}})")
                    page.wait_for_timeout(700)
                page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
                page.wait_for_timeout(500)

                raw_html = page.content()
                dom = PageTypeDetector.analyze_dom(raw_html)
                perf = PerformanceProfiler.capture_metrics(page)
                seo = SEOLintEngine.audit_page(raw_html)
                a11y = AccessibilityAuditor.run_audit(page)
                
                SmartVisionCapturer.capture(page, url, "initial", config.screenshots_dir)
                
                validator = AutomationValidator(page)
                initial_state = validator.capture_state_snapshot()
                
                executor_engine = SmartInteractionExecutor(page)
                actions = executor_engine.interact_with_page(dom["metrics"])
                
                SmartVisionCapturer.capture(page, url, "final", config.screenshots_dir)
                is_valid, errs, fix = validator.validate_runtime_mutations(initial_state)
                
                # --- LONG ENGAGEMENT DWELL RETENTION TIMEOUT HOLD (15-30s) ---
                hold_duration = random.randint(15, 30)
                logger.info(f"⏳ Dynamic Engagement Mode: Keeping session active for {hold_duration} seconds with micro-mouse movements...")
                
                start_time = time.time()
                while time.time() - start_time < hold_duration:
                    page.mouse.move(random.randint(150, 600), random.randint(150, 600))
                    page.wait_for_timeout(3000)
                
                return {
                    "url": url, "status": "PASSED" if is_valid else "FAILED", "page_classification": dom["classification"],
                    "performance": perf, "seo": seo, "accessibility": a11y, "actions": actions, "failure_reason": " | ".join(errs)
                }
            finally:
                context.close()
                browser.close()

if __name__ == "__main__":
    engine = EnterpriseAutomationEngine()
    engine.execute_framework()