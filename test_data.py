import json
import uuid
import base64
from typing import Dict, Any
from faker import Faker

class SmartDataGenerator:
    def __init__(self) -> None:
        self.fake = Faker()

    def get_text(self) -> str: return self.fake.word()
    def get_paragraph(self) -> str: return self.fake.paragraph()
    def get_email(self) -> str: return self.fake.email()
    def get_password(self) -> str: return self.fake.password(length=12)
    def get_url(self) -> str: return self.fake.url()
    def get_phone(self) -> str: return self.fake.phone_number()
    def get_address(self) -> str: return self.fake.address().replace("\n", ", ")
    def get_name(self) -> str: return self.fake.name()
    def get_number(self) -> str: return str(self.fake.random_int(min=1, max=5000))
    def get_date(self) -> str: return self.fake.date()
    def get_time(self) -> str: return self.fake.time()
    def get_color_hex(self) -> str: return self.fake.hex_color()

    def generate_value_by_type(self, element_meta: Dict[str, Any]) -> str:
        itype = element_meta.get("type", "text").lower()
        name = element_meta.get("name", "").lower()
        placeholder = element_meta.get("placeholder", "").lower()
        ctx = f"{name} {placeholder}"
        
        if itype == "email" or "email" in ctx: return self.get_email()
        if itype == "password" or "pass" in ctx: return self.get_password()
        if itype == "url" or "url" in ctx or "link" in ctx: return self.get_url()
        if itype == "tel" or "phone" in ctx: return self.get_phone()
        if itype == "number" or "count" in ctx: return self.get_number()
        if itype == "date" in ctx: return self.get_date()
        if itype == "color" or "hex" in ctx: return self.get_color_hex()
        if "json" in ctx: return json.dumps({"active": True, "node_id": str(uuid.uuid4())})
        
        return self.get_text()