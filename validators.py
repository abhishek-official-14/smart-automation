# from typing import Dict, Any, List, Tuple
# from playwright.sync_api import Page

# class AutomationValidator:
#     def __init__(self, page: Page) -> None:
#         self.page = page

#     def capture_state_snapshot(self) -> Dict[str, Any]:
#         try:
#             return {
#                 "textareas": [el.input_value() for el in self.page.locator("textarea").all() if el.is_visible()],
#                 "tables": self.page.locator("table").count(),
#                 "text_length": len(self.page.locator("body").inner_text() or "")
#             }
#         except Exception:
#             return {"textareas": [], "tables": 0, "text_length": 0}

#     def validate_runtime_mutations(self, initial: Dict[str, Any]) -> Tuple[bool, List[str], str]:
#         current = self.capture_state_snapshot()
#         errors = []
        
#         # UI layer content diff analysis check
#         if current["text_length"] == initial["text_length"] and current["textareas"] == initial["textareas"]:
#             errors.append("UI Mutation Failure: Content stayed static after triggering process loops.")
#             return False, errors, "Verify backend event mapping hooks or extend execution timeout frames."
#         return True, [], "Pass"










import logging
from typing import Dict, Any, List, Tuple
from playwright.sync_api import Page

logger = logging.getLogger("Framework.PolymorphicValidator")

class AutomationValidator:
    def __init__(self, page: Page) -> None:
        self.page = page

    def capture_state_snapshot(self) -> Dict[str, Any]:
        """Page ke saare media, computational, aur data views ka detailed state record karta hai."""
        try:
            # 1. Input/Textarea elements ka data
            textareas_content = [el.input_value() for el in self.page.locator("textarea").all() if el.is_visible()]
            inputs_content = [el.input_value() for el in self.page.locator("input[type='text']").all() if el.is_visible()]
            
            # 2. Files and dynamic download link updates
            download_links = [el.get_attribute("href") for el in self.page.locator("a[href*='blob:'], a[download]").all()]
            
            # 3. Dynamic layout attributes
            canvas_states = []
            canvases = self.page.locator("canvas").all()
            for c in canvases:
                if c.is_visible():
                    # Canvas ke pixels badle ya nahi checking via internal dynamic base64 signatures
                    try:
                        canvas_states.append(c.evaluate("node => node.toDataURL()"))
                    except Exception:
                        canvas_states.append("error_reading_canvas")

            # 4. Visible dynamic messages/alerts containers
            alert_boxes = [el.inner_text().strip() for el in self.page.locator(".alert, .error-msg, .success-msg, [class*='result'], [id*='result']").all() if el.is_visible()]

            return {
                "textareas": textareas_content,
                "inputs": inputs_content,
                "tables_count": self.page.locator("table").count(),
                "images_count": self.page.locator("img").count(),
                "canvas_signatures": canvas_states,
                "download_links": download_links,
                "alert_messages": alert_boxes,
                "text_length": len(self.page.locator("body").inner_text() or "")
            }
        except Exception as e:
            logger.error(f"Error while capturing dynamic UI snapshot layout: {str(e)}")
            return {
                "textareas": [], "inputs": [], "tables_count": 0, "images_count": 0,
                "canvas_signatures": [], "download_links": [], "alert_messages": [], "text_length": 0
            }

    def validate_runtime_mutations(self, initial: Dict[str, Any]) -> Tuple[bool, List[str], str]:
        """
        Polymorphic Verification Process:
        Tool ke context ke hisab se smart assertions lagata hai ki exact output mila ya nahi.
        """
        current = self.capture_state_snapshot()
        errors: List[str] = []
        suggested_remediations: List[str] = []
        
        # Track parameters changes states indicators
        mutation_detected = False

        # --- CHECKPOINT 1: IMAGE & VISUAL TOOLS VERIFICATION (Canvas/Previews) ---
        if len(initial["canvas_signatures"]) > 0 or len(current["canvas_signatures"]) > 0:
            if initial["canvas_signatures"] != current["canvas_signatures"]:
                mutation_detected = True
            else:
                errors.append("Visual Engine Failure: Canvas layout signatures remained identical. Image modification failed.")
                suggested_remediations.append("Check WebGL context allocations or check if the source image file was correctly parsed inside the canvas element container.")

        # --- CHECKPOINT 2: DATA & DYNAMIC CONVERTERS (Download Links/Blobs) ---
        if len(current["download_links"]) > len(initial["download_links"]):
            mutation_detected = True
        else:
            # Check if an existing download target URL changed its underlying reference map pointer
            if current["download_links"] != initial["download_links"]:
                mutation_detected = True

        # --- CHECKPOINT 3: TEXT & OFFICE UTILITIES (Textareas/Input Fields) ---
        if initial["textareas"] != current["textareas"] or initial["inputs"] != current["inputs"]:
            # Make sure the new values are not blank or unmodified strings
            initial_str = "".join(initial["textareas"]) + "".join(initial["inputs"])
            current_str = "".join(current["textareas"]) + "".join(current["inputs"])
            if len(current_str.strip()) > len(initial_str.strip()):
                mutation_detected = True
            else:
                errors.append("Data Generation Failure: Input text fields changed state but the output buffer remains empty.")
                suggested_remediations.append("Verify if structural formatting utility routines are dropping exceptions or silent compilation faults inside script blocks.")

        # --- CHECKPOINT 4: STRUCTURAL ELEMENTS DATA MATRIX (Tables/Dynamic Grids) ---
        if current["tables_count"] > initial["tables_count"]:
            mutation_detected = True

        # --- CHECKPOINT 5: BROAD TEXT/INNER DATA MUTATION (Universal Fallback) ---
        if not mutation_detected and current["text_length"] != initial["text_length"]:
            # Check if it was an error message or valid text variation data layout
            mutation_detected = True

        # --- FINAL CRITICAL CRASH ANALYSIS GUARD ---
        # Agar UI me error class ya text validation fatne ki warnings dikh rahi hain, toh seedhe flag fail karo
        for msg in current["alert_messages"]:
            msg_lower = msg.lower()
            if "error" in msg_lower or "failed" in msg_lower or "invalid" in msg_lower or "undefined" in msg_lower:
                errors.append(f"Application Execution Error Detected: Screen explicitly printed error payload block -> '{msg}'")
                suggested_remediations.append("Review inputs formatting specs or check edge case parameter structures in validation files.")
                return False, errors, suggested_remediations[0]

        # Final Verification Judgment Layer logic block
        if not mutation_detected and not errors:
            errors.append("UI Mutation Failure: The page layout configuration remained completely static after processing action inputs.")
            suggested_remediations.append("Ensure explicit asynchronous wait states are calibrated correctly for slow network calls or check click execution paths.")
            return False, errors, suggested_remediations[0]

        if errors:
            return False, errors, suggested_remediations[0]

        return True, [], "Verification validation pipeline confirmed successful state transformation passes."