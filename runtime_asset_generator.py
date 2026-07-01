import os
import io
import json
import uuid
import math
import random
import mimetypes
import hashlib
import zipfile
import logging
import struct
import wave
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import cv2
from PIL import Image, ImageDraw

logger = logging.getLogger("Framework.RuntimeAssetGenerator")

@dataclass(frozen=True)
class AssetMetadata:
    filename: str
    extension: str
    mime_type: str
    file_size_bytes: int
    checksum_sha256: str
    created_at: str
    dimensions: Optional[Tuple[int, int]] = None
    duration_seconds: Optional[float] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)

class AssetGenerationError(Exception):
    """Custom exception raised when an asset fails runtime synthesis or structural validation."""
    pass

class RuntimeAssetGenerator:
    def __init__(self, base_artifacts_dir: str = "artifacts") -> None:
        self.base_dir = base_artifacts_dir
        self.dirs = {
            "images": os.path.join(self.base_dir, "images"),
            "videos": os.path.join(self.base_dir, "videos"),
            "audio": os.path.join(self.base_dir, "audio"),
            "documents": os.path.join(self.base_dir, "documents"),
            "office": os.path.join(self.base_dir, "office"),
            "data": os.path.join(self.base_dir, "data"),
            "archives": os.path.join(self.base_dir, "archives")
        }
        self._initialize_directories()
        random.seed(datetime.now(timezone.utc).timestamp())

    def _initialize_directories(self) -> None:
        for name, path in self.dirs.items():
            os.makedirs(path, exist_ok=True)

    def generate_random_filename(self, ext: str) -> str:
        return f"synthetic_{uuid.uuid4().hex[:8]}_{int(datetime.now(timezone.utc).timestamp())}.{ext.lower().lstrip('.')}"

    def generate_random_color(self, include_alpha: bool = False) -> Tuple[int, ...]:
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return rgb + (random.randint(0, 255),) if include_alpha else rgb

    def generate_random_text(self, paragraph_count: int = 1) -> str:
        words = ["automation", "playwright", "runtime", "synthetic", "verification", "element", "locator", "payload", "validation", "modular", "architecture"]
        paragraphs = []
        for _ in range(paragraph_count):
            sentence = " ".join(random.choices(words, k=random.randint(6, 12))).capitalize() + "."
            paragraphs.append(sentence)
        return "\n\n".join(paragraphs)

    def validate_asset(self, file_path: str, expected_ext: str, category: str) -> AssetMetadata:
        if not os.path.exists(file_path):
            raise AssetGenerationError(f"Path does not exist: {file_path}")
        size = os.path.getsize(file_path)
        if size == 0:
            raise AssetGenerationError(f"Zero-byte file payload: {file_path}")
        
        _, actual_ext = os.path.splitext(file_path)
        actual_ext = actual_ext.lower().lstrip(".")
        
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        checksum = sha256_hash.hexdigest()
        
        mime, _ = mimetypes.guess_type(file_path)
        inferred_mime = mime or f"application/x-{actual_ext}"
        
        logger.info(f"Asset Validated: {os.path.basename(file_path)}")
        return AssetMetadata(
            filename=os.path.basename(file_path), extension=actual_ext, mime_type=inferred_mime,
            file_size_bytes=size, checksum_sha256=checksum, created_at=datetime.now(timezone.utc).isoformat()
        )

    def generate_image(self, ext: str, width: int = 400, height: int = 400, style: str = "solid") -> str:
        out_name = self.generate_random_filename(ext)
        target_path = os.path.join(self.dirs["images"], out_name)
        color = (30, 41, 59)
        
        if style == "noise":
            noise_matrix = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
            img = Image.fromarray(noise_matrix, "RGB")
        else:
            img = Image.new("RGB", (width, height), color)
            
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), f"EaseMyTools Test: {ext.upper()}", fill=(255, 255, 255))
        img.save(target_path)
        self.validate_asset(target_path, ext, "image")
        return target_path

    def generate_png(self) -> str: return self.generate_image("png")
    def generate_jpg(self) -> str: return self.generate_image("jpg")
    def generate_jpeg(self) -> str: return self.generate_image("jpeg")
    def generate_webp(self) -> str: return self.generate_image("webp")
    def generate_bmp(self) -> str: return self.generate_image("bmp")
    def generate_tiff(self) -> str: return self.generate_image("tiff")
    def generate_gif(self) -> str: return self.generate_image("gif")
    def generate_transparent_png(self) -> str: return self.generate_image("png", style="transparent")
    def generate_gradient_image(self) -> str: return self.generate_image("png", style="gradient")
    def generate_noise_image(self) -> str: return self.generate_image("png", style="noise")
    def generate_qr_like_image(self) -> str: return self.generate_image("png", style="qr")
    def generate_random_shapes_image(self) -> str: return self.generate_image("png", style="shapes")
    def generate_thumbnail_image(self) -> str: return self.generate_image("png", 150, 150)
    def generate_very_small_image(self) -> str: return self.generate_image("png", 16, 16)
    def generate_very_large_image(self) -> str: return self.generate_image("png", 2000, 2000)
    def generate_portrait_image(self) -> str: return self.generate_image("png", 400, 600)
    def generate_landscape_image(self) -> str: return self.generate_image("png", 600, 400)
    def generate_square_image(self) -> str: return self.generate_image("png", 500, 500)
    def generate_random_resolution_image(self) -> str: return self.generate_image("png", random.choice([300, 400]), random.choice([300, 400]))

    def generate_svg_image(self) -> str:
        out_name = self.generate_random_filename("svg")
        target_path = os.path.join(self.dirs["images"], out_name)
        content = f'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="blue"/><text x="10" y="50" fill="white">SVG</text></svg>'
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return target_path

    def generate_video(self, ext: str, duration_seconds: int = 2) -> str:
        out_name = self.generate_random_filename(ext)
        target_path = os.path.join(self.dirs["videos"], out_name)
        fps = 20
        width, height = 320, 240
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(target_path, fourcc, float(fps), (width, height))
        
        for frame_idx in range(fps * duration_seconds):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            cv2.circle(frame, (int(10 + frame_idx * 5) % width, height // 2), 20, (0, 255, 0), -1)
            video_writer.write(frame)
        video_writer.release()
        return target_path

    def generate_mp4(self) -> str: return self.generate_video("mp4")
    def generate_avi(self) -> str: return self.generate_video("avi")
    def generate_webm(self) -> str: return self.generate_video("webm")
    def generate_mov(self) -> str: return self.generate_video("mov")

    def generate_audio(self, ext: str, duration_seconds: int = 2) -> str:
        out_name = self.generate_random_filename(ext)
        target_path = os.path.join(self.dirs["audio"], out_name)
        if ext.lower() == "wav":
            sample_rate = 22050
            wave_file = wave.open(target_path, "wb")
            wave_file.setnchannels(1)
            wave_file.setsampwidth(2)
            wave_file.setframerate(sample_rate)
            for i in range(int(sample_rate * duration_seconds)):
                val = int(16383.0 * math.sin(2.0 * math.pi * 440.0 * (i / sample_rate)))
                wave_file.writeframes(struct.pack("<h", val))
            wave_file.close()
        else:
            with open(target_path, "wb") as f:
                f.write(b"ID3MockAudioPayloadBytesFrameDataStream" * 50)
        return target_path

    def generate_mp3(self) -> str: return self.generate_audio("mp3")
    def generate_wav(self) -> str: return self.generate_audio("wav")
    def generate_ogg(self) -> str: return self.generate_audio("ogg")

    def generate_pdf(self) -> str:
        out_name = self.generate_random_filename("pdf")
        target_path = os.path.join(self.dirs["documents"], out_name)
        content = "%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000120 00000 n\ntrailer\n<< /Size 4 /Root 1 0 R >>\n%%EOF"
        with open(target_path, "w", encoding="ascii", errors="ignore") as f:
            f.write(content)
        return target_path

    def generate_txt(self) -> str:
        out_name = self.generate_random_filename("txt")
        target_path = os.path.join(self.dirs["documents"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(self.generate_random_text(2))
        return target_path

    def _generate_office(self, ext: str) -> str:
        out_name = self.generate_random_filename(ext)
        target_path = os.path.join(self.dirs["office"], out_name)
        with open(target_path, "wb") as f:
            f.write(b"PK\x03\x04MockOfficeContainerDocumentDataStructureBytes")
        return target_path

    def generate_docx(self) -> str: return self._generate_office("docx")
    def generate_xlsx(self) -> str: return self._generate_office("xlsx")
    def generate_pptx(self) -> str: return self._generate_office("pptx")

    def generate_csv(self) -> str:
        out_name = self.generate_random_filename("csv")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("id,key,value\n1,test_token,synthetic_payload\n")
        return target_path

    def generate_json(self) -> str:
        out_name = self.generate_random_filename("json")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump({"status": "runtime_active", "mock": True}, f)
        return target_path

    def generate_xml(self) -> str:
        out_name = self.generate_random_filename("xml")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("<root><mock status='active'/></root>")
        return target_path

    def generate_yaml(self) -> str:
        out_name = self.generate_random_filename("yaml")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("matrix:\n  environment: pipeline\n  mock: true")
        return target_path

    def generate_html(self) -> str:
        out_name = self.generate_random_filename("html")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("<html><body><h1>Automation Target</h1></body></html>")
        return target_path

    def generate_markdown(self) -> str:
        out_name = self.generate_random_filename("md")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("# Runtime Doc\n\n- Active automation pass")
        return target_path

    def generate_sql(self) -> str:
        out_name = self.generate_random_filename("sql")
        target_path = os.path.join(self.dirs["data"], out_name)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("CREATE TABLE mock (id INT); INSERT INTO mock VALUES (1);")
        return target_path

    def generate_zip(self) -> str:
        out_name = self.generate_random_filename("zip")
        target_path = os.path.join(self.dirs["archives"], out_name)
        t_path = self.generate_txt()
        with zipfile.ZipFile(target_path, "w") as zf:
            zf.write(t_path, arcname="contained_log.txt")
        return target_path