import argparse
import json
import platform
import subprocess
import sys


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8", errors="ignore")


def get_wifi_passwords() -> dict[str, str | None]:
    wifi_passwords: dict[str, str | None] = {}
    system = platform.system()

    if system == "Windows":
        out = _run(["netsh", "wlan", "show", "profiles"])
        profiles = [line.split(":", 1)[1].strip() for line in out.splitlines() if "All User Profile" in line]
        for profile in profiles:
            try:
                detail = _run(["netsh", "wlan", "show", "profile", profile, "key=clear"])
                pw = [line.split(":", 1)[1].strip() for line in detail.splitlines() if "Key Content" in line]
                wifi_passwords[profile] = pw[0] if pw else None  # None = open network / no key stored
            except subprocess.CalledProcessError as e:
                wifi_passwords[profile] = f"ERROR: {e}"

    elif system == "Linux":
        import pathlib
        folder = pathlib.Path("/etc/NetworkManager/system-connections/")
        if not folder.exists():
            print("NetworkManager folder not found. Run with sudo, or use `nmcli` instead.")
            return {}
        for path in sorted(folder.iterdir()):
            if not path.is_file():
                continue
            try:
                psk = None
                for line in path.read_text(errors="ignore").splitlines():
                    if line.strip().startswith("psk="):
                        psk = line.split("=", 1)[1].strip()
                wifi_passwords[path.name] = psk
            except PermissionError:
                wifi_passwords[path.name] = "ERROR: permission denied — re-run with sudo"
            except OSError as e:
                wifi_passwords[path.name] = f"ERROR: {e}"
    else:
        print(f"Unsupported OS: {system}. This script supports Windows and Linux only.")
    return wifi_passwords


def main():
    ap = argparse.ArgumentParser(description="List saved WiFi passwords on YOUR OWN device.")
    ap.add_argument("--output", default=None, help="Optional JSON file to save results to")
    args = ap.parse_args()

    passwords = get_wifi_passwords()
    if not passwords:
        print("No saved WiFi profiles found.")
        return
    for name, pw in passwords.items():
        print(f"{name}: {'(no key / open)' if pw is None else pw}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(passwords, f, indent=4)
        print(f"\nSaved to {args.output} — keep this file private, it contains passwords!")


if __name__ == "__main__":
    main()
