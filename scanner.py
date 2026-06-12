import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
import sys
import platform
import socket

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
    "178.22.122.101",
    "185.255.89.101",
    "185.141.106.238",
]

# ---------------- LOG ----------------
LOG_FILE = "scan_log.txt"

def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(msg + "\n")
    except:
        pass

# ---------------- ANIMATION ----------------
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
            time.sleep(0.02)

        print(" ✔")
        time.sleep(0.1)

    print("\nSYSTEM READY\n")

# ---------------- BANNER ----------------
def banner():
    print(C.C + C.BOLD)
    print("""
██╗██████╗      ██████╗ ██████╗
██║██╔══██╗    ██╔═══██╗██╔══██╗
██║██████╔╝    ██║   ██║██████╔╝
██║██╔═══╝     ██║   ██║██╔═══╝
██║██║         ╚██████╔╝██║
╚═╝╚═╝          ╚═════╝ ╚═╝
""")
    print(C.G + "        IP CHECKER v2.0")
    print(C.Y + "        powered by @AKPAC\n" + C.W)

# ---------------- MENU ----------------
def menu():
    print(C.C + "╔════════════════════════════╗")
    print("║ 1) Default IPs            ║")
    print("║ 2) Load from file         ║")
    print("║ 3) Manual input           ║")
    print("║ 4) Exit                   ║")
    print("╚════════════════════════════╝" + C.W)

# ---------------- HTTP CHECK ----------------
def check_ip(ip, timeout=5):
    try:
        start = time.time()
        requests.get(f"http://{ip}", timeout=timeout)
        latency = round((time.time() - start) * 1000)
        return (ip, latency, "OK")
    except:
        return (ip, 9999, "BAD")

# ---------------- FIXED TCP SCAN ----------------
def check_ports(ip):
    ports = [80, 443, 22]
    result = {}

    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            code = s.connect_ex((ip, p))

            if code == 0:
                result[p] = "OPEN"
            else:
                # تفاوت CLOSED و FILTERED خیلی دقیق نیست، ولی بهتر از قبله
                result[p] = "CLOSED"

            s.close()

        except:
            result[p] = "FILTERED"

    return result

# ---------------- GEO ----------------
def geo_ip(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        d = r.json()
        return f"{d.get('country','?')} | {d.get('isp','?')}"
    except:
        return "UNKNOWN"

# ---------------- ENHANCE ----------------
def enhance(result):
    ip, lat, status = result

    ports = check_ports(ip)
    geo = geo_ip(ip)

    log(f"{status} | {ip} | {lat}ms | ports:{ports} | {geo}")

    return (ip, lat, status, ports, geo)

# ---------------- SAVE PATH ----------------
def get_save_path():
    system = platform.system().lower()

    if "android" in system:
        return "/storage/emulated/0/Download/clean_ips.txt"
    elif "windows" in system:
        return os.path.join(os.environ.get("USERPROFILE", ""), "Desktop", "clean_ips.txt")
    else:
        return os.path.join(os.path.expanduser("~"), "clean_ips.txt")

# ---------------- INPUT ----------------
def get_ip_list():
    menu()
    c = input(C.Y + "\nSELECT > " + C.W).strip()

    if c == "1":
        return ips

    elif c == "2":
        path = input("FILE PATH > ").strip()
        if os.path.exists(path):
            return [i.strip() for i in open(path).readlines() if i.strip()]
        return []

    elif c == "3":
        return [i.strip() for i in input("IPS > ").split(",") if i.strip()]

    elif c == "4":
        exit()

    return []

# ---------------- RUN ----------------
def run():
    ip_list = get_ip_list()
    if not ip_list:
        return

    results = []
    total = len(ip_list)

    print(C.C + "\nLIVE DASHBOARD\n" + C.W)

    with ThreadPoolExecutor(max_workers=25) as ex:
        futures = [ex.submit(check_ip, ip) for ip in ip_list]

        done = 0

        for f in as_completed(futures):
            enhanced = enhance(f.result())
            results.append(enhanced)

            done += 1
            sys.stdout.write(C.Y + f"\rProgress: {int((done/total)*100)}% ({done}/{total})" + C.W)
            sys.stdout.flush()

    print("\n")

    results.sort(key=lambda x: x[1])

    clean = [(ip, lat) for ip, lat, status, _, _ in results if status == "OK"]
    clean.sort(key=lambda x: x[1])

    print(C.C + "╔════════════════════════════╗")
    print("║ STATUS | IP | PING | PORTS ║")
    print("╚════════════════════════════╝" + C.W)

    for ip, lat, status, ports, geo in results:
        color = C.G if status == "OK" else C.R

        print(color + f"{status} | {ip} | {lat}ms | {ports} | {geo}" + C.W)

    out = get_save_path()

    try:
        with open(out, "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(C.G + f"\n✔ SAVED: {out}")
    except:
        print(C.R + "SAVE ERROR")

    print(C.C + f"✔ LOG: {LOG_FILE}" + C.W)

# ---------------- MAIN ----------------
def main():
    startup_animation()
    banner()

    while True:
        run()
        input(C.Y + "\nPRESS ENTER..." + C.W)

if __name__ == "__main__":
    main()
