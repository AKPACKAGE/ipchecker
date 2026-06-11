import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
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
        "booting core system",
        "loading encryption layer",
        "initializing network stack",
        "spawning scan engine",
        "syncing modules"
    ]

    bar_len = 22

    for step in steps:
        for i in range(bar_len + 1):
            filled = "█" * i
            empty = "░" * (bar_len - i)
            percent = int((i / bar_len) * 100)

            sys.stdout.write(f"\r{step} [{filled}{empty}] {percent}%")
            sys.stdout.flush()
            time.sleep(0.03)

        print(" ✔")
        time.sleep(0.15)

    print("\nSYSTEM READY\n")
    time.sleep(0.3)

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

def run():
    ip_list = get_ip_list()
    if not ip_list:
        return

    stop = threading.Event()
    t = threading.Thread(target=animate, args=(stop,))
    t.start()

    clean = []
    total = len(ip_list)
    done = 0

    print(C.C + "\n╔════════════════════════════════════╗")
    print("║        LIVE IP DASHBOARD           ║")
    print("╚════════════════════════════════════╝" + C.W)

    print(C.B + f"TOTAL TARGETS: {total}\n" + C.W)

    print(C.C + "┌─────────┬──────────────┬────────┐")
    print("│ STATUS  │ IP           │ PING   │")
    print("├─────────┼──────────────┼────────┤" + C.W)

    with ThreadPoolExecutor(max_workers=25) as ex:
        futures = [ex.submit(check_ip, ip) for ip in ip_list]

        for f in as_completed(futures):
            ip, lat, status = f.result()
            done += 1

            if status == "OK":
                clean.append((ip, lat))
                icon = C.G + "ONLINE  " + C.W
            else:
                icon = C.R + "OFFLINE " + C.W

            ip_fixed = ip.ljust(12)
            ping_fixed = f"{lat}ms".ljust(6)

            print(f"│ {icon} │ {ip_fixed} │ {ping_fixed} │")

            percent = int((done / total) * 100)
            sys.stdout.write(C.Y + f"\rProgress: {percent}% ({done}/{total})" + C.W)
            sys.stdout.flush()

    stop.set()
    t.join()

    print(C.C + "\n└─────────┴──────────────┴────────┘" + C.W)

    clean.sort(key=lambda x: x[1])

    print(C.G + f"\n✔ CLEAN IPS FOUND: {len(clean)}" + C.W)

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
