import random
import time
import numpy as np
import pyaudio
import threading
import ping3
try:
    import scapy.all as scapy
    import optparse
except ImportError:
    print("[+] packages not installed ")
    print("try-> pip install scapy")
    print("pip install optparse-pretty")


class SoundPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()

    def play_sound(self, frequency, duration, volume=1.0):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * frequency * t)
        audio_data *= volume

        stream = self.p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=sample_rate,
                             output=True)

        stream.write(audio_data.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()

    def play_sound_async(self, frequency, duration, volume=1.0):
        threading.Thread(target=self.play_sound, args=(frequency, duration, volume)).start()


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t",
                      "--target",
                      dest="target",
                      help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]

    clients_list = []
    for element in answered_list:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(clients_dict)

    return clients_list


def print_result(result_list):
    print("IP\t\t\tMAC ADDRESS\n..........................................................................")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


def play_sounds(sound_player):
    sounds = {
        "raindrops": {"min_freq": 100, "max_freq": 300, "min_duration": 0.1, "max_duration": 0.5},
        "rustling_leaves": {"min_freq": 500, "max_freq": 1500, "min_duration": 0.2, "max_duration": 0.7},
        "chirping_birds": {"min_freq": 1000, "max_freq": 5000, "min_duration": 0.2, "max_duration": 0.4}
    }

    while True:
        selected_sounds = list(sounds.keys())
        random.shuffle(selected_sounds)

        for sound_choice in selected_sounds:
            sound_params = sounds[sound_choice]
            frequency = random.uniform(sound_params["min_freq"], sound_params["max_freq"])
            duration = random.uniform(sound_params["min_duration"], sound_params["max_duration"])
            volume = random.uniform(0.5, 1.0)

            print(f"Playing {sound_choice}...")
            sound_player.play_sound_async(frequency, duration, volume)
            time.sleep(random.uniform(0.1, 0.5))


def ping_servers(servers):
    while True:
        for server in servers:
            response_time = ping3.ping(server)
            if response_time is not None:
                print(f"{server} is up (Response Time: {response_time} ms)")
            else:
                print(f"{server} is down! ALERT!")

        time.sleep(60)


def main():
    sound_player = SoundPlayer()
    threading.Thread(target=play_sounds, args=(sound_player,)).start()

    servers_to_monitor = ["google.com", "example.com", "localhost"]
    threading.Thread(target=ping_servers, args=(servers_to_monitor,)).start()

    options = get_arguments()
    if options.target is None:
        print("Please specify a target IP range.")
        return

    scan_result = scan(options.target)
    print_result(scan_result)


if __name__ == "__main__":
    main()