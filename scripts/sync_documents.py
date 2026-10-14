"""Sync เวลารอบรันและรูปฝังในเอกสาร จาก verification/results.json และ figures/."""
import base64
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def main():
    results = json.loads((ROOT / "verification/results.json").read_text(encoding="utf-8"))
    timings = {r["model"]: r for r in results["tables"]["clo4"]}
    aliases = {"HGB": "HistGradientBoosting", "RF": "Random Forest",
               "Linear + log1p(y)": "Linear Regression + log1p(y)"}
    images = dict(zip(["ยอดเช่าเฉลี่ยรายชั่วโมงแยกประเภทวัน", "ยอดเช่าตามฤดูและอุณหภูมิ", "ยอดเช่าตามปริมาณฝน",
                      "Hour cyclic encoding", "CV MAE by model and selector (± fold std)",
                      "37 preprocessed columns (hour cyclic)", "Default CV MAE ± fold std", "In-scope test errors"],
                     ["04_hourly_by_daytype.png", "04_season_temperature.png", "04_rainfall.png", "05_hour_cyclic.png",
                      "07_model_feature_selection.png", "08_pca_variance.png", "10_model_comparison.png", "13_test_errors.png"]))
    files = [ROOT / "reports/report.html", *sorted((ROOT / "slides").glob("*.html"))]
    for p in files:
        text = p.read_text(encoding="utf-8")
        # source HTML ใช้ฟอนต์ Windows โดยตรง จึงไม่ต้องต่ออินเทอร์เน็ต
        text = re.sub(r'<link\b[^>]*href="https://fonts\.[^>]*>\s*', '', text)
        text = text.replace("'IBM Plex Sans Thai Looped',sans-serif", "'Leelawadee UI',Tahoma,sans-serif")
        text = text.replace("'IBM Plex Mono',monospace", "Consolas,monospace")
        text = text.replace("ผล test ครั้งเดียว", "ผล test หลังตรึงโมเดล")
        soup = BeautifulSoup(text, "html.parser")
        if p.name == "seoul-bike-presentation.html":
            for para in soup.find_all("p"):
                if "clip ลบ 15 แถว" in para.get_text():
                    para.string = "MSE 22,219.3 คัน²; CV ก่อน clip; test clip ≥0 (15 แถว)"
        seen_qa = False
        for detail in list(soup.find_all("details")):
            if detail.summary and detail.summary.get_text() == "ใช้ holdout ซ้ำ และ clip ต่างจาก CV หรือไม่":
                if seen_qa:
                    detail.decompose()
                seen_qa = True
        for table in soup.find_all("table"):
            if table.find("tr") is None:
                continue
            headers = table.find("tr").get_text(" ", strip=True)
            if "fit" in headers and ("ms/แถว" in headers or "ms/แถว" in table.get_text()):
                for row in table.find_all("tr")[1:]:
                    cells = row.find_all("td")
                    if not cells:
                        continue
                    key = aliases.get(cells[0].get_text(strip=True), cells[0].get_text(strip=True))
                    if key in timings:
                        r = timings[key]
                        cells[-2].string = f'{r["fit ทั้ง train (s)"]:.3f}'
                        cells[-1].string = f'{r["latency / 1 แถว (ms)"]:.2f}'
        for im in soup.find_all("img"):
            if im.get("alt") in images:
                im["src"] = "data:image/png;base64," + base64.b64encode((ROOT / "figures" / images[im["alt"]]).read_bytes()).decode()
        if p.name == "report.html":
            for fig in soup.find_all("figure"):
                if fig.img and fig.figcaption:
                    fig.img["alt"] = fig.figcaption.get_text(" ",strip=True)
            for para in soup.find_all("p"):
                if para.get_text().startswith("เวลาขึ้นกับเครื่อง"):
                    parts = [f'{short}: fit {timings[name]["fit ทั้ง train (s)"]:.3f} s, predict {timings[name]["latency / 1 แถว (ms)"]:.2f} ms/แถว'
                             for short,name in [("HGB","HistGradientBoosting"),("RF","Random Forest"),("kNN log","kNN + log1p(y)"),("Linear log","Linear Regression + log1p(y)")]]
                    para.string = "เวลาขึ้นกับเครื่อง จำนวน thread และสภาพขณะรัน; ค่ารอบเดียวกับ Notebook ชุดส่ง: " + "; ".join(parts) + ". fit รวม preprocessing/selector; latency เป็น median 30 ครั้งต่อ input 1 แถว ไม่ใช่ benchmark production"
                if "รอบแก้ไขนี้ไม่รัน 00_setup ใหม่" in para.get_text():
                    para.string = "Python 3.13.11 บน Windows; requirements.txt pin เวอร์ชัน; random_state=42. ชุดส่งรัน 00_setup → 01_eda → 02_modeling จาก kernel ใหม่ทุกไฟล์ ครบทุก cell พร้อม outputs; ดูเวลาและ environment ใน verification/execution.json และ environment-lock.txt. ใช้คำสั่งใน README เพื่อสร้าง .venv และรันซ้ำ; ไม่มีไฟล์โมเดลเก่าในชุดส่ง"
            policy = soup.new_tag("p",attrs={"class":"note"})
            policy.string = "CV/train MAE ใช้ค่าก่อน clip; test/sensitivity/สถานการณ์ใช้ clip ≥0 (test ติดลบ 15 แถว). Holdout เดิมเคยใช้ในหลาย revision; รอบนี้ประเมินหลังตรึง configuration จาก train CV จึงยังมีความเสี่ยงจากการใช้ holdout ซ้ำ ควรยืนยันด้วยข้อมูลใหม่"
            section = next(s for s in soup.select(".report-page") if s.h3 and "11.1" in s.h3.text)
            if "Holdout เดิมเคยใช้" not in section.text:
                section.append(policy)
            intro = next(s for s in soup.select(".report-page") if s.h2 and s.h2.text == "2. ข้อมูล")
            intro.p.string = "Seoul Bike Sharing Demand (UCI id 560, CC BY 4.0) มี 8,760 แถว ×14 คอลัมน์ ครบ 365 วัน ×24 ชั่วโมง ไม่มีแถวซ้ำ. Raw ไม่มี missing; processed สร้าง missing ความชื้นเพิ่ม 9 ค่าเพื่อการเรียนตามที่อาจารย์อนุญาต โดย scripts/make_dataset.py; ทั้งสองชุดแนบครบแล้ว"
            text = str(soup)
            text = text.replace("จำนวนแถว/วันหลังกรองดูตาราง 5.4", "จำนวนแถว/วันหลังกรองดูตาราง 5.1")
            # renumber โดย token แบบชั่วคราว เพื่อไม่ชนกันระหว่างการแทน
            maps = {"5.4":"5.1", "5.1":"5.2", "5.2":"5.3", "5.3":"5.4", "11.4":"11.2", "11.2":"11.3", "11.3":"11.4"}
            if "ตารางที่ 5.4 จำนวนก่อน/หลัง" in text:
                text = re.sub(r'ตารางที่ (5\.[1-4]|11\.[2-4])\b', lambda m:"ตารางที่ @@"+maps[m[1]]+"@@", text)
                text = text.replace("@@","")
            text = text.replace("<h2>11. Error analysis แยกกลุ่ม</h2>","<h2>11. ผลบนชุดทดสอบ (ต่อ)</h2><h3>11.3 Error analysis แยกกลุ่ม</h3>")
            text = text.replace("<h2>11. ชั่วโมงที่พลาดมาก และการนำไปใช้</h2>","<h2>11. ผลบนชุดทดสอบ (ต่อ)</h2><h3>11.4 ชั่วโมงที่พลาดมาก</h3>")
        else:
            text = str(soup)
            text = text.replace("02_modeling33codecellsRunAllครบ outputsเรียง1–33", "02_modeling34codecellsRunAllครบ outputsเรียง1–34")
            text = text.replace("missing ความชื้น 9 ค่าครับ", "raw ไม่มี missing; processed เพิ่มความชื้นว่าง 9 ค่าเพื่อการเรียนครับ")
            text = text.replace("หลังตรึงโมเดล ประเมิน test ในขอบเขต", "Holdout เดิมเคยใช้หลาย revision; รอบนี้ตรึงโมเดลก่อนประเมิน test ในขอบเขต")
            if p.name == "speaker-script.html":
                text = text.replace("รายงาน5.4/11.4", "รายงาน5.1/11.2")
                text = text.replace("รายงาน11.1/11.2", "รายงาน11.1/11.3")
                text = text.replace("รายงาน11.3 แถวแรก", "รายงาน11.4 แถวแรก")
                text = text.replace("รายงาน5.3/ภาคผนวก", "รายงาน5.4/ภาคผนวก")
                qa = '<details><summary>ใช้ holdout ซ้ำ และ clip ต่างจาก CV หรือไม่</summary><p>Holdout เดิมใช้หลาย revision แล้ว รอบสุดท้ายตรึง configuration จาก train CV ก่อนประเมิน; ยังต้องยืนยันด้วยข้อมูลใหม่. CV/train MAE ก่อน clip ส่วน test/sensitivity/input สมมติ clip ≥0; test มี 15 แถวที่ถูก clip จึงอ่านคะแนนพร้อม policy นี้</p></details>'
                if not seen_qa:
                    text = text.replace('<script>',qa+'\n<script>',1)
            if p.name == "seoul-bike-presentation.html":
                text = text.replace("clip prediction ≥0", "CV ก่อน clip; test clip ≥0")
                text = text.replace("MSE 22,219.3 คัน²; clip ลบ 15 แถว", "MSE 22,219.3; CV ก่อน clip; test clip ≥0 (15 แถว)")
                text = text.replace("ตรึงโมเดลจาก CV แล้วทดสอบ", "holdout เดิมใช้หลาย revision; ตรึงจาก CV แล้วทดสอบ")
            if p.name == "seoul-bike-overview.html":
                text = text.replace("ไม่รัน 00_setup ใหม่", "รัน 00_setup ใหม่ด้วย kernel ใหม่ครบแล้ว")
                text = text.replace("รายงานตาราง 5.3", "รายงานตาราง 5.4")
                text = text.replace("รายงาน11.1/11.4", "รายงาน11.1/11.2")
                text = text.replace("8,760 แถว × 14 · ไม่มีแถวซ้ำ · missing 9 ค่า", "processed 8,760 ×14 · ไม่ซ้ำ · missing 9; raw ไม่มี missing")
                text = text.replace("testใช้ประเมินหลังเลือก ไม่ย้อนปรับ", "holdoutเดิมใช้หลายrevision; รอบสุดท้ายตรึงก่อนประเมิน")
                text = text.replace("clipค่าติดลบเป็น0", "CVก่อนclip; testclip≥0")
                text = text.replace("เอกสารทุกชุดตรงกับnotebook outputs", "holdoutเดิมใช้หลายrevision; ตรึงก่อนประเมิน; CVก่อนclip/testหลังclip")
        p.write_text(text,encoding="utf-8")
    p = ROOT / "notebooks/02_modeling.ipynb"
    nb = json.loads(p.read_text(encoding="utf-8"))
    h = timings["HistGradientBoosting"]
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            text = "".join(cell["source"])
            text = re.sub(r"เวลา fit ของผู้ชนะ [0-9.]+ วินาที, latency median [0-9.]+ ms/แถว",
                          f'เวลา fit ของผู้ชนะ {h["fit ทั้ง train (s)"]:.3f} วินาที, latency median {h["latency / 1 แถว (ms)"]:.2f} ms/แถว', text)
            text = text.replace("ลำดับงานถัดไป: sync report/PDF/slides ตามผลสุดท้าย รวมผลความไวใน 13.1.1", "รายงาน/PDF/สไลด์ sync กับผลรันสุดท้าย; รวมผลความไวใน 13.1.1")
            cell["source"] = text.splitlines(keepends=True)
    p.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    print("Sync ตารางเวลา รูปฝัง และคำอธิบายแล้ว")


if __name__ == "__main__":
    main()
