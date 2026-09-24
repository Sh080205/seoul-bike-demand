"""ดาวน์โหลด Seoul Bike Sharing Demand → data/raw/SeoulBikeData.csv

รัน: python scripts/download_data.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402


def main():
    # TODO 1: ลอง ucimlrepo ก่อน — fetch_ucirepo(id=config.UCI_ID)
    #   ⚠️ ตรวจว่าได้คอลัมน์ Date + target ครบ (บางเวอร์ชันแยก features/targets ให้)
    # TODO 2: ถ้าไม่ได้ → ดาวน์โหลด zip จากหน้า UCI แล้วแตกไฟล์
    #   ⚠️ ห้ามสมมติ encoding — ลองอ่านหลายแบบ (utf-8, cp1252, latin-1)
    #      แล้วเลือกแบบที่ชื่อคอลัมน์ Temperature มี "°C" ถูกต้อง
    # TODO 3: ตรวจโครงสร้างจริงก่อนบันทึก: พิมพ์ shape, ชื่อคอลัมน์, dtypes,
    #   ช่วงวันที่ + จำนวนวันที่ไม่ซ้ำ (คาด ~365), จำนวนแถวต่อวัน (คาด 24)
    #   ⚠️ รูปแบบวันที่ dd/mm/yyyy vs mm/dd/yyyy — ตรวจด้วยวันที่ > 12
    # TODO 4: บันทึกลง config.RAW_CSV แล้วอัปเดต config.RAW_ENCODING / DATE_FORMAT
    #   และกรอก data/README.md (วันที่ดาวน์โหลด, จำนวนจริง)
    raise NotImplementedError("TODO: download_data.py")


if __name__ == "__main__":
    main()
