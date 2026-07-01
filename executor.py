# import logging
# from typing import Dict, Any, List
# from playwright.sync_api import Page
# from test_data import SmartDataGenerator
# from runtime_asset_generator import RuntimeAssetGenerator

# logger = logging.getLogger("Framework.Executor")

# class SmartInteractionExecutor:
#     def __init__(self, page: Page) -> None:
#         self.page = page
#         self.data_gen = SmartDataGenerator()
#         self.asset_engine = RuntimeAssetGenerator()

#     def interact_with_page(self, element_metrics: Dict[str, int]) -> List[str]:
#         actions = []
#         if element_metrics["inputs_file"] > 0:
#             actions.append(self._handle_file_uploads())
#         if element_metrics["selects"] > 0:
#             actions.append(self._handle_selects())
#         if element_metrics["inputs_text"] > 0 or element_metrics["inputs_color"] > 0:
#             actions.append(self._handle_inputs())
#         if element_metrics["textareas"] > 0:
#             actions.append(self._handle_textareas())
            
#         actions.append(self._trigger_processing_buttons())
#         return [a for a in actions if a]

#     def _handle_file_uploads(self) -> str:
#         try:
#             file_inputs = self.page.locator("input[type='file']").all()
#             for inp in file_inputs:
#                 if inp.is_visible():
#                     accept = inp.get_attribute("accept") or "txt"
#                     if "png" in accept or "jpg" in accept: asset = self.asset_engine.generate_png()
#                     elif "pdf" in accept: asset = self.asset_engine.generate_pdf()
#                     elif "csv" in accept: asset = self.asset_engine.generate_csv()
#                     else: asset = self.asset_engine.generate_txt()
#                     inp.set_input_files(asset)
#             return "File Upload Interacted"
#         except Exception:
#             return ""

#     def _handle_selects(self) -> str:
#         try:
#             for dropdown in self.page.locator("select").all():
#                 if dropdown.is_visible() and dropdown.is_enabled():
#                     opts = dropdown.locator("option").all()
#                     vals = [o.get_attribute("value") for o in opts if o.get_attribute("value")]
#                     if vals: dropdown.select_option(value=vals[-1])
#             return "Dropdown Selects Manipulated"
#         except Exception: return ""

#     def _handle_inputs(self) -> str:
#         try:
#             for inp in self.page.locator("input").all():
#                 if inp.is_visible() and inp.is_enabled():
#                     itype = inp.get_attribute("type") or "text"
#                     if itype in ["hidden", "submit", "button", "file"]: continue
#                     meta = {"type": itype, "name": inp.get_attribute("name") or "", "placeholder": inp.get_attribute("placeholder") or ""}
#                     inp.fill(self.data_gen.generate_value_by_type(meta))
#             return "Input Fields Filled"
#         except Exception: return ""

#     def _handle_textareas(self) -> str:
#         try:
#             for area in self.page.locator("textarea").all():
#                 if area.is_visible() and area.is_enabled() and not area.input_value():
#                     meta = {"type": "textarea", "name": area.get_attribute("name") or "", "placeholder": area.get_attribute("placeholder") or ""}
#                     area.fill(self.data_gen.generate_value_by_type(meta))
#             return "Textareas Loaded"
#         except Exception: return ""

#     def _trigger_processing_buttons(self) -> str:
#         try:
#             selectors = ["button:has-text('Generate')", "button:has-text('Convert')", "button:has-text('Process')", "input[type='submit']", "#process-btn"]
#             for s in selectors:
#                 loc = self.page.locator(s).first
#                 if loc.count() > 0 and loc.is_visible() and loc.is_enabled():
#                     loc.click()
#                     return "Processing Button Clicked"
#             return ""
#         except Exception: return ""








import logging
from typing import Dict, Any, List
from playwright.sync_api import Page
from runtime_asset_generator import RuntimeAssetGenerator

logger = logging.getLogger("Framework.ExecutorEngine")

class SmartInteractionExecutor:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.asset_engine = RuntimeAssetGenerator()

    def interact_with_page(self, element_metrics: Dict[str, Any]) -> List[str]:
        actions = []
        
        # 1. Determine Dynamic Inferred Profile Context from markup state values
        html_src = self.page.content().lower()
        file_accepts = element_metrics.get("file_accepts", [])
        
        # 2. SMART CONTEXTUAL FILE UPLOADER 
        if element_metrics["inputs_file"] > 0:
            actions.append(self._handle_smart_uploads(file_accepts, html_src))

        # 3. SELECT OPTION HANDLERS
        if element_metrics["selects"] > 0:
            actions.append(self._handle_dropdowns())

        # 4. INLINE INPUT FORM SUBMISSIONS
        if element_metrics["inputs_text"] > 0 or element_metrics["inputs_number"] > 0:
            actions.append(self._handle_input_fields(html_src))

        # 5. MULTILINE TEXT BLOCK GENERATION ENGINE (For rich data text tools validation)
        if element_metrics["textareas"] > 0:
            actions.append(self._handle_rich_textareas(html_src))
            
        # 6. TRIGGER ACTION WORKFLOW
        actions.append(self._click_execution_triggers())
        return [a for a in actions if a]

    def _handle_smart_uploads(self, file_accepts: List[str], ctx: str) -> str:
        try:
            file_inputs = self.page.locator("input[type='file']").all()
            for inp in file_inputs:
                if not inp.is_visible():
                    continue
                
                generated_asset = None
                
                # Dynamic matching rules based on element accept types or body layout markers
                if any("video" in x for x in file_accepts) or "video" in ctx:
                    logger.info("Context Match: Video Tool detected. Generating test video assets dynamically...")
                    generated_asset = self.asset_engine.generate_mp4()
                elif any("audio" in x for x in file_accepts) or "audio" in ctx:
                    logger.info("Context Match: Audio Tool detected. Launching synthetic wave generation...")
                    generated_asset = self.asset_engine.generate_wav()
                elif any("pdf" in x for x in file_accepts) or "pdf" in ctx:
                    generated_asset = self.asset_engine.generate_pdf()
                elif any("csv" in x for x in file_accepts) or "csv" in ctx:
                    generated_asset = self.asset_engine.generate_csv()
                elif any(img in "".join(file_accepts) for img in ["png", "jpg", "jpeg", "webp"]):
                    generated_asset = self.asset_engine.generate_png()
                else:
                    # Generic fallback asset dump
                    generated_asset = self.asset_engine.generate_txt()

                if generated_asset:
                    inp.set_input_files(generated_asset)
                    logger.info(f"Successfully loaded runtime dynamic testing asset into UI frame target: {generated_asset}")
            return "Contextual File Upload Sequence Completed"
        except Exception as e:
            logger.error(f"Error handling automated media uploads profiles: {str(e)}")
            return ""

    def _handle_dropdowns(self) -> str:
        try:
            for dropdown in self.page.locator("select").all():
                if dropdown.is_visible() and dropdown.is_enabled():
                    opts = dropdown.locator("option").all()
                    vals = [o.get_attribute("value") for o in opts if o.get_attribute("value")]
                    if vals:
                        dropdown.select_option(value=vals[-1])
            return "Dropdown Manipulation Fired"
        except Exception: return ""

    def _handle_input_fields(self, ctx: str) -> str:
        try:
            for inp in self.page.locator("input").all():
                if not inp.is_visible() or not inp.is_enabled(): continue
                itype = inp.get_attribute("type") or "text"
                if itype in ["hidden", "submit", "button", "file", "checkbox", "radio"]: continue
                
                # Insert target programmatic dummy metrics numbers
                if itype == "number" or "size" in ctx or "width" in ctx or "height" in ctx:
                    inp.fill("50")
                elif "color" in itype or "hex" in ctx:
                    inp.fill("#00adb5")
                else:
                    inp.fill("Automation Test String")
            return "Input Fields Loaded"
        except Exception: return ""

    def _handle_rich_textareas(self, ctx: str) -> str:
        try:
            for area in self.page.locator("textarea").all():
                if area.is_visible() and area.is_enabled() and not area.input_value():
                    # Check what type of layout payload content data strings are needed
                    if "json" in ctx:
                        payload = self.asset_engine.generate_random_text(1)
                        payload = '{"test_suite_token": "SA_ACTIVE", "payload_data": "sample text parameters validation"}'
                    elif "markdown" in ctx or "md" in ctx:
                        payload = "# Dynamic Test Heading\n\n- Operational item verification line 1\n- Core infrastructure validation block 2"
                    else:
                        # Feed massive multiline paragraph data blocks for comprehensive text processing analysis
                        payload = self.asset_engine.generate_random_text(paragraph_count=4)
                        
                    area.fill(payload)
            return "Deep Textarea Multiline Blocks Injected"
        except Exception: return ""

    def _click_execution_triggers(self) -> str:
        try:
            selectors = [
                "button:has-text('Generate')", "button:has-text('Convert')", "button:has-text('Process')",
                "button:has-text('Compress')", "button:has-text('Upload')", "button:has-text('Run')",
                "input[type='submit']", "#process-btn", ".action-btn"
            ]
            for s in selectors:
                loc = self.page.locator(s).first
                if loc.count() > 0 and loc.is_visible() and loc.is_enabled():
                    loc.click()
                    return f"Action Transmutation Button Fired -> ({s})"
            return ""
        except Exception: return ""