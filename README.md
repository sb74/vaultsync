# Vault Sync Project

Your vault syncing and daily note integration tool.

## Usage

1. Edit your `.env` file to set your actual Master and Work vault paths.
2. Run `make sync` to sync notes and append your Work Daily Note into your Home Journal.
3. Optionally, create a shell alias for easy daily use.

### Shell Alias (Fish shell example):

```fish
alias vaultsync 'make -C /path/to/vault-sync-project sync'
```
