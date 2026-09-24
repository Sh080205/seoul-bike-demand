"""โหลดข้อมูลดิบและ split — ไม่แปลง/ไม่ทำ feature engineering ใดๆ ที่นี่"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402


def load_raw():
    """คืน DataFrame ดิบจาก config.RAW_CSV

    TODO: อ่านด้วย config.RAW_ENCODING และ parse วันที่ด้วย config.DATE_FORMAT
    ⚠️ ห้ามแก้ค่า/ลบแถวที่นี่ (เช่น Functioning Day = No) — ตัดสินใจใน notebook จาก train
    """
    raise NotImplementedError


def load_split():
    """คืน X_train, X_test, y_train, y_test ตามรายการวันใน data/splits/

    TODO: join แถวกับ train_dates / test_dates
    ⚠️ y = config.TARGET_COL ดิบ (การทำ high_demand label ทำใน notebook เพราะ
       threshold ต้องคำนวณจาก y_train เท่านั้น)
    ⚠️ เก็บคอลัมน์วันที่ไว้ใน X (หรือคืนแยก) เพื่อใช้เป็น groups ใน GroupKFold
       แต่ต้องไม่ถูกใช้เป็น feature ตรงๆ
    """
    raise NotImplementedError
