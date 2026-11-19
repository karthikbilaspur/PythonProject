import argparse
import random
import signal
import sys
import threading
import time
from types import FrameType

import numpy as np

try:
    import pyaudio
except ImportError:
    pyaudio = None

try:
    import scapy.all as scapy  # pyright: ignore[reportMissingTypeStubs]
except ImportError:
    scapy = None

try:
    import ping3  # pyright: ignore[reportMissingTypeStubs]
except ImportError:
    ping3 = None

# --- Config ---
STOP_EVENT = threading.Event()

class SoundPlayer:
    def __init__(self):
        if pyaudio is None:
            raise RuntimeError("pyaudio not installed. Run: pip install pyaudio numpy")
        self.p = pyaudio.PyAudio()
        self.sample_rate = 44100
        # Reuse ONE stream instead of opening one per beep
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True
        )
        self.lock = threading.Lock()

    def play_sound(self, frequency: float, duration: float, volume: float = 1.0) -> None:
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        # Fade in/out to avoid clicks
        audio_data = np.sin(2 * np.pi * frequency * t) * volume
        fade = int(self.sample_rate * 0.01)
        audio_data[:fade] *= np.linspace(0, 1, fade)
        audio_data[-fade:] *= np.linspace(1, 0, fade)

        with self.lock:
            try:
                self.stream.write(audio_data.astype(np.float32).tobytes())
            except Exception as e:
                print(f"[!] Audio error: {e}")

    def play_sound_async(self, frequency: float, duration: float, volume: float = 1.0) -> None:
        threading.Thread(
            target=self.play_sound,
            args=(frequency, duration, volume),
            daemon=True
        ).start()

    def close(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        except Exception:
            pass

def get_arguments():
    parser = argparse.ArgumentParser(description="Network Scanner + Ambient Sounds + Ping Monitor")
    parser.add_argument("-t", "--target", dest="target",
                        help="Target IP / IP range. e.g. 192.168.1.1/24")
    parser.add_argument("--no-sound", action="store_true",
                        help="Disable ambient sounds")
    parser.add_argument("--no-ping", action="store_true",
                        help="Disable ping monitor")
    return parser.parse_args()

def scan(ip: str) -> list[dict[str, str]]:
    if scapy is None:
        print("[!] scapy not installed. Run: pip install scapy")
        return []

    print(f"[*] Scanning {ip} ... (needs Admin / sudo)")
    arp_request = scapy.ARP(pdst=ip)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownVariableType]
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownVariableType]
    answered_list = scapy.srp(broadcast / arp_request, timeout=2, verbose=False)[0]  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType, reportUnknownVariableType]

    clients_list: list[dict[str, str]] = []
    for element in answered_list:
        packet = element[1]
        clients_list.append({
            "ip": str(packet.psrc),
            "mac": str(packet.hwsrc),
        })
    return clients_list

def print_result(result_list: list[dict[str, str]]) -> None:
    print("\nIP\t\t\tMAC ADDRESS")
    print("-" * 60)
    if not result_list:
        print("No devices found.")
        return
    for client in result_list:
        print(f"{client['ip']}\t\t{client['mac']}")
    print(f"\n[+] Found {len(result_list)} device(s)")

def play_sounds(sound_player: SoundPlayer) -> None:
    sounds: dict[str, dict[str, float]] = {
        "raindrops":       {"min_freq": 100,  "max_freq": 300,  "min_duration": 0.1, "max_duration": 0.5},
        "rustling_leaves": {"min_freq": 500,  "max_freq": 1500, "min_duration": 0.2, "max_duration": 0.7},
        "chirping_birds":  {"min_freq": 1000, "max_freq": 5000, "min_duration": 0.2, "max_duration": 0.4},
    }

    while not STOP_EVENT.is_set():
        keys = list(sounds.keys())
        random.shuffle(keys)
        for name in keys:
            if STOP_EVENT.is_set():
                break
            p = sounds[name]
            freq = random.uniform(p["min_freq"], p["max_freq"])
            dur = random.uniform(p["min_duration"], p["max_duration"])
            vol = random.uniform(0.3, 0.7)
            print(f"[sound] Playing {name} ({int(freq)} Hz)...")
            sound_player.play_sound_async(freq, dur, vol)
            STOP_EVENT.wait(random.uniform(0.3, 0.8))

def ping_servers(servers: list[str], interval: int = 60) -> None:
    if ping3 is None:
        print("[!] ping3 not installed. Run: pip install ping3")
        return

    while not STOP_EVENT.is_set():
        for server in servers:
            if STOP_EVENT.is_set():
                break
            try:
                rt = ping3.ping(server, timeout=2)  # pyright: ignore[reportUnknownMemberType]
            except Exception as e:
                rt = None
                print(f"[!] Ping error for {server}: {e}")

            if rt is not None:
                print(f"[ping] {server} is UP ({rt*1000:.1f} ms)")
            else:
                print(f"[ping] {server} is DOWN! ALERT!")
        STOP_EVENT.wait(interval)

def main():
    args = get_arguments()

    # Graceful Ctrl+C
    def on_exit(_sig: int, _frame: FrameType | None) -> None:
        print("\n[*] Stopping...")
        STOP_EVENT.set()
        sys.exit(0)
    signal.signal(signal.SIGINT, on_exit)

    sound_player = None
    if not args.no_sound:
        try:
            sound_player = SoundPlayer()
            threading.Thread(target=play_sounds, args=(sound_player,), daemon=True).start()
        except Exception as e:
            print(f"[!] Sound disabled: {e}")

    if not args.no_ping:
        servers = ["google.com", "example.com", "localhost"]
        threading.Thread(target=ping_servers, args=(servers,), daemon=True).start()

    if args.target is None:
        print("Please specify a target. Example:")
        print("  python main.py -t 192.168.1.1/24")
        print("  python main.py -t 192.168.1.1/24 --no-sound")
        # Keep ping/sound running if no target
        try:
            while not STOP_EVENT.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        return

    scan_result = scan(args.target)
    print_result(scan_result)

    # Keep background threads alive for a bit, then exit
    print("\n[*] Press Ctrl+C to stop background monitors...")
    try:
        while not STOP_EVENT.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        STOP_EVENT.set()
        if sound_player:
            sound_player.close()

if __name__ == "__main__":
    main()