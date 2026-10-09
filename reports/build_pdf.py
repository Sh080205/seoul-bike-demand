"""สร้าง reports/report.pdf จาก reports/report.html ด้วย Edge/Chrome แบบ headless

รัน: python reports/build_pdf.py
ใช้ browser แทน reportlab เพราะ browser วางสระ/วรรณยุกต์ภาษาไทยได้ถูกต้อง
ฟอนต์ Leelawadee UI มากับ Windows 10/11 ทุกเครื่อง
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE / "report.html"
PDF = HERE / "report.pdf"

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium",
]


def find_browser():
    for c in CANDIDATES:
        if Path(c).exists():
            return c
        if shutil.which(c):
            return shutil.which(c)
    sys.exit("ไม่เจอ Edge หรือ Chrome — ติดตั้งอย่างใดอย่างหนึ่งก่อน")


def main():
    # โปรไฟล์แยกช่วยให้ process รอจนเขียนไฟล์จบ ไม่ส่งงานให้ Edge ที่ผู้ใช้เปิดอยู่
    with tempfile.TemporaryDirectory(prefix="seoul-bike-pdf-") as temp_dir:
        temporary_pdf = Path(temp_dir) / "report.pdf"
        subprocess.run([
            find_browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={Path(temp_dir) / 'profile'}",
            f"--print-to-pdf={temporary_pdf}", HTML.as_uri(),
        ], check=True, capture_output=True, timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
        data = temporary_pdf.read_bytes()
        if not data.startswith(b"%PDF-") or not data.rstrip().endswith(b"%%EOF"):
            raise RuntimeError("browser ยังไม่ได้สร้าง PDF ที่สมบูรณ์")
        PDF.write_bytes(data)
    print(f"สร้าง {PDF.relative_to(HERE.parent)} ({PDF.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
