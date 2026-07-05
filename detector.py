# from typing import Dict, Any
# from bs4 import BeautifulSoup

# class PageTypeDetector:
#     @staticmethod
#     def analyze_dom(html_content: str) -> Dict[str, Any]:
#         soup = BeautifulSoup(html_content, "lxml")
#         metrics = {
#             "textareas": len(soup.find_all("textarea")),
#             "inputs_text": len(soup.find_all("input", type=lambda t: t in [None, "text", "search"])),
#             "inputs_file": len(soup.find_all("input", type="file")),
#             "inputs_number": len(soup.find_all("input", type="number")),
#             "inputs_color": len(soup.find_all("input", type="color")),
#             "selects": len(soup.find_all("select")),
#             "checkboxes": len(soup.find_all("input", type="checkbox")),
#             "radios": len(soup.find_all("input", type="radio")),
#             "canvases": len(soup.find_all("canvas")),
#             "videos": len(soup.find_all("video")),
#             "audios": len(soup.find_all("audio")),
#             "tables": len(soup.find_all("table")),
#             "svgs": len(soup.find_all("svg")),
#             "iframes": len(soup.find_all("iframe")),
#             "contenteditables": len(soup.find_all(attrs={"contenteditable": True})),
#             "dropzones": len(soup.select("[class*='dropzone'], [id*='dropzone']"))
#         }
        
#         text = soup.body.text.lower() if soup.body else ""
#         classification = "Developer Tool"
        
#         if metrics["canvases"] > 0:
#             classification = "Color Tool" if "color" in text else "Image Tool"
#         elif metrics["inputs_file"] > 0:
#             classification = "Converter" if "convert" in text else "PDF Tool"
#         elif metrics["textareas"] >= 2:
#             classification = "JSON Tool" if "json" in text else "Text Tool"
#         elif metrics["tables"] > 0 and metrics["inputs_text"] == 0:
#             classification = "Static Category Page"
            
#         return {"classification": classification, "metrics": metrics}







# from typing import Dict, Any
# from bs4 import BeautifulSoup

# class PageTypeDetector:
#     @staticmethod
#     def analyze_dom(html_content: str) -> Dict[str, Any]:
#         soup = BeautifulSoup(html_content, "lxml")
        
#         # Pull structural accept values directly from document markup elements
#         file_inputs = soup.find_all("input", type="file")
#         file_accept_types = []
#         for inp in file_inputs:
#             accept = inp.get_attribute_list("accept")
#             if accept and accept[0]:
#                 file_accept_types.extend([a.strip().lower() for a in accept[0].split(",")])

#         metrics = {
#             "textareas": len(soup.find_all("textarea")),
#             "inputs_text": len(soup.find_all("input", type=lambda t: t in [None, "text", "search"])),
#             "inputs_file": len(file_inputs),
#             "inputs_number": len(soup.find_all("input", type="number")),
#             "inputs_color": len(soup.find_all("input", type="color")),
#             "selects": len(soup.find_all("select")),
#             "canvases": len(soup.find_all("canvas")),
#             "videos": len(soup.find_all("video")),
#             "tables": len(soup.find_all("table")),
#             "file_accepts": file_accept_types
#         }
        
#         body_text = soup.body.text.lower() if soup.body else ""
        
#         # Polymorphic Classifier Logic Block mapping functional domain areas
#         classification = "Developer Tool"
        
#         # 1. VIDEO / AUDIO MEDIA CHECK
#         if any(x in ["video/*", ".mp4", ".avi", ".webm", ".mov"] for x in file_accept_types) or "video" in body_text:
#             classification = "Video Tool"
#         elif any(x in ["audio/*", ".mp3", ".wav", ".ogg"] for x in file_accept_types) or "audio" in body_text:
#             classification = "Audio Tool"
            
#         # 2. IMAGE GRAPHICS UTILITIES
#         elif metrics["canvases"] > 0 or any(x in ["image/*", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"] for x in file_accept_types):
#             if "color" in body_text or "palette" in body_text:
#                 classification = "Color Tool"
#             else:
#                 classification = "Image Tool"
                
#         # 3. PDF VALIDATION MATRIX
#         elif any(x in [".pdf", "application/pdf"] for x in file_accept_types) or "pdf" in body_text:
#             classification = "PDF Tool"
            
#         # 4. TEXT PROCESSING UTILITIES
#         elif metrics["textareas"] >= 1:
#             if "json" in body_text: classification = "JSON Tool"
#             elif "xml" in body_text: classification = "XML Tool"
#             elif "csv" in body_text: classification = "CSV Tool"
#             elif "convert" in body_text or "case" in body_text or "slug" in body_text or "text" in body_text:
#                 classification = "Text Tool"
                
#         # 5. MATHEMATICAL FORM ACTIONS
#         elif metrics["inputs_number"] > 0 and ("calculate" in body_text or "math" in body_text):
#             classification = "Calculator"

#         return {"classification": classification, "metrics": metrics}














from typing import Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging

logger = logging.getLogger("Framework.PageTypeDetector")

class PageTypeDetector:
    @staticmethod
    def analyze_dom(html_content: str, url: str = "") -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, "lxml")
        
        # Pull structural accept values directly from document markup elements
        file_inputs = soup.find_all("input", type="file")
        file_accept_types = []
        for inp in file_inputs:
            accept = inp.get_attribute_list("accept")
            if accept and accept[0]:
                file_accept_types.extend([a.strip().lower() for a in accept[0].split(",")])

        metrics = {
            "textareas": len(soup.find_all("textarea")),
            "inputs_text": len(soup.find_all("input", type=lambda t: t in [None, "text", "search"])),
            "inputs_file": len(file_inputs),
            "inputs_number": len(soup.find_all("input", type="number")),
            "inputs_color": len(soup.find_all("input", type="color")),
            "selects": len(soup.find_all("select")),
            "canvases": len(soup.find_all("canvas")),
            "videos": len(soup.find_all("video")),
            "tables": len(soup.find_all("table")),
            "file_accepts": file_accept_types
        }
        
        body_text = soup.body.text.lower() if soup.body else ""
        url_path = urlparse(url).path.lower() if url else ""
        
        # --- ULTIMATE DYNAMIC CLASSIFIER BLOCK ---
        # 1. First Priority: Strict URL Structure Check (No False Positives)
        if url_path == "/" or url_path == "":
            classification = "Homepage"
        elif "/tools/category/" in url_path:
            cat = url_path.split("/tools/category/")[-1].strip("/")
            classification = f"Category ({cat.upper()})"
        elif url_path in ["/pricing", "/about", "/contact", "/faq", "/terms-conditions", "/privacy-policy", "/features", "/documentation", "/blog"]:
            classification = f"{url_path.strip('/').replace('-', ' ').title()} Page"
        elif url_path == "/tools":
            classification = "Tools Directory"
            
        # 2. Second Priority: Direct Tool-Slug Mapping (For Absolute Accuracy)
        elif "/tools/tool/" in url_path:
            tool_slug = url_path.split("/tools/tool/")[-1].strip("/")
            if any(k in tool_slug for k in ["image", "svg", "favicon", "background", "profile-pic", "picker", "color"]):
                classification = "Image Tool"
            elif any(k in tool_slug for k in ["video", "mp4", "thumbnail", "gif"]):
                classification = "Video Tool"
            elif any(k in tool_slug for k in ["json", "xml", "csv", "regex", "jwt", "base64", "url-encode", "hash", "ssl"]):
                classification = "Developer Tool"
            elif any(k in tool_slug for k in ["text", "word", "lorem", "case", "diff", "extractor"]):
                classification = "Text Tool"
            elif any(k in tool_slug for k in ["encryptor", "password"]):
                classification = "Security Tool"
            elif any(k in tool_slug for k in ["converter", "calculator", "percentage", "age", "time"]):
                classification = "Calculation Tool"
            else:
                classification = "Utility Tool"
                
        # 3. Third Priority: DOM-Based Fallback (If URL is not provided)
        else:
            if any(x in ["video/*", ".mp4", ".avi", ".webm", ".mov"] for x in file_accept_types):
                classification = "Video Tool"
            elif any(x in ["audio/*", ".mp3", ".wav", ".ogg"] for x in file_accept_types):
                classification = "Audio Tool"
            elif metrics["canvases"] > 0 or any(x in ["image/*", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"] for x in file_accept_types):
                classification = "Color Tool" if "color" in body_text else "Image Tool"
            elif any(x in [".pdf", "application/pdf"] for x in file_accept_types):
                classification = "PDF Tool"
            elif metrics["textareas"] >= 1:
                if "json" in body_text: classification = "JSON Tool"
                elif "xml" in body_text: classification = "XML Tool"
                elif "csv" in body_text: classification = "CSV Tool"
                else: classification = "Text Tool"
            elif metrics["inputs_number"] > 0 and "calculate" in body_text:
                classification = "Calculator"
            else:
                classification = "Developer Tool"

        return {"classification": classification, "metrics": metrics}