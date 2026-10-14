"""สร้าง ZIP ชุดส่งจาก allowlist; ไม่รวม Git, environment, cache หรือโมเดลเก่า."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
TOP_FILES = ["README.md", "requirements.txt", "config.py"]
DIRECTORIES = ["notebooks", "data", "scripts", "figures", "reports", "slides"]
EVIDENCE = ["results.json", "execution.json", "environment-lock.txt", "pip-check.txt",
            "00_setup-output.txt", "01_eda-output.txt", "02_modeling-output.txt",
            "run.log", "utf8-pipe.txt", "pdf-build.txt", "browser.log", "content-audit.log",
            "content-checks.json", "table-checks.csv", "submission-audit.md", "zip-test.json", "jupyter-check.json"]


def main():
    paths = [ROOT / name for name in TOP_FILES]
    for name in DIRECTORIES:
        paths += [p for p in (ROOT / name).rglob("*") if p.is_file()
                  and not any(part in {"__pycache__", ".ipynb_checkpoints", ".git", ".venv"} for part in p.parts)
                  and p.suffix not in {".pyc", ".joblib"} and p.name != ".gitkeep"]
    paths += [ROOT / "verification" / name for name in EVIDENCE if (ROOT / "verification" / name).exists()]
    paths += list((ROOT / "verification").glob("*.csv"))
    paths += list((ROOT / "verification/previews").glob("*.png"))
    paths += [ROOT / "verification/browser/checks.json"]
    paths = sorted(set(paths))
    manifest = {str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    manifest_path = ROOT / "verification/manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),encoding="utf-8")
    paths.append(manifest_path)
    dest = ROOT / "dist"
    dest.mkdir(exist_ok=True)
    output = dest / "Seoul-Bike-Demand-submission.zip"
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for p in paths:
            archive.write(p,"seoul-bike-demand/"+str(p.relative_to(ROOT)).replace("\\", "/"))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert {p.split("/")[0] for p in archive.namelist()} == {"seoul-bike-demand"}
        assert not any(bad in p.split("/") for p in archive.namelist() for bad in {".git",".venv",".claude","__pycache__"})
    print(f"{output.name}: {len(paths)} files, {output.stat().st_size:,} bytes")
    print("SHA256",hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
