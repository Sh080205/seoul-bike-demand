# ผลตรวจชุดส่ง Seoul Bike Demand

ตรวจวันที่ 14 ต.ค. 2569 (Asia/Bangkok). ใช้ผลจาก kernel รอบอ้างอิงเดียวกันทั้งหมด; ไม่ปรับโมเดลหรือ scope ให้ตรง audit เดิม.

## ฐาน Git และงานล่าสุด

- repository ไม่มี AGENTS.md/CLAUDE.md ที่ใช้กับ worktree นี้; ตรวจ README, config, requirements และ .gitignore ก่อนแก้.
- fetch GitHub ใหม่: main/origin/main = `904a996`; PR #25 OPEN ที่ `3e96c5e`; PR #26 OPEN ที่ `3eff48a` รวม commit ของ #25 แล้ว. ไม่มี commit เดิมที่ยังไม่ push จากการตรวจ local branches เทียบ remotes.
- ฐานเนื้อหาชุดส่ง = `3eff48a`. จุดร่วมกับ main คือ `6b1901d`; main มี merge commit #24 จึงรวมด้วย merge บน `codex/submission-ready` รักษาสองเส้นประวัติ. ไม่ cherry-pick #25 ซ้ำ. checkout หลักและ branch เดิมคงอยู่.
- [PR #25](https://github.com/Sh080205/seoul-bike-demand/pull/25), [PR #26](https://github.com/Sh080205/seoul-bike-demand/pull/26) ยังไม่ merge เข้าสู่ main. ชุดส่งรวมเนื้อหาทั้งสองแล้ว. branch เตรียมส่งเป็น local; ไม่ได้ push หรือ merge PR บน GitHub.

## ตารางผลรันจริงเทียบข้อความชุดส่ง

Notebook outputs และ `results.json`/CSV เป็นแหล่งอ้างอิง. ทุกค่าในตารางเป็นผลรอบอ้างอิง; เอกสารอาจปัดทศนิยมตามพื้นที่แสดง. รายงาน PDF มาจาก HTML ล่าสุด.

| หัวข้อ / ผลรันจริง | ข้อความในไฟล์ชุดส่ง | ตรงหรือไม่ | การแก้ไขและหลักฐาน |
|---|---|---|---|
| Raw 8,760×14 ไม่มี missing; processed เพิ่ม missing RH 9 | README, data README, 01_eda, รายงาน§2, สไลด์3, overviewโหลดข้อมูล, บทพูดหน้า3 แยกบริบท | ตรง | แก้ data README เดิมที่รวม raw กับ processed; ตรวจ shape/NaN และสคริปต์ seed42 |
| split train7,008/292วัน; test1,752/73วัน; ปิด240/55ชั่วโมง | Notebook01/02, รายงาน3.1, สไลด์4/7, overview3/5 | ตรง | เก็บ splitเดิม; ไม่เปลี่ยน testเพื่อคะแนน |
| EDA trainเปิด6,768/282วัน; modeling6,672/278วัน; testในscope1,656/69วัน | README,รายงาน4/5.1,สไลด์6/7,overview4/5 | ตรง | รักษา6,768ในEDA; ไม่replaceรวมทั้งโปรเจกต์ |
| sensitivityทุกชั่วโมงเปิด1,697/71วัน; พายุ41/2วัน | รายงาน11.2,สไลด์15,overviewtest,บทพูด15/Q&A | ตรง | ไม่refit; predictionปกติในชุดรวมตรงกับผลหลัก; priorrainขาด3ค่าใช้trainmedian |
| rain_prev_3h=h−1+h−2+h−3ในวันเดียวกัน,ไม่รวมปัจจุบัน/ไม่ข้ามเที่ยงคืน; missingภายในวัน→NaN | Notebook5.3,รายงาน5.2/5.4,สไลด์7,overview5,บทพูด/Q&A | ตรง | JSกราฟ/ตัวอย่างและinputสมมติไม่คำนวณhistoryจากแถวซ้ำ; priorrain0ทุกชุด |
| X18; preprocessLinear59,kNN37,RF/HGB36 | Notebook5.6/6.3/7,README,รายงาน5.3,สไลด์7/10,overview5 | ตรง | แก้Notebookคำอธิบายinput17→18 และgridFilter/RFE58→59; HGBMI36เก็บ36/36 |
| priorrain pairedCV112.15±4.23→109.18±2.93; ดีขึ้น5fold | รายงาน5.5,สไลด์7,overview5,บทพูดB | ตรง | CVบนtrain; ไม่ใช้testเลือกfeature |
| FS LinearRFE40/59=262.26±2.90; Lassoalpha.3,52features=262.45; kNNMI10/37=179.15±8.96; RF/HGBชุดย่อยไม่ชนะ | Notebook7,รายงาน6.1–6.3,สไลด์10–11,overview7,บทพูดB/Q&A | ตรง | ตรวจmatrixและproxyRFสำหรับHGB; ไม่อ้างselectorชื่อMI36ว่าลดมิติ |
| PCA14PC≥90%,19PC≥95%; Linearcyclic311.3→PCA15 324.6;kNN191.9→184.1 | Notebook8,รายงาน7,สไลด์10–11,overview8,บทพูด10 | ตรง | รูปPCAฝังhashตรงfigures; ไม่ใช้varianceแทนความแม่นy |
| baseline mean527.6,median512.6,time398.4; defaultLinear262.5,kNN191.9,RF119.1,HGB109.2 | Notebook9–10,รายงาน8.1,สไลด์12–13,JS MODELS,overview9–10,บทพูดC | ตรง | ตรวจMSE/RMSE/R²/std/trainMAEทุกแถวพร้อมCSV; ค่าปัดเป็นbaselinecontext |
| tunedLinearraw262.3/log205.9;kNNraw177.1/log176.8;RF117.8;HGB104.9/log107.3 | Notebook11,รายงาน9.1,สไลด์14,overview11,บทพูด14/Q&A | ตรง | ผู้ชนะHGBraw; รายงานงบค้นและselectionbias ไม่อ้างFSเป็นเหตุเดียว |
| HGBMI36: lr.1,iter200,leaves63,minleaf5,l2=1,seed42; CV104.86019±3.95890 | Notebook12,README,รายงาน10,สไลด์14,overview12,บทพูด14 | ตรง | ตรวจsearch_parametersในresults.jsonและPipelineoutput; selectorเก็บทุก36คอลัมน์ |
| testMAE91.46262,MSE22219.27193,RMSE149.06130,R².93754 | Notebook13.1,README,รายงาน11.1,สไลด์1/15/18,data-to,overview13,บทพูด15 | ตรง | ปัด91.46/22,219.3/149.06/.938; animationจบได้ค่าตรง |
| รวมพายุMAE95.47773,MSE26864.87925,RMSE163.90509,R².92457; เฉพาะพายุMAE257.64895 | Notebook13.1.1,รายงาน11.2,สไลด์15,overview13,บทพูด/Q&A | ตรง | 23ส.ค.24ชั่วโมงMAE345.29;6ต.ค.17ชั่วโมงMAE133.91;ตรวจweightedMAE |
| train–CV defaultgapLinear5.2,kNN40.1,RF82.5,HGB42.4 | Notebook10,รายงาน8,สไลด์12–13,overview10,บทพูด12–13 | ตรง | ใช้gapประกอบerror; ไม่พิสูจน์over/underfitด้วยgapค่าเดียว |
| seasonMAE Winter51.0,Spring91.3,Autumn124.1,Summer116.8;วันทำงาน98.0/วันหยุด78.3 | Notebook13.2,รายงาน11.3,สไลด์15,overviewerror,บทพูด | ตรง | ตรวจn,mean_y,bias,MAE/meanทุกกลุ่ม; testWinter33.3%เทียบtrain24.1% |
| ฝน89ชั่วโมงMAE143.0/mean171.9=83.2%;ไม่มีฝน1,567ชั่วโมงMAE88.5 | Notebook13.2,README,รายงาน11.3,สไลด์15,overview13,บทพูด/Q&A | ตรง | อัตราMAE/meanไม่ใช่MAPE; ไม่ยืนยันสาเหตุจากกลุ่มตัวอย่างเล็ก |
| ชั่วโมงMAEสูงสุด08:00≈176,18:00≈158,19:00≈145;ต่ำสุด04≈20,05≈29,03≈31 | Notebook13.3/by_hour.csv,รายงาน11.3/กราฟ,overviewerror | ตรง | รูป13_test_errorsทั้งไฟล์และbase64ตรงรอบนี้ |
| worstแรก2018-09-24 18:00:จริง1,237ทาย2,120error+883; worst10มี8แถวทายเกิน | Notebook13.4/worst.csv,รายงาน11.4,สไลด์16,overviewworst,บทพูด16/Q&A | ตรง | ตรวจทั้ง10แถวรวมอากาศจริง;23ส.ค.ไม่อยู่เพราะscope |
| สถานการณ์2,960/569/2,233/605; priorrain0ทุกชุด | Notebook13.5/scenarios.csv,รายงาน12.1,JS SCEN/ปุ่ม17,overviewprediction,บทพูด17/Q&A | ตรง | เปลี่ยนคำทีละปัจจัย→เปรียบเทียบชุดสถานการณ์ เพราะเปลี่ยนอากาศหลายตัว |
| เวลาจากรอบอ้างอิง HGB1.827s/5.55ms;RF5.944/15.51;kNNlog1.161/3.30;Linearlog.026/4.10 | Notebook12,clo4.csv,README,รายงาน10.1/ข้อความ,สไลด์14,overview12 | ตรง | อัปเดตทั้งตารางและข้อความ; medianlatency30ครั้ง; เวลาขึ้นกับเครื่อง |
| cliptest15แถว;MAEก่อนclip91.64670/หลัง91.46262;CVก่อนclip | Notebook13.1,README,รายงาน11.1,สไลด์15/overviewสรุป,บทพูด/Q&A | ตรง | เปิดเผยpolicyต่างกัน ไม่เปลี่ยนCV/modelเดิมเพื่อจับคะแนน |
| holdoutเดิมเคยใช้หลายrevision;รอบสุดท้ายตรึงconfigurationก่อนประเมิน | Notebook01/02,README,รายงาน11.1,สไลด์15,overviewสรุป,บทพูด15/Q&A | ตรง | ตัดคำtestครั้งเดียว;เปิดเผยความเสี่ยงholdoutซ้ำและเสนอข้อมูลใหม่ |
| สมาชิก6330300160ชญานิน,6730300591ศุภวิชญ์,6730300850พัฒนเดช | README/ปกรายงาน/สไลด์/บทพูด ใช้ชื่อรหัสเดียวกัน | ตรง | เทียบชื่อและบทบาทA/B/Cครบ;setupchecklistแก้ตามงานที่ทำแล้ว |
| ตาราง5.1scope/5.2features/5.3encoding/5.4folds/5.5rain;11.1test/11.2sensitivity/11.3errors/11.4worst | รายงานและอ้างข้ามไฟล์ | ตรงหลังแก้ | แก้ลำดับcaption/altรูปและreferenceoverview/Q&A |

`table-checks.csv` และ `content-checks.json`: 165 automated checks ผ่านทั้งหมด (การปัดตามจำนวนทศนิยมที่แสดง). ส่วนคำอธิบาย/พารามิเตอร์/ข้อจำกัดในตารางนี้สอบทานกับsourceและoutputsด้วย. `results.json` มีค่าละเอียดและCSVครบทุกหัวข้อ.

## การทดสอบจริงและหลักฐาน

- Python3.13.11/Windows11;ติดตั้งrequirementsใน.venvใหม่และpipcheckผ่าน (`pip-check.txt`, `environment-lock.txt`). คำสั่งpy-3.13,ipykernelinstallและnotebook7.6.3ใช้ได้ในterminalปกติ.
- kernelใหม่แยกทุกNotebook:00_setup2codecells/1.46s,01_eda23/10.93s,02_modeling34/224.96s;executionเรียงครบและไม่มีcellerror (`execution.json`,outputsNotebook,logs).
- UTF-8:make_dataset.pyและbuild_pdf.pyพิมพ์ไทยผ่านpipe/ไฟล์ได้;processedเปลี่ยนเพียง9ช่องความชื้น (`utf8-pipe.txt`).
- PDF23หน้าA4:เรนเดอร์ทุกหน้าด้วยPoppler ตรวจภาษาไทยตารางรูปoverflowหน้าว่างและเลขหน้า1ปกไม่แสดง/2–23ครบ;ไม่มีภาพหาย (`pdf-build.txt`, `previews/contact-*.png`).
- OfflineChrome:สไลด์18/overview28 ไม่มีJavaScripterror,requestภายนอก,รูปหายหรือboundingoverflow;navigationHome/ArrowRight/ArrowLeftและสถานการณ์4ชุดผ่าน. รอ2.4วินาทีหลังเลขนับและ8.5วินาทีหน้าcodeก่อนตรวจ (`browser/checks.json`, `browser.log`, `previews/`).
- ตัดCDNfontใช้LeelawadeeUI/TahomaบนWindows;ไม่เพิ่มdependencyภายนอกสำหรับเปิดเอกสาร.
- โมเดลเก่าในcheckoutหลักมี17featureไม่มีrain_prev_3h;ไม่แนบjoblibใดในZIP. โมเดลสุดท้ายสร้างในkernelและสาธิตinputผ่านPipelineแล้ว.
- มีjoblibresource_trackerKeyErrorตอนcleanupของkernelในlogรอบอ้างอิง;ไม่ใช่cellerror ทุกผลและassertผ่าน. Windowssandboxเคยบล็อกtemporarykernelspec/launcher/SSL;terminalปกติรันผ่าน. ไม่ซ่อนข้อความเหล่านี้;READMEอธิบายวิธีตรวจ.

## ไฟล์ที่แก้และเหตุผล

README/dataREADME:คู่มือสำหรับผู้แตกZIPและแยกraw/processed/scope. Notebookทั้งสาม:แก้คำอธิบายและเก็บoutputsจากkernelใหม่. reportHTML/PDF:เวลารอบเดียว,policyholdout/clip,เลขตารางและaltรูป. สไลด์/overview/บทพูด:เวลา,รูปbase64,reference,ข้อจำกัดและฟอนต์offline. make_dataset/build_pdf:UTF-8stdout. scriptsเพิ่มrun_notebooks/export_results/sync_documents/audit_submission/package_submissionเพื่อทำซ้ำและเก็บหลักฐาน; .gitignoreตัดenvironment/ทดลอง/ZIPจากGit.

## ZIP และรายการค้าง

ZIPใช้allowlist มีโฟลเดอร์seoul-bike-demandชั้นเดียว พร้อมmanifestSHA256ของทุกไฟล์ ไม่รวม.git/.venv/.claude/worktrees/cache/ไฟล์ทดลอง/joblib. ผลแตกZIPและรันซ้ำจาก.venvใหม่อยู่ใน `zip-test.json`.

งานเตรียมชุดส่งไม่มีblocker. งานบนGitHubที่ยังค้างคือPR25/26ยังOPEN และbranchเตรียมส่งยังไม่push. ไม่อ้างว่าการเตรียมZIPเท่ากับmergePRหรือส่งงานให้อาจารย์แล้ว. ข้อจำกัดเชิงวิธีวิจัยคือholdoutซ้ำ,CVselectionbias,ปีเดียวเมืองเดียวและอากาศที่วัดจริง ตามที่เปิดเผยในเอกสาร.

### ผล ZIP ที่แตกใหม่

ติดตั้ง .venv ใหม่ผ่าน requirements และ pip check ผ่าน; เปิด Jupyter จริง เห็น Notebook ทั้งสามและ kernel Python ชี้ .venv ในโฟลเดอร์ที่แตกใหม่ (`jupyter-check.json`). รัน 00_setup/01_eda/02_modeling ครบ 2/23/34 code cells ใช้เวลา 2.83/14.67/219.81 วินาที. เทียบทุก metric, ตาราง, prediction และ configuration กับรอบอ้างอิงแล้วตรงกัน (ยกเว้นเวลาและตำแหน่งหน่วยความจำของ callable ซึ่ง normalize ในตัวส่งออกแล้ว). คำสั่งสร้าง processed, sync เอกสาร, สร้าง PDF และ audit หลัง sync ผ่าน. ZIP ที่ส่งเก็บ outputs/เวลาจากรอบอ้างอิงแรกไว้เหมือนกันทุกไฟล์; รอบซ้ำใช้ยืนยันความสามารถในการทำซ้ำ.
