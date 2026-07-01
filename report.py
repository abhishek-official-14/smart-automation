import json
import os
from typing import List, Dict, Any
import pandas as pd

class EnterpriseReportAggregator:
    def __init__(self, raw_data: List[Dict[str, Any]], output_dir: str) -> None:
        self.raw_data = raw_data
        self.output_dir = output_dir

    def generate_all(self) -> None:
        # JSON Report Output
        with open(os.path.join(self.output_dir, "report.json"), "w", encoding="utf-8") as f:
            json.dump(self.raw_data, f, indent=2, default=str)
            
        # CSV Structural Layout
        flattened = [{"URL": r.get("url"), "Status": r.get("status"), "Class": r.get("page_classification")} for r in self.raw_data]
        pd.DataFrame(flattened).to_csv(os.path.join(self.output_dir, "report.csv"), index=False)
        
        # HTML Verification Dashboard Layer
        rows = ""
        for item in self.raw_data:
            style = "color: green;" if item.get("status") == "PASSED" else "color: red;"
            rows += f"<tr><td>{item.get('url')}</td><td><b style='{style}'>{item.get('status')}</b></td><td>{item.get('page_classification')}</td></tr>"
            
        html = f"<html><body style='font-family:sans-serif;'><h1>Automation Report</h1><table border='1'>{rows}</table></body></html>"
        with open(os.path.join(self.output_dir, "dashboard.html"), "w", encoding="utf-8") as f:
            f.write(html)