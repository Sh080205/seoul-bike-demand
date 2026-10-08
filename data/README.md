# Data

| รายการ | ค่า |
|---|---|
| แหล่งที่มา | UCI ML Repository id 560 — https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand |
| License | CC BY 4.0 |
| วันที่ดาวน์โหลด | 2026-09-24 (commit "Add Dataset") |
| วิธีดาวน์โหลด | zip จากหน้า UCI → `raw/seoul+bike+sharing+demand.zip` แตกเป็น `raw/seoul+bike+sharing+demand/SeoulBikeData.csv` |
| Encoding ของไฟล์ต้นฉบับ | `cp1252` (`°` = byte 0xB0, อ่านด้วย UTF-8 ไม่ได้) — ตรวจใน `notebooks/01_eda.ipynb` ขั้น 2.1 |
| รูปแบบวันที่ | `dd/mm/yyyy` (`%d/%m/%Y`) |
| จำนวนแถว / คอลัมน์ | 8,760 × 14 · ไฟล์ดิบไม่มี missing · ไม่มีแถวซ้ำ |
| ช่วงวันที่ / จำนวนวัน | 2017-12-01 ถึง 2018-11-30 · 365 วัน × 24 ชม. ครบทุกวัน |
| ชั่วโมงที่ระบบปิด (`Functioning Day = No`) | 295 แถว (12 วันเต็ม + 7 ชม. ของ 2018-10-06) ยอดเช่า = 0 ทุกแถว |
| split | `GroupShuffleSplit` ตามวัน (test_size=0.2, random_state=42) · train **292 วัน / 7,008 แถว** · test **73 วัน / 1,752 แถว** · ชั่วโมงระบบปิด: train 240, test 55 |

## ไฟล์

- `raw/seoul+bike+sharing+demand/SeoulBikeData.csv` — ไฟล์ต้นฉบับ (แตกจาก zip ของ UCI)
- `splits/train_dates.csv`, `splits/test_dates.csv` — รายการวัน (สร้างโดย `notebooks/01_eda.ipynb` ขั้น 3)
- `processed/SeoulBikeData_humidity0_to_nan.csv` — ไฟล์ดิบที่ลบความชื้น 0% (outlier จากเซนเซอร์ 17 ช่อง) ให้ว่าง → โหลดแล้วเป็น missing value (NaN) · สร้างโดย `notebooks/01_eda.ipynb` ขั้น 4.11 · `02_modeling` ใช้ไฟล์นี้
