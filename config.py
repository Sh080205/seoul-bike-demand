"""ค่าคงที่ของโปรเจกต์ — ทุกไฟล์ import จากที่นี่ ห้าม hard-code ซ้ำ"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ---- reproducibility ----
RANDOM_STATE = 42          # ใช้ทุกจุดที่มีการสุ่ม (split, CV, model)
TEST_FRAC = 0.2            # สัดส่วน "วัน" ที่เป็น test (ไม่ใช่สัดส่วนแถว)

# ---- ชนิดงาน: รอยืนยันจากอาจารย์ ----
TASK = "classification"    # หรือ "regression"

# ---- paths ----
DATA_DIR = ROOT / "data"
RAW_CSV = DATA_DIR / "raw" / "SeoulBikeData.csv"
SPLIT_DIR = DATA_DIR / "splits"
TRAIN_DATES = SPLIT_DIR / "train_dates.csv"
TEST_DATES = SPLIT_DIR / "test_dates.csv"
FIGURES_DIR = ROOT / "figures"
REPORTS_DIR = ROOT / "reports"

# ---- dataset ----
UCI_ID = 560
DATE_COL = "Date"
TARGET_COL = "Rented Bike Count"
# TODO: ยืนยันหลังดาวน์โหลดจริง — ไฟล์ต้นฉบับจาก UCI ตรวจพบว่าไม่ใช่ UTF-8
#       (° เป็น byte 0xB0 → Latin-1/cp1252) และวันที่เป็นรูปแบบ dd/mm/yyyy
RAW_ENCODING = None        # TODO: ใส่ encoding ที่ตรวจแล้วว่าอ่านถูก
DATE_FORMAT = None         # TODO: ใส่รูปแบบวันที่ที่ตรวจแล้ว เช่น "%d/%m/%Y"
