# Seoul Bike Demand

> วิชา: **Machine Learning** · กำหนดส่ง **9 ต.ค. 2569**

## สมาชิก (เรียงตามรหัสนิสิต)

| รหัสนิสิต | ชื่อ-นามสกุล |
|---|---|
| TODO | TODO |
| TODO | TODO |
| TODO | TODO |

## ปัญหา

**Regression** — ทำนาย **จำนวนจักรยานที่ถูกเช่าในชั่วโมงนั้น (คัน/ชั่วโมง)** ของทั้งระบบ Seoul Bike
จากสภาพอากาศและเวลา (ข้อมูลที่รู้ล่วงหน้าได้จากพยากรณ์อากาศ + ปฏิทิน)

- ประโยชน์: ผู้ให้บริการวางแผนจำนวนจักรยานที่ต้องพร้อมใช้ และจัดคนกระจายจักรยานล่วงหน้าในชั่วโมงที่ความต้องการสูง
- เมตริกหลัก: **MAE** (คัน/ชม.) · รอง: RMSE, R² — เหตุผลใน `notebooks/02_modeling.ipynb` ขั้น 1
- ขอบเขต: เฉพาะชั่วโมงที่ระบบเปิดให้บริการ, ระดับทั้งเมือง (ไม่ใช่รายสถานี)
- ⚠️ ยังรอยืนยันจากอาจารย์ว่าใช้ regression ได้ (`config.TASK`)

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
jupyter notebook notebooks/
```

รัน notebook ตามลำดับ `00_setup` → `01_eda` → `02_modeling`
(`01_eda` ขั้น 3 สร้าง `data/splits/*.csv` — ไฟล์นี้ commit ไว้แล้ว `02_modeling` จึงรันได้ทันที)

## โครงสร้าง

```
config.py            ค่าคงที่ทั้งหมด (RANDOM_STATE, path, TASK)
data/raw/            ไฟล์ CSV ต้นฉบับ
data/splits/         รายการวัน train/test
scripts/             (stub — งานจริงทำใน notebook)
src/data.py          (stub — ยังไม่ใช้ notebook โหลดข้อมูลเอง)
notebooks/00_setup   ตรวจ environment + กติกากลุ่ม (ขั้น 0)
notebooks/01_eda     โหลด/ตรวจข้อมูล, split ตามวัน, EDA บน train (ขั้น 2–4)
notebooks/02_modeling  นิยามปัญหา, feature engineering, Pipeline, (ต่อ) FS, PCA, เทียบโมเดล
figures/             รูปที่ใช้ในรายงาน
reports/             รายงาน + สไลด์
```

## ผลหลัก

TODO: ตารางเทียบโมเดล (CV บน train + test ครั้งเดียว), feature ที่เลือก, ผล PCA, ตาราง resource

## ข้อจำกัด

TODO
