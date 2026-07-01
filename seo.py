from typing import Dict, Any, List
from bs4 import BeautifulSoup

class SEOLintEngine:
    @staticmethod
    def audit_page(html_content: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_content, "lxml")
        errors: List[str] = []
        
        if not soup.find("title"): errors.append("Missing title element.")
        if not soup.find("meta", attrs={"name": "description"}): errors.append("Missing meta description.")
        if not soup.find("link", attrs={"rel": "canonical"}): errors.append("Missing canonical linkage anchor.")
        
        return {"score": max(0, 100 - (len(errors) * 30)), "seo_errors": errors}