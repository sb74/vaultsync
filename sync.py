#!/usr/bin/env python3

import os
import shutil
import datetime

# === LOAD .env ===
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    else:
        print("[ERROR] .env file not found. Please create one with MASTER_VAULT and WORK_VAULT.")
        exit(1)

load_env()

MASTER_VAULT = os.getenv("MASTER_VAULT")
WORK_VAULT = os.getenv("WORK_VAULT")

if not MASTER_VAULT or not WORK_VAULT:
    print("[ERROR] MASTER_VAULT and WORK_VAULT must be set in the .env file.")
    exit(1)

EXCLUDED_DIRS = ["Journals"]
WORK_DAILY_NOTE_FOLDER = os.path.join(WORK_VAULT, "Daily Notes")
MASTER_JOURNAL_FOLDER = os.path.join(MASTER_VAULT, "Journals")

# === HELPERS ===

def should_exclude(path):
    for excluded in EXCLUDED_DIRS:
        if os.path.normpath(path).startswith(os.path.join(WORK_VAULT, excluded)):
            return True
    return False

def sync_folder(source_root, target_root, direction):
    for root, dirs, files in os.walk(source_root):
        rel_path = os.path.relpath(root, source_root)
        target_root_full = os.path.join(target_root, rel_path)

        # Exclude unwanted directories
        if should_exclude(root):
            continue

        os.makedirs(target_root_full, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_root_full, file)

            if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                shutil.copy2(source_file, target_file)
                print(f"[SYNC {direction}] {source_file} → {target_file}")

def append_work_daily_note():
    today = datetime.date.today().strftime("%Y-%m-%d")
    work_daily_note = os.path.join(WORK_DAILY_NOTE_FOLDER, f"{today}.md")
    master_journal_note = os.path.join(MASTER_JOURNAL_FOLDER, f"{today}.md")

    if not os.path.exists(work_daily_note):
        print(f"[INFO] No work daily note found for today: {work_daily_note}")
        return

    os.makedirs(MASTER_JOURNAL_FOLDER, exist_ok=True)

    if not os.path.exists(master_journal_note):
        with open(master_journal_note, "w") as f:
            f.write(f"# Journal for {today}\n\n")

    with open(work_daily_note, "r") as src:
        work_content = src.read().strip()

    if work_content:
        with open(master_journal_note, "a") as dest:
            dest.write("\n\n## Work Notes\n")
            dest.write(work_content)
            print(f"[APPEND] {work_daily_note} → {master_journal_note}")
    else:
        print(f"[INFO] Work daily note for today is empty: {work_daily_note}")

# === MAIN ===

if __name__ == "__main__":
    print("[INFO] Starting vault sync...")

    sync_folder(WORK_VAULT, MASTER_VAULT, "Work → Master")
    sync_folder(MASTER_VAULT, WORK_VAULT, "Master → Work")

    append_work_daily_note()

    print("[INFO] Vault sync complete.")
