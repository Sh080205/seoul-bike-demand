"""แบ่ง train/test ตาม "วัน" → data/splits/{train,test}_dates.csv

รัน: python scripts/make_split.py
⚠️ ไฟล์นี้ต้องมี logic เหมือนกับ bike-trash-apps/scripts/make_bike_split.py ทุกบรรทัด
   (คัดลอกไฟล์ ไม่ import ข้าม repo) เพื่อให้ได้รายการวัน test ตรงกัน
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402


def main():
    # TODO 1: โหลด config.RAW_CSV (ใช้ encoding ที่ตรวจแล้ว) และ parse คอลัมน์วันที่
    # TODO 2: GroupShuffleSplit(n_splits=1, test_size=config.TEST_FRAC,
    #         random_state=config.RANDOM_STATE) โดย groups = วันที่
    #   ⚠️ ห้ามสุ่มทีละแถว — ชั่วโมงติดกันคล้ายกันมาก ผลจะดูดีเกินจริง
    #   ⚠️ เรียงข้อมูลตามวันที่ก่อน split เพื่อให้ผลเหมือนกันทุกเครื่อง/ทุก repo
    # TODO 3: บันทึกรายการวัน (เรียงแล้ว, รูปแบบ ISO yyyy-mm-dd) ลง
    #         config.TRAIN_DATES / config.TEST_DATES
    # TODO 4: พิมพ์จำนวนวัน + จำนวนแถว train/test
    #         และ assert ว่าไม่มีวันไหนอยู่ทั้งสองฝั่ง
    raise NotImplementedError("TODO: make_split.py")


if __name__ == "__main__":
    main()
