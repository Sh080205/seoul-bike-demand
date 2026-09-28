"""สร้าง reports/report.pdf จาก reports/report.html ด้วย Edge/Chrome แบบ headless

รัน: python reports/build_pdf.py
ใช้ browser แทน reportlab เพราะ browser วางสระ/วรรณยุกต์ภาษาไทยได้ถูกต้อง
ฟอนต์ Leelawadee UI มากับ Windows 10/11 ทุกเครื่อง
"""
import shutil
import subprocess
import sys
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
    subprocess.run([
        find_browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={PDF}", HTML.as_uri(),
    ], check=True, capture_output=True)
    print(f"สร้าง {PDF.relative_to(HERE.parent)} ({PDF.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
