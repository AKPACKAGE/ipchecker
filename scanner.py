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
]

def boot_animation():
    frames = [
        "[■□□□□□□□□□] Booting system...",
        "[■■□□□□□□□□] Loading modules...",
        "[■■■□□□□□□□] Initializing scanner...",
        "[■■■■□□□□□□] Connecting network...",
        "[■■■■■□□□□□] Preparing UI...",
        "[■■■■■■□□□□] Optimizing engine...",
        "[■■■■■■■□□□] Starting services...",
        "[■■■■■■■■□□] Almost ready...",
        "[■■■■■■■■■□] Final check...",
        "[■■■■■■■■■■] READY"
    ]

    for f in frames:
        sys.stdout.write("\r" + C.C + f)
        sys.stdout.flush()
        time.sleep(0.25)

    print("\n")

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
    print(C.Y + "     powered by mamad eini\n" + C.W)

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
    menu()
    c = input(C.Y + "\nSELECT > " + C.W)

    if c == "1":
        return ips

    elif c == "2":
        path = input("FILE PATH > ").strip()

        if os.path.exists(path):
            return [i.strip() for i in open(path).readlines() if i.strip()]

        print(C.R + "FILE NOT FOUND\n" + C.W)
        return []

    elif c == "3":
        return [i.strip() for i in input("IPS > ").split(",") if i.strip()]

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

def main():
    os.system("clear")
    boot_animation()
    banner()

    while True:
        run()
        input(C.Y + "\nPRESS ENTER TO RETURN MENU..." + C.W)

if __name__ == "__main__":
    main()
