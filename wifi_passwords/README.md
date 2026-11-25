# WiFi Password Viewer

Shows saved WiFi profiles/passwords stored on **your own computer**.

## ⚠️ Ethics / Safety
For YOUR OWN device only. Do NOT run this on someone else's device without permission — that is unauthorized access.

## Requirements
- Python 3.9+
- Windows: `netsh` (built-in). May need admin for `key=clear`.
- Linux: reads `/etc/NetworkManager/system-connections/` — re-run with `sudo` if you get permission errors.
- macOS: not supported — use Keychain Access instead.

## Run
```bash
python wifi_passwords.py
python wifi_passwords.py --output wifi_passwords.json
```

## Output
Prints `profile: password` for each saved network. `None` / `(no key / open)` means an open network or no key stored.

## Security note
The `--output` JSON file contains passwords. Keep it private, don't commit it to git, delete it when done. The script itself stores nothing — it only reads what the OS already saved.

## Limitations
- Only shows networks this machine has connected to before.
- Some Windows setups block `key=clear` without admin rights.
- Linux systems using `iwd` / `wpa_supplicant` without NetworkManager won't be listed.
