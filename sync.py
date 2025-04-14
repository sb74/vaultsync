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
        print(
            "[ERROR] .env file not found. Please create one with MASTER_VAULT and WORK_VAULT."
        )
        exit(1)


load_env()

MASTER_VAULT = os.getenv("MASTER_VAULT")
WORK_VAULT = os.getenv("WORK_VAULT")

if not MASTER_VAULT or not WORK_VAULT:
    print("[ERROR] MASTER_VAULT and WORK_VAULT must be set in the .env file.")
    exit(1)

EXCLUDED_DIRS = ["Journals", ".obsidian", ".git"]

# === HELPERS ===


def should_exclude(path, base_vault):
    rel_path = os.path.relpath(path, base_vault)

    # ✅ Allow base vault root (do not skip, do not log)
    if rel_path in (".", ""):
        return False

    parts = rel_path.split(os.sep)

    # Exclude hidden files and folders (below root only)
    if parts[0].startswith("."):
        print(f"[SKIP] {path} (hidden)")
        return True

    # Exclude explicitly listed directories (below root only)
    if parts[0] in EXCLUDED_DIRS:
        print(f"[SKIP] {path} (excluded)")
        return True

    return False


def sync_folder(source_root, target_root, direction):
    for root, dirs, files in os.walk(source_root):
        if should_exclude(root, source_root):
            continue

        rel_path = os.path.relpath(root, source_root)
        target_root_full = os.path.join(target_root, rel_path)

        os.makedirs(target_root_full, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_root_full, file)

            if should_exclude(source_file, source_root):
                continue

            if not os.path.exists(target_file) or os.path.getmtime(
                source_file
            ) > os.path.getmtime(target_file):
                shutil.copy2(source_file, target_file)
                print(f"[SYNC {direction}] {source_file} → {target_file}")


def append_work_daily_note():
    today = datetime.date.today().strftime("%Y-%m-%d")
    work_daily_note = os.path.join(WORK_VAULT, "Work Notes", f"{today}.md")
    master_journal_note = os.path.join(MASTER_VAULT, "Journals", f"{today}.md")

    if not os.path.exists(work_daily_note):
        print(f"[INFO] No work daily note found for today: {work_daily_note}")
        return

    os.makedirs(os.path.dirname(master_journal_note), exist_ok=True)

    # Read journal content
    if os.path.exists(master_journal_note):
        with open(master_journal_note, "r") as f:
            journal_content = f.read()
    else:
        journal_content = ""

    # Prepare append content: clean backlink + full content
    backlink_line = f"[[Work Notes/{today}]]"
    with open(work_daily_note, "r") as src:
        work_content = src.read().strip()

    append_block = f"{backlink_line}\n\n{work_content}\n"

    # Check if already appended
    if backlink_line in journal_content:
        print(f"[INFO] Work note already appended for today: {master_journal_note}")
        return

    # Append to journal
    with open(master_journal_note, "a") as dest:
        dest.write("\n\n" + append_block)
        print(
            f"[APPEND] {work_daily_note} → {master_journal_note} (backlink + content)"
        )


# === MAIN ===

if __name__ == "__main__":
    print("[INFO] Starting vault sync...")

    sync_folder(WORK_VAULT, MASTER_VAULT, "Work → Master")
    sync_folder(MASTER_VAULT, WORK_VAULT, "Master → Work")

    append_work_daily_note()

    print("[INFO] Vault sync complete.")
