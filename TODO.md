# Vaultsync Project — TODO

## 🛠️ Critical Improvements

- [ ] **Prevent multiple appends of Orbit daily note into Atlas journal**
  - Deduplicate daily notes
  - Option: Check if note already contains Orbit note content before appending
  - Option: Add unique marker in append to detect if already inserted

## 🚀 Next Improvements

- [ ] Optional: Add log rotation (if we later add logging)
- [ ] Optional: Add environment variable support for date override (for manual backfills)
- [ ] Optional: Add argument parsing (allow override paths at runtime)
- [ ] Optional: Systemd timer or cronjob automation
- [ ] Optional: Add test suite for sync logic
- [ ] Optional: Prettify terminal output (optional Rich library)

## 🧩 Future Enhancements

- [ ] Obsidian Plugin version (native integration)
- [ ] Optional UI / log viewer
- [ ] Optional: Diff-checking before append
- [ ] Optional: Archive completed Orbit notes automatically

## ✅ Done

- [x] .env support for vault paths
- [x] Clean project structure
- [x] GitHub repository initialised
- [x] Successful initial sync and append

