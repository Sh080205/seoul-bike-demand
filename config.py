"""ค่าคงที่ของโปรเจกต์ — ทุกไฟล์ import จากที่นี่ ห้าม hard-code ซ้ำ"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ---- reproducibility ----
RANDOM_STATE = 42          # ใช้ทุกจุดที่มีการสุ่ม (split, CV, model)
TEST_FRAC = 0.2            # สัดส่วน "วัน" ที่เป็น test (ไม่ใช่สัดส่วนแถว)

# ---- ชนิดงาน ----
TASK = "regression"        # ทำนาย rented_bike_count (คัน/ชั่วโมง) — เหตุผลใน 02_modeling ขั้น 1

# ---- paths ----
DATA_DIR = ROOT / "data"
RAW_CSV = DATA_DIR / "raw" / "seoul+bike+sharing+demand" / "SeoulBikeData.csv"   # แตกมาจาก zip ของ UCI
# ไฟล์ดิบที่ลบค่าความชื้น 0% (outlier จากเซนเซอร์ · 01_eda 4.10) ให้เป็นช่องว่าง → โหลดแล้วเป็น NaN (สร้างใน 01_eda 4.11)
PROCESSED_CSV = DATA_DIR / "processed" / "SeoulBikeData_humidity0_to_nan.csv"
SPLIT_DIR = DATA_DIR / "splits"
TRAIN_DATES = SPLIT_DIR / "train_dates.csv"
TEST_DATES = SPLIT_DIR / "test_dates.csv"
FIGURES_DIR = ROOT / "figures"
REPORTS_DIR = ROOT / "reports"

# ---- dataset ----
UCI_ID = 560
# ตรวจแล้วใน notebooks/01_eda.ipynb ขั้น 2: ไฟล์ไม่ใช่ UTF-8 (° = byte 0xB0) และวันที่เป็น dd/mm/yyyy
RAW_ENCODING = "cp1252"
DATE_FORMAT = "%d/%m/%Y"

# ชื่อคอลัมน์ดิบ → snake_case (ไม่มีหน่วย/อักขระพิเศษ) — ใช้ชื่อฝั่งขวาทุกที่หลังโหลด
COLUMN_MAP = {
    "Date": "date",
    "Rented Bike Count": "rented_bike_count",
    "Hour": "hour",
    "Temperature(°C)": "temp_c",
    "Humidity(%)": "humidity_pct",
    "Wind speed (m/s)": "wind_speed_ms",
    "Visibility (10m)": "visibility_10m",
    "Dew point temperature(°C)": "dew_point_c",
    "Solar Radiation (MJ/m2)": "solar_radiation_mj",
    "Rainfall(mm)": "rainfall_mm",
    "Snowfall (cm)": "snowfall_cm",
    "Seasons": "seasons",
    "Holiday": "holiday",
    "Functioning Day": "functioning_day",
}
DATE_COL = "date"
TARGET_COL = "rented_bike_count"
