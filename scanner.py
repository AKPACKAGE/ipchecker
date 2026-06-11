import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os
import sys
import threading

class C:
    H = "\033[95m"
    B = "\033[94m"
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    W = "\033[0m"
    BOLD = "\033[1m"

ips = [
    "184.24.77.16",
    "184.24.77.42",
    "2.19.205.33",
    "2.19.205.27",
    "2.19.205.105",
    "23.201.248.171",
    "2.16.10.149",
    "2.16.2.27",
    "23.67.129.53",
    "104.76.220.168",
    "178.22.122.101",
    "185.137.25.214",
    "81.12.72.218",
    "185.142.158.162",
    "185.141.106.238",
    "5.144.129.174",
    "109.72.197.1",
    "80.191.243.226",
    "185.88.178.196",
    "81.91.145.2",
]

def banner():
    print(C.C + C.BOLD)
    print("""
██╗██████╗      ██████╗ ██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗
██║██╔══██╗    ██╔═══██╗██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗
██║██████╔╝    ██║   ██║██████╔╝    ██║     ███████║█████╗  ██║     ███████║█████╗  ██████╔╝
██║██╔═══╝     ██║   ██║██╔═══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔══██║██╔══╝  ██╔══██╗
██║██║         ╚██████╔╝██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██║███████╗██║  ██║
╚═╝╚═╝          ╚═════╝ ╚═╝          ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
""")
    print(C.G + "        IP CHECKER v2.0")
    print(C.Y + "        powered by mamad eini\n" + C.W)

def menu():
    print(C.C + "╔════════════════════════════╗")
    print("║ 1) Default IPs            ║")
    print("║ 2) Load from file         ║")
    print("║ 3) Manual input           ║")
    print("║ 4) Exit                   ║")
    print("╚════════════════════════════╝" + C.W)

def animate(stop_event):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(C.C + f"\r🔍 SCANNING {chars[i % len(chars)]} " + C.W)
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def check_ip(ip, timeout=5):
    try:
        start = time.time()
        requests.get(f"http://{ip}", timeout=timeout)
        latency = round((time.time() - start) * 1000)
        return (ip, latency, "OK")
    except:
        return (ip, 9999, "BAD")

def get_ip_list():
    banner()
    menu()

    c = input(C.Y + "\nSELECT > " + C.W).strip()

    if c == "1":
        print(C.G + "✔ Default IPs loaded\n" + C.W)
        return ips

    elif c == "2":
        path = input("FILE PATH > ").strip()

        if os.path.exists(path):
            data = [i.strip() for i in open(path).readlines() if i.strip()]
            print(C.G + f"✔ FILE LOADED ({len(data)} IPs)\n" + C.W)
            return data
        else:
            print(C.R + "❌ FILE NOT FOUND\n" + C.W)
            return []

    elif c == "3":
        data = [i.strip() for i in input("IPS > ").split(",") if i.strip()]
        print(C.G + f"✔ MANUAL INPUT LOADED ({len(data)} IPs)\n" + C.W)
        return data

    elif c == "4":
        print(C.R + "EXITING..." + C.W)
        exit()

    else:
        print(C.R + "INVALID OPTION\n" + C.W)
        return []

def print_table(results):
    results.sort(key=lambda x: x[1])

    print(C.C + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" RANK | STATUS | PING | IP")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━" + C.W)

    rank = 1
    for ip, lat, status in results:
        icon = "🟢" if status == "OK" else "🔴"
        print(f" {rank:>3}  | {icon} {status:<4} | {lat:>4}ms | {ip}")
        rank += 1

    print(C.C + "━━━━━━━━━━━━━━━━━━━━━━━━━━\n" + C.W)

def run():
    ip_list = get_ip_list()
    if not ip_list:
        return

    print(C.C + f"\n📡 TARGETS LOADED: {len(ip_list)}\n" + C.W)

    stop = threading.Event()
    t = threading.Thread(target=animate, args=(stop,))
    t.start()

    with ThreadPoolExecutor(max_workers=25) as ex:
        results = list(ex.map(check_ip, ip_list))

    stop.set()
    t.join()

    sys.stdout.write("\r" + " " * 60 + "\r")

    print_table(results)

    clean = [(ip, lat) for ip, lat, st in results if st == "OK"]
    clean.sort(key=lambda x: x[1])

    out = "/storage/emulated/0/Download/clean_ips.txt"

    try:
        with open(out, "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(C.G + f"💾 SAVED {len(clean)} CLEAN IPS -> DOWNLOADS\n" + C.W)
    except:
        with open("clean_ips.txt", "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(C.Y + "💾 SAVED LOCALLY\n" + C.W)

def main():
    while True:
        run()
        input(C.Y + "\nPRESS ENTER TO RETURN MENU..." + C.W)

if __name__ == "__main__":
    main()
