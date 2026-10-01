"""A thin runner that keeps familiar commands, while DVC does the work.

    uv run python run_pipeline.py                 # run everything that is out of date
    uv run python run_pipeline.py --only scores   # bring one part up to date (and what it needs)
    uv run python run_pipeline.py --check         # what is out of date, and what would run
    uv run python run_pipeline.py --list          # show the pipeline

Every run is also written to logs/run_<date>_<time>.log (add logs/ to .gitignore).
Edit PARTS so that each part names the last stage of that part in dvc.yaml.
"""
import argparse
import datetime
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PARTS = {
    "macro": "macro_project",
    "scores": "scores_project",
    "pricing": "pricing_project",
}


def dvc(*args: str) -> int:
    command = ["dvc", *args]
    print(f"> {' '.join(command)}", flush=True)
    log_dir = ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"run_{datetime.datetime.now():%Y%m%d_%H%M%S}.log"
    with open(log_file, "w", encoding="utf-8") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                   errors="replace")
        for line in process.stdout:
            print(line, end="")
            log.write(line)
        return process.wait()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", choices=PARTS, help="bring one part up to date")
    parser.add_argument("--check", action="store_true", help="show what would run, run nothing")
    parser.add_argument("--list", action="store_true", help="show the pipeline")
    args = parser.parse_args()

    if args.list:
        return dvc("dag")
    if args.check:
        return dvc("status") or dvc("repro", "--dry")
    if args.only:
        return dvc("repro", PARTS[args.only])
    return dvc("repro")


if __name__ == "__main__":
    sys.exit(main())
