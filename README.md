# Seoul Bike Demand

> วิชา: **Machine Learning** · กำหนดส่ง **9 ต.ค. 2569**

## สมาชิก (เรียงตามรหัสนิสิต)

| รหัสนิสิต | ชื่อ-นามสกุล |
|---|---|
| 6330300160 | นาย ชญานิน ตลับเงิน |
| 6730300591 | นาย ศุภวิชญ์ ไชยานุศักดิ์ |
| 6730300850 | นาย พัฒนเดช มะหิเมือง |

## ปัญหา

**Regression** — ทำนาย **จำนวนจักรยานที่ถูกเช่าในชั่วโมงนั้น (คัน/ชั่วโมง)** ของทั้งระบบ Seoul Bike
จากสภาพอากาศและเวลา (ข้อมูลที่รู้ล่วงหน้าได้จากพยากรณ์อากาศ + ปฏิทิน)

- ประโยชน์: ผู้ให้บริการวางแผนจำนวนจักรยานที่ต้องพร้อมใช้ และจัดคนกระจายจักรยานล่วงหน้าในชั่วโมงที่ความต้องการสูง
- เมตริกหลัก: **MAE** (คัน/ชม.) · รอง: MSE, RMSE, R² — เหตุผลใน `notebooks/02_modeling.ipynb` ขั้น 1
- ขอบเขต: เฉพาะชั่วโมงที่ระบบเปิดให้บริการ, ระดับทั้งเมือง (ไม่ใช่รายสถานี)
- ชนิดงาน: ตัดสินใจใช้ **regression** (`config.TASK = "regression"`) เพราะ target ของ dataset เป็นจำนวนนับต่อเนื่อง ทำนายได้ตรงๆ โดยไม่ต้องตั้ง threshold เอง

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
notebooks/00_setup   ตรวจ environment + กติกากลุ่ม (ขั้น 0)
notebooks/01_eda     โหลด/ตรวจข้อมูล, split ตามวัน, EDA บน train (ขั้น 2–4)
notebooks/02_modeling  นิยามปัญหา, feature engineering, Pipeline, FS, PCA, baseline, เทียบ/tune โมเดล, test (ขั้น 1, 5–13)
figures/             รูปที่ใช้ในรายงานและสไลด์
reports/             รายงาน (report.html → report.pdf)
slides/              สไลด์นำเสนอ 18 หน้า · บทพูด · ภาพรวมทีละขั้น (HTML)
```

## ผลหลัก

CV = 5-fold `GroupKFold` (group = วัน) บน train · test ประเมินครั้งเดียวหลังเลือกโมเดล · หน่วย MAE = คัน/ชม.

| โมเดล (หลัง tune) | CV MAE |
|---|---|
| Baseline: เวลาอย่างเดียว (hour × วันทำงาน/วันหยุด) | 401.0 |
| Linear Regression + log1p(y) | 211.0 ± 6.9 |
| kNN (k=5, distance, PCA 15) | 183.7 ± 7.8 |
| Random Forest | 121.8 ± 9.1 |
| **HistGradientBoosting** ✅ | **109.0 ± 8.1** |

- **test (HistGradientBoosting):** MAE **97.4** · MSE 28,947.7 · RMSE 170.1 · R² **0.919** (MSE รายงานตามเกณฑ์โจทย์ แต่อธิบายผลด้วย RMSE เพราะหน่วยเป็นคัน/ชม.)
- Feature selection (f_regression, mutual_info, RFE, Lasso): ไม่มีวิธีไหนลด MAE เกิน noise → ใช้ทุก feature · RFE ใช้ 30/58 feature ได้ MAE เท่าเดิม
- PCA: 14 PC อธิบาย variance 90% · ช่วย kNN เล็กน้อย ไม่ช่วย Linear
- รายละเอียดและตาราง resource (CLO4): `notebooks/02_modeling.ipynb` ขั้น 7–13

## ข้อจำกัด

- **ชั่วโมงที่ฝนตก** ทายคลาดมาก (MAE ≈ 89% ของยอดเฉลี่ย ใน test) — ชั่วโมงฝนตกมีแค่ ~6% ของ train
- **เหตุการณ์พิเศษที่ไม่มีใน feature** เช่น พายุไต้ฝุ่น Soulik (23 ส.ค. 2018), เทศกาลชูซอก → error ก้อนใหญ่ที่สุดใน test
- ความคลาดเป็นคันโตตามระดับยอด (พีคเย็นคลาดมากสุด) และโดยรวมทายสูงกว่าจริงเล็กน้อย (bias บวก)
- ข้อมูลมีแค่ 1 ปี และเป็นยอดรวมทั้งเมือง (ไม่ใช่รายสถานี) · ใช้ได้เฉพาะชั่วโมงที่ระบบเปิดให้บริการ
- split แบบสุ่มวัน (ไม่ใช่ตัดตามเวลา) → วัดความสามารถ "อากาศ + เวลา → ยอดเช่า" ไม่ใช่การพยากรณ์อนาคตล่วงหน้าหลายเดือน
