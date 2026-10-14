# Seoul Bike Demand — ชุดส่งโครงงาน Machine Learning

## เปิดไฟล์ใดก่อน

1. `reports/report.pdf` — รายงานฉบับสมบูรณ์
2. `slides/seoul-bike-presentation.html` — สไลด์นำเสนอ 18 หน้า เปิด offline ด้วย Edge/Chrome
3. `notebooks/00_setup.ipynb`, `01_eda.ipynb`, `02_modeling.ipynb` — โค้ดพร้อม outputs จากการรันจริง
4. `verification/submission-audit.md` — ตารางสอบทานและหลักฐานทดสอบ

5. `bike-regression/app/app.py` — เว็บแอปทำนายจำนวนจักรยาน พร้อม `model.joblib` ที่ export จากโมเดล HGB ใน Notebook

ข้อมูล raw, processed และรายการวัน train/test **แนบครบแล้ว** ไม่ต้องดาวน์โหลดเพิ่มเพื่อรัน Notebook. แตก ZIP ก่อนรัน; ภายในมีโฟลเดอร์ `seoul-bike-demand` ชั้นเดียว.

## สมาชิก

| รหัสนิสิต | ชื่อ-นามสกุล |
|---|---|
| 6330300160 | นาย ชญานิน ตลับเงิน |
| 6730300591 | นาย ศุภวิชญ์ ไชยานุศักดิ์ |
| 6730300850 | นาย พัฒนเดช มะหิเมือง |

## โจทย์และข้อมูล

ทำนายจำนวนจักรยานที่ถูกเช่าในชั่วโมงนั้นของ Seoul Bike ทั้งเมือง จากอากาศ ปฏิทิน และฝน 3 ชั่วโมงก่อนหน้าภายในวันเดียวกัน. Target เป็นจำนวนนับไม่ติดลบ (จำนวนเต็ม); ใช้ **regression** ประมาณยอดเช่าเชิงปริมาณ. Prediction อาจเป็นทศนิยม ปัดเฉพาะตอนแสดงตัวอย่าง.

ขอบเขตหลัก: ระบบเปิดและนอกวันผลกระทบพายุจากประกาศ KMA ล่วงหน้าใน `config.py`; กฎเดียวกันทั้ง train/test. ใช้ MAE (คัน/ชม.) เป็นหลัก และรายงาน MSE, RMSE, R².

Seoul Bike Sharing Demand [Dataset]. (2020). UCI Machine Learning Repository id 560, [DOI](https://doi.org/10.24432/C5F62R), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Raw 8,760 ×14 ไม่มี missing; processed เพิ่มช่องความชื้นว่าง 9 ค่าเพื่อการเรียนตามที่อาจารย์อนุญาต. ดู `data/README.md`.

## ติดตั้งและเปิด Notebook — Windows PowerShell

ทดสอบจริงวันที่ 14 ต.ค. 2569 บน **Windows 11, Python 3.13.11 (64-bit)**. ติดตั้ง Python 3.13 ก่อน; หาก `py -3.13` หาไม่พบ ใช้ path ของ `python.exe` รุ่น 3.13 แทน. ติดตั้ง dependencies ต้องใช้อินเทอร์เน็ตหรือ pip cache.

เปิดโฟลเดอร์ที่แตก ZIP ซึ่งมี `README.md`, `config.py`, `requirements.txt` ใน File Explorer → คลิก address bar → พิมพ์ `powershell` → Enter. Windows 11 ใช้คลิกขวา → **Open in Terminal** ได้. ทุกคำสั่งต่อไปนี้รันจากโฟลเดอร์นี้.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m ipykernel install --sys-prefix --name seoul-bike --display-name "Python (Seoul Bike)"
.\.venv\Scripts\python.exe -m notebook notebooks
```

เรียก Python ของ `.venv` โดยตรง จึงไม่ต้อง activate และไม่ติดปัญหา ExecutionPolicy. `pip check` ต้องแสดง `No broken requirements found.`

เปิด Notebook แล้วเลือก **Kernel → Change Kernel → Python (Seoul Bike)**. รันตามลำดับ `00_setup` → `01_eda` → `02_modeling`; แต่ละไฟล์เลือก **Kernel → Restart Kernel and Run All Cells** (บางหน้าจอชื่อ Restart Kernel & Run All) และบันทึกเมื่อจบ. `01_eda` ตรวจวัน split ที่แนบและสร้างใหม่เฉพาะเมื่อยังไม่มีไฟล์.

หรือรันอัตโนมัติจาก kernel ใหม่ทุกไฟล์:

```powershell
.\.venv\Scripts\python.exe scripts\run_notebooks.py
```

สคริปต์ลงทะเบียน kernel ใน `.venv` เอง เก็บ outputs กลับใน Notebook, กราฟใน `figures/`, logs/tables ใน `verification/`. รอบอ้างอิง: setup **1.5 s**, EDA **10.9 s**, modeling **225.0 s** รวมประมาณ **4 นาที** ไม่รวมติดตั้ง. เวลาขึ้นกับเครื่อง thread และโหลดขณะรัน.

## ผลสำคัญที่ควรเห็น

| รายการ | ผลรอบอ้างอิง |
|---|---|
| split ก่อนกรอง | train 7,008 ชั่วโมง/292 วัน; test 1,752 ชั่วโมง/73 วัน |
| EDA ระบบเปิด ก่อนกรองพายุ | train 6,768 ชั่วโมง/282 วัน |
| หลัง scope | train 6,672 ชั่วโมง/278 วัน; test 1,656 ชั่วโมง/69 วัน |
| X ก่อน preprocess | 18 คอลัมน์ รวม `rain_prev_3h` |
| หลัง preprocess | Linear 59; kNN 37; RF/HGB 36 |
| FS บน default | Linear RFE40/59: 262.26; kNN MI10/37: 179.15; RF/HGB ชุดย่อยไม่ชนะทั้งหมด |
| PCA | 14 PC ≥90%, 19 PC ≥95%; PCA15 ช่วย kNN cyclic 191.9 →184.1 แต่ไม่ช่วย Linear |
| baseline เวลา | CV MAE 398.4 |
| tuned finalists CV MAE ±std | Linear log 205.86±9.97; kNN log 176.83±10.39; RF 117.77±4.12; **HGB 104.86±3.96** |
| test ของ HGB | **MAE 91.46**, MSE 22,219.3, RMSE 149.06, R² 0.938 |
| รวมวันพายุ ด้วยโมเดลเดิม | 1,697 ชั่วโมง/71 วัน: MAE 95.48; พายุ 41 ชั่วโมง MAE 257.65 |
| prediction สมมติ | 2,960 /569 /2,233 /605 คัน/ชม. |
| HGB fit /latency รอบอ้างอิง | 1.827 s /5.55 ms ต่อ 1 แถว (median 30 ครั้ง) |

ผู้ชนะ: `HistGradientBoostingRegressor(learning_rate=0.1, max_iter=200, max_leaf_nodes=63, min_samples_leaf=5, l2_regularization=1.0, random_state=42)`; hour raw, `SelectKBest(mutual_info_regression, k=36)` เก็บทั้งหมด 36/36. Pipeline รวม preprocessing/selector; สาธิต prediction ใน Notebook ไม่แนบโมเดลเก่า.

## เปิดเว็บแอป

ติดตั้งแพ็กเกจจาก `bike-regression/app/requirements.txt` ใน Python 3.13 แล้วรัน `python bike-regression/app/app.py` จากโฟลเดอร์โปรเจกต์ หรือเปิด [คู่มือแอป](bike-regression/app/README.md). โฟลเดอร์แอปมีโมเดลและไฟล์คะแนนครบ รันแยกจากโค้ดฝึกได้. หากต้องสร้างโมเดลซ้ำ ให้รัน `python scripts/export_app_model.py` ใน environment ที่ติดตั้ง requirements ของโปรเจกต์; สคริปต์จะตรวจคะแนนกับ `verification/results.json` ก่อนบันทึกไฟล์.

## เปิดเอกสารและสไลด์ offline

- ดับเบิลคลิก `reports/report.pdf` หรือเปิด `reports/report.html` ใน Edge/Chrome. HTML ใช้รูปใน `figures/` ต้องเก็บโครงสร้างโฟลเดอร์ครบ.
- สไลด์: `slides/seoul-bike-presentation.html` → **← /→**, Home/End, คลิกครึ่งซ้าย/ขวา หรือปุ่มขั้นด้านล่าง; F11 เต็มจอ. รอเลขนับประมาณ 2 วินาทีให้จบ. หน้า 17 กดปุ่มสถานการณ์ทั้ง 4 ชุด.
- ภาพรวม: `slides/seoul-bike-overview.html` → **← /→**, **M** กลับแผนที่, คลิกจุดขั้น; ปุ่ม **โหมดอ่าน/โหมดสไลด์** เปลี่ยนการแสดงผล.
- บทพูด: `slides/speaker-script.html` → แถบผู้พูด A/B/C และถาม-ตอบ; มีตัวจับเวลา. HTML ใช้ JavaScript ในเครื่องและฟอนต์ Leelawadee UI/Tahoma บน Windows ไม่โหลดฟอนต์/ไลบรารีภายนอก.

## สร้าง processed dataset และ PDF ซ้ำ

```powershell
.\.venv\Scripts\python.exe scripts\make_dataset.py
.\.venv\Scripts\python.exe scripts\run_notebooks.py
.\.venv\Scripts\python.exe scripts\sync_documents.py
.\.venv\Scripts\python.exe reports\build_pdf.py
```

`make_dataset.py` ใช้ raw CSV และ seed 42 ทำช่องความชื้นว่าง 9 จาก 17 ช่องที่เป็น 0; ส่วนอื่นเหมือน raw ทุก byte. หลังรันใหม่ `sync_documents.py` ปรับตารางเวลา รูปฝัง และคำอธิบายเวลาใน Notebook จาก `verification/results.json`; หากเปลี่ยน configuration ต้องตรวจตัวเลขเนื้อหาอื่นใหม่ด้วยตาราง audit. `build_pdf.py` ใช้ Edge/Chrome ด้วยโปรไฟล์ชั่วคราวแยก ไม่ต้องติดตั้งแพ็กเกจเพิ่ม.

## ข้อจำกัดและ policy คะแนน

เลือก configuration ด้วย 5-fold GroupKFold ตามวันบน train; learned steps อยู่ใน Pipeline. **Holdout เดิมเคยใช้หลาย revision**; รอบสุดท้ายตรึง configuration จาก train CV ก่อนประเมิน แต่ยังมีความเสี่ยงจากการใช้ holdout ซ้ำ ควรยืนยันด้วยข้อมูลใหม่.

CV/train MAE ใช้ค่าก่อน clip; test/sensitivity/สถานการณ์ clip ค่าติดลบเป็น 0. Test ถูก clip 15 แถว: MAE ก่อน clip 91.65 หลัง clip 91.46. อ่านคะแนนพร้อม policy และสัดส่วนฤดู (test Winter 33.3%, train 24.1%); ไม่ใช้คะแนนคู่นี้ยืนยันว่าไม่มี overfitting.

ฝนตกใน test 89 ชั่วโมง: MAE 143.0 หรือ 83.2% ของยอดเฉลี่ย (ไม่ใช่ MAPE). ตัวอย่างฝนเปลี่ยนอากาศหลายตัวพร้อมกัน จึงเปรียบเทียบ **ชุดสถานการณ์** ไม่ใช่ผลเชิงสาเหตุของฝนอย่างเดียว. ข้อมูลปีเดียว เมืองเดียว split สุ่มวัน และใช้อากาศที่วัดจริง ยังไม่ทดสอบ forecast error หรือข้ามปี.

## ปัญหาที่พบจริงระหว่างทดสอบ

- Kernel/เวอร์ชันผิด: เลือก Python (Seoul Bike), ตรวจ `sys.executable` แล้วติดตั้งผ่าน Python ของ `.venv`; setup จะ assert เวอร์ชัน.
- CSV อ่าน UTF-8 ไม่ได้: ใช้ `config.RAW_ENCODING="cp1252"`, `DATE_FORMAT="%d/%m/%Y"`.
- สคริปต์พิมพ์ไทยผ่าน pipe บน Windows เคยเกิด `UnicodeEncodeError`: แก้ stdout/stderr เป็น UTF-8 แล้ว และทดสอบ pipe จริง.
- Windows sandbox เคยให้ `Access is denied` ตอนสร้าง temporary kernelspec: ข้อจำกัด sandbox ของเครื่องตรวจ; terminal ปกติรันผ่าน. kernel อยู่ใน `.venv` ของโฟลเดอร์ ZIP ที่แตกใหม่ ไม่ต้องอาศัย checkout เดิม.
- รอบอ้างอิงพบ `joblib resource_tracker KeyError` ตอนปิด kernel หลังงานขนาน: ทุก cell ผ่านและไม่มี Notebook error; เป็นข้อความ cleanup ใน log. ตรวจ cell traceback และ `execution.json` ก่อนตัดสินว่าการรันล้มเหลว.
- สร้าง PDF ไม่พบ browser: ติดตั้ง Edge/Chrome หรือเปิด HTML แล้ว Print → Save as PDF; PDF สำเร็จรูปแนบไว้แล้ว.

## โครงสร้างชุดส่ง

`config.py`, `requirements.txt`, `notebooks/`, `data/`, `scripts/`, `figures/`, `reports/`, `slides/`, `verification/` (ผลและหลักฐาน), `bike-regression/app/` (เว็บแอปและโมเดลที่ export). ไม่รวม `.git`, `.venv`, worktrees, cache, ไฟล์ทดลอง หรือ `models/model.joblib` รุ่นเก่า.
