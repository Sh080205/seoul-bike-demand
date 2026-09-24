# Seoul Bike Demand

> วิชา: **Machine Learning** · กำหนดส่ง **9 ต.ค. 2569**

## สมาชิก (เรียงตามรหัสนิสิต)

| รหัสนิสิต | ชื่อ-นามสกุล |
|---|---|
| TODO | TODO |
| TODO | TODO |
| TODO | TODO |

## ปัญหา

TODO: อธิบายปัญหาและเป้าหมาย
- ชนิดงาน **รอยืนยันจากอาจารย์** (`config.TASK`)
  - default: classification — ทำนายว่าชั่วโมงนั้นเป็น "ชั่วโมงความต้องการสูง" หรือไม่
  - ทางเลือก: regression — ทำนาย `Rented Bike Count` (คัน/ชม.)

## Dataset

- **Seoul Bike Sharing Demand** — UCI Machine Learning Repository, id 560
  https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand
- ข้อมูลรายชั่วโมง ~8,760 แถว (1 ปี), target `Rented Bike Count`
- รายละเอียด/จำนวนจริง: ดู [data/README.md](data/README.md)

### Attribution

Seoul Bike Sharing Demand [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5F62R
Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## การแบ่งข้อมูล

แบ่ง train/test **ตามวัน** (ไม่ใช่ตามแถว) — ชั่วโมงติดกันในวันเดียวกันคล้ายกันมาก
ถ้าสุ่มทีละแถว ข้อมูลวันเดียวกันจะรั่วไปทั้งสองฝั่ง ผลจะดูดีเกินจริง

## วิธีรัน

```bash
py -3.13 -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python scripts/download_data.py
python scripts/make_split.py
jupyter notebook notebooks/
```

## โครงสร้าง

```
config.py            ค่าคงที่ทั้งหมด (RANDOM_STATE, path, TASK)
data/raw/            ไฟล์ CSV ต้นฉบับ
data/splits/         รายการวัน train/test
scripts/             ดาวน์โหลด + แบ่งข้อมูล
src/data.py          ฟังก์ชันโหลดข้อมูล
notebooks/01_eda     สำรวจข้อมูล (ใช้ train เท่านั้น)
notebooks/02_modeling  feature selection, PCA, เทียบโมเดล
figures/             รูปที่ใช้ในรายงาน
reports/             รายงาน + สไลด์
```

## ผลหลัก

TODO: ตารางเทียบโมเดล (CV บน train + test ครั้งเดียว), feature ที่เลือก, ผล PCA, ตาราง resource

## ข้อจำกัด

TODO
