"""Deliver a version of the final output to a new folder on S3, and record it.

    uv run python scripts/publish_version.py 2026.10

It stops, without uploading anything, if:
  - there are uncommitted changes,
  - the pipeline is not up to date with the code, settings and data (dvc status),
  - or this version was already delivered (the folder exists on S3).
Then it uploads the file and adds a line to deliveries.csv: date, version, S3 path, git commit.
Commit deliveries.csv and tag the commit afterwards (see page 5 of the tutorial).
"""
import csv
import datetime
import subprocess
import sys
from pathlib import Path

import boto3

from helpers import ROOT, load_config


def stop(message: str) -> None:
    print(f"Not delivered: {message}")
    sys.exit(1)


def run(*command: str) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True)


if len(sys.argv) != 2:
    stop("give the version to deliver, for example: publish_version.py 2026.10")
version = sys.argv[1]
settings = load_config()["publish"]

# 1. Only deliver results that match committed code, settings and data
if run("git", "status", "--porcelain").stdout.strip():
    stop("there are uncommitted changes. Commit them first.")
if run("dvc", "status", "--quiet").returncode != 0:
    stop("the pipeline is not up to date. Run: uv run dvc repro, then commit.")

# 2. Never overwrite a delivered version
s3 = boto3.client("s3")
folder = f"{settings['prefix']}/{version}/"
if s3.list_objects_v2(Bucket=settings["bucket"], Prefix=folder).get("KeyCount", 0):
    stop(f"version {version} already exists in s3://{settings['bucket']}/{folder}")

# 3. Upload
source = ROOT / settings["file"]
key = folder + source.name
s3.upload_file(str(source), settings["bucket"], key)
destination = f"s3://{settings['bucket']}/{key}"

# 4. Record it
commit = run("git", "rev-parse", "HEAD").stdout.strip()
record = ROOT / "deliveries.csv"
new_file = not record.exists()
with open(record, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    if new_file:
        writer.writerow(["date", "version", "destination", "commit"])
    writer.writerow([datetime.date.today().isoformat(), version, destination, commit])

print(f"Delivered {source.relative_to(ROOT)} to {destination}")
print("Now commit deliveries.csv and tag this version (page 5, section 7).")
