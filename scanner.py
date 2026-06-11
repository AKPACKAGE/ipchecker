import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os
import sys
import threading
import platform

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
]

def startup_animation():
    steps = [
        "Initializing system",
        "Loading modules",
        "Preparing scanner engine",
        "Syncing network interface",
        "Starting IP Checker"
    ]

    chars = ["|", "/", "-", "\\"]
    for step in steps:
        for i in range(8):
            sys.stdout.write(f"\r{step} {chars[i % 4]}")
            sys.stdout.flush()
            time.sleep(0.1)
        print(f"\r{step} ✔")
    print("\n")
    time.sleep(0.5)

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

def get_save_path():
    system = platform.system().lower()

    if "android" in system:
        return "/storage/emulated/0/Download/clean_ips.txt"
    elif "windows" in system:
        return os.path.join(os.environ.get("USERPROFILE", ""), "Desktop", "clean_ips.txt")
    else:
        return os.path.join(os.path.expanduser("~"), "clean_ips.txt")

def get_ip_list():
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
        print(C.R + "❌ FILE NOT FOUND\n" + C.W)
        return []

    elif c == "3":
        data = [i.strip() for i in input("IPS > ").split(",") if i.strip()]
        print(C.G + f"✔ MANUAL INPUT LOADED ({len(data)} IPs)\n" + C.W)
        return data

    elif c == "4":
        print(C.R + "EXITING..." + C.W)
        exit()

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

    stop = threading.Event()
    t = threading.Thread(target=animate, args=(stop,))
    t.start()

    with ThreadPoolExecutor(max_workers=25) as ex:
        results = list(ex.map(check_ip, ip_list))

    stop.set()
    t.join()

    print_table(results)

    clean = [(ip, lat) for ip, lat, st in results if st == "OK"]
    clean.sort(key=lambda x: x[1])

    out = get_save_path()

    try:
        with open(out, "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(C.G + f"💾 SAVED: {out}" + C.W)
    except:
        with open("clean_ips.txt", "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(C.Y + "💾 SAVED LOCALLY" + C.W)

def main():
    startup_animation()
    banner()
    while True:
        run()
        input(C.Y + "\nPRESS ENTER TO RETURN MENU..." + C.W)

if __name__ == "__main__":
    main()
