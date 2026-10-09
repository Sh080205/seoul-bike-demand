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
- ขอบเขต: ระบบเปิด นอกช่วงพายุที่กำหนดจากประกาศ KMA ล่วงหน้าสำหรับเขตเมืองหลวง; ระดับทั้งเมือง (ไม่ใช่รายสถานี) กฎเดียวกันทั้ง train/test
- ชนิดงาน: ตัดสินใจใช้ **regression** (`config.TASK = "regression"`) เพราะ target ของ dataset เป็นจำนวนจักรยานเชิงปริมาณ ทำนายได้ตรงๆ โดยไม่ต้องตั้ง threshold เอง

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
(`scripts/make_dataset.py` สร้าง `data/processed/*.csv` และ `01_eda` ขั้น 3 สร้าง `data/splits/*.csv` — ทั้งสองอย่าง commit ไว้แล้ว notebook จึงรันได้ทันที)

## โครงสร้าง

```
config.py            ค่าคงที่ทั้งหมด (RANDOM_STATE, path, TASK)
data/raw/            ไฟล์ CSV ต้นฉบับ
data/processed/      dataset ที่ทุก notebook ใช้ (config.DATA_CSV)
scripts/             make_dataset.py สร้าง data/processed/ จาก data/raw/
data/splits/         รายการวัน train/test
notebooks/00_setup   ตรวจ environment + กติกากลุ่ม (ขั้น 0)
notebooks/01_eda     โหลด/ตรวจข้อมูล, split ตามวัน, EDA บน train (ขั้น 2–4)
notebooks/02_modeling  นิยามปัญหา, feature engineering, Pipeline, FS, PCA, baseline, เทียบ/tune โมเดล, test (ขั้น 1, 5–13)
figures/             รูปที่ใช้ในรายงานและสไลด์
reports/             รายงาน (report.html → report.pdf)
slides/              สไลด์นำเสนอ 18 หน้า · บทพูด · ภาพรวมทีละขั้น (HTML)
```

## ผลหลัก

CV = 5-fold `GroupKFold` (group = วัน) บน train · เลือกโมเดลด้วย CV แล้วประเมิน test/sensitivity ในขั้น 13 · MAE มีหน่วยคัน/ชม.

| โมเดล (หลัง tune) | selector / จำนวนคอลัมน์ | CV MAE ± fold std |
|---|---|---|
| Baseline เวลา (hour × วันทำงาน/วันหยุด) | - | 398.4 ± 10.9 |
| Linear Regression + log1p(y) | ทุก 59 | 205.86 ± 9.97 |
| kNN + log1p(y), k=15, distance | MI 10/37 | 176.83 ± 10.39 |
| Random Forest, 300 trees | ทุก 36 | 117.77 ± 4.12 |
| **HistGradientBoosting** | **MI 36/36 (เก็บทุกคอลัมน์)** | **104.86 ± 3.96** |

- **test ในขอบเขต (1,656 ชั่วโมง / 69 วัน):** MAE **91.46** · MSE 22,219.3 · RMSE 149.06 · R² **0.938**
- **รวมวันพายุกลับมา (1,697 ชั่วโมง / 71 วัน):** MAE **95.48** · RMSE 163.91 · R² 0.925; ใช้ final_model เดิม ไม่ fit เพิ่ม วันพายุ 41 ชั่วโมงมี MAE 257.65
- ขอบเขต: ตัดระบบปิดก่อน แล้ววันที่ 2 ก.ค., 23–24 ส.ค., 5–7 ต.ค. 2018 ตามช่วงคาดการณ์ฝน/ลมบนบกในเขตเมืองหลวงจาก KMA ไม่อ้างว่าทุกวันมี formal Seoul typhoon warning หรือเป็นวันขึ้นฝั่ง วันที่ 1 ก.ค. เก็บไว้เป็นบริบทมรสุม แหล่งอ้างอิงอยู่ใน `config.STORM_EVENTS` และรายงาน
- ไฟล์วัน split เดิม 292/73 วัน; กรองแล้ว train 6,672 ชั่วโมง / 278 วัน ไม่เปลี่ยน `data/splits/`
- Sensor rules: humidity=0 → NaN; เมื่อ Magnus gap >15 จุดเปอร์เซ็นต์ และ T/Td เป็น 0 เพียงตัวเดียว แก้เฉพาะคอลัมน์นั้นเป็น NaN (สงสัยเซนเซอร์; อนุมาน) train NaN: humidity17, dew point5, temp1 เติม median ภายใน Pipeline
- `rain_prev_3h`: ฝน 3 ชั่วโมงก่อนหน้าในวันเดียวกัน ไม่รวมปัจจุบัน/ไม่ข้ามวัน; ชั่วโมงภายในวันหาย → NaN HGB paired CV ไม่มี/มี feature = 112.15 ±4.23 / 109.18 ±2.93 ดีขึ้นครบ5foldsจึงเก็บ
- Feature selection ทดลองตามแต่ละโมเดล: Linear F/MI/RFE(Ridge)/Lasso; kNN MI; RF/HGB MI/RFE(RF proxy)/SelectFromModel(RF proxy) MI10 ช่วย kNN 12.79 คัน; ชุดย่อยไม่ช่วยต้นไม้ใน default CV ส่ง selector configuration เข้า tuning และเรียนใหม่ภายใน folds HGB MI36 ยังเก็บทุกคอลัมน์
- PCA จาก 37 คอลัมน์ (hour cyclic): 14 PC ≥90%; 19 PC ≥95% kNN PCA15 ได้ MAE184.1 แต่รุ่นสุดท้ายชนะด้วย MI10
- HGB: learning_rate0.1, max_iter200, max_leaf_nodes63, min_samples_leaf5, l2_regularization1.0 · รอบสุดท้าย fit1.786s / predict5.63ms ต่อแถวบนเครื่องนี้

## ข้อจำกัด

- ฝนตกใน test ในขอบเขตมี89ชั่วโมง MAE143.0 หรือ83.2%ของยอดเฉลี่ย; rain historyช่วยCVแต่ยังไม่แก้ข้อจำกัดนี้ทั้งหมด
- วันหยุดยาวและวันที่อธิบายไม่ได้ยังเก็บไว้ ไม่ลบเพราะ residualใหญ่ กฎพายุครอบคลุมเฉพาะ6วันที่ระบุ ไม่ใช่ภัยธรรมชาติทุกชนิด
- ประเมินด้วยอากาศที่วัดจริง ยังไม่รวมความผิดพลาดของ weather forecast เมื่อใช้ล่วงหน้าต้องมีประวัติฝน/forecastสำหรับช่วงก่อนชั่วโมงนั้นและประกาศขอบเขตที่พร้อมณเวลาทำนาย
- ข้อมูล1ปี เมืองเดียว ยอดรวมทั้งเมือง; splitสุ่มวันไม่วัดการพยากรณ์ข้ามปี CVใช้เลือกconfigurationจึงอาจมี selection bias
- การขยาย search spaceด้วยselectorเปลี่ยนชุดพารามิเตอร์ที่สุ่ม จึงไม่สรุปว่าFSเพียงอย่างเดียวทำให้ tunedRF/HGBดีขึ้น foldstdไม่ใช่confidence intervalของส่วนต่าง

## เอกสารฉบับส่ง

- `reports/report.html` → `reports/report.pdf` (23หน้า): `python reports/build_pdf.py`
- `slides/seoul-bike-presentation.html` (18หน้า), `slides/seoul-bike-overview.html` (28หน้า)
- `slides/speaker-script.html`: บทพูด9:00, A3:25 / B2:25 / C3:10 และQ&Aอ้างตารางรายงานฉบับล่าสุด
- รายละเอียดการทดลองและoutputs: `notebooks/02_modeling.ipynb` ขั้น7–13; ไม่มีไฟล์โมเดลใหม่ในcommit
