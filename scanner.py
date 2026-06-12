import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
import sys
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
"178.22.122.101",
"178.22.122.101",
"185.255.89.101",
"178.22.122.101",
"178.22.122.101",
"178.22.122.101",
"185.255.89.101",
"185.141.106.238",
"62.3.41.131",
"178.22.122.101",
"185.142.158.162",
"185.141.106.238",
"185.141.106.238",
"5.144.129.174",
"185.141.106.238",
"185.255.89.101",
"185.13.230.155",
"185.141.106.238",
"185.141.106.238",
"5.144.129.174",
"5.144.129.174",
"185.141.106.238",
"185.142.158.162",
"185.142.158.162",
"62.3.41.131",
"62.3.41.131",
"185.141.106.238",
"185.50.37.52",
"185.13.230.155",
"5.144.129.174",
"5.144.129.174",
"185.142.158.162",
"185.142.158.162",
"109.72.197.1",
"185.13.230.155",
"80.191.243.226",
"80.191.243.226",
"194.5.205.51",
"37.255.243.44",
"80.191.243.226",
"80.191.243.226",
"109.72.197.1",
"80.191.243.226",
"80.191.243.226",
"109.72.197.1",
"109.72.197.1",
"109.72.197.1",
"5.160.68.233",
"23.67.129.53",
"178.173.190.222",
"185.200.232.49",
"185.200.232.49",
"185.200.232.49",
"185.200.232.49",
"85.133.193.54",
"185.8.175.249",
"2.22.151.4",
"23.67.253.11",
"23.67.253.24",
"23.67.253.55",
"23.67.253.77",
"23.67.253.101",
"23.67.253.120",
"23.53.35.146",
"23.53.35.158",
"23.53.35.171",
"23.53.35.182",
"23.53.35.194",
"23.53.35.207",
"184.26.163.12",
"184.26.163.24",
"184.26.163.38",
"184.26.163.51",
"184.26.163.66",
"184.26.163.79",
"2.16.186.20",
"2.16.186.31",
"2.16.186.44",
"2.16.186.58",
"2.16.186.69",
"2.16.186.81",
"23.195.81.72",
"23.195.81.84",
"23.195.81.96",
"23.195.81.108",
"104.124.148.191",
"104.124.148.203",
"23.32.5.18",
"23.32.5.44",
"23.32.5.71",
"23.32.5.96",
"23.32.5.118",
"23.32.5.141",
"23.32.5.167",
"23.32.5.193",
"23.32.5.214",
"23.32.5.236",
"96.16.97.82",
"96.16.97.104",
"96.16.97.126",
"96.16.97.148",
"96.16.97.169",
"96.16.97.191",
"184.50.87.22",
"184.50.87.44",
"184.50.87.66",
"184.50.87.88",
"92.122.123.128",
"2.19.204.87",
"2.19.204.137",
"2.19.204.144",
"2.19.204.145",
"2.19.204.170",
"2.19.204.184",
"2.19.204.185",
"2.19.204.202",
"2.19.204.210",
"138.201.54.122",
"2.22.151.4",
"2.22.151.9",
"2.22.151.12",
"2.22.151.13",
"2.22.151.15",
"2.22.151.17",
"2.22.151.20",
"2.22.151.22",
"2.22.151.23",
"2.22.151.32",
"2.22.151.36",
"2.22.151.37",
"2.22.151.39",
"2.22.151.47",
"2.22.151.51",
"2.22.151.53",
"2.22.151.54",
"2.22.151.58",
"2.22.151.60",
"2.22.151.62",
"2.22.151.135",
"2.22.151.138",
"2.22.151.139",
"2.22.151.141",
"2.22.151.142",
"2.22.151.143",
"2.22.151.144",
"2.22.151.146",
"2.22.151.149",
"2.22.151.150",
"2.22.151.151",
"2.22.151.152",
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
    print(C.Y + "        powered by @AKPAC\n" + C.W)

def menu():
    print(C.C + "╔════════════════════════════╗")
    print("║ 1) Default IPs            ║")
    print("║ 2) Load from file         ║")
    print("║ 3) Manual input           ║")
    print("║ 4) Exit                   ║")
    print("╚════════════════════════════╝" + C.W)

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
            print(C.G + f"✔ FILE LOADED ({len(data)})\n" + C.W)
            return data
        print(C.R + "❌ FILE NOT FOUND\n" + C.W)
        return []

    elif c == "3":
        data = [i.strip() for i in input("IPS > ").split(",") if i.strip()]
        print(C.G + f"✔ MANUAL INPUT LOADED ({len(data)})\n" + C.W)
        return data

    elif c == "4":
        print(C.R + "EXITING..." + C.W)
        exit()

    return []

def run():
    ip_list = get_ip_list()
    if not ip_list:
        return

    results = []
    total = len(ip_list)

    print(C.C + "\n╔════════════════════════════════════╗")
    print("║        LIVE IP DASHBOARD           ║")
    print("╚════════════════════════════════════╝" + C.W)

    print(C.B + f"TOTAL TARGETS: {total}\n" + C.W)

    sys.stdout.write("\r" + " " * 80 + "\r")
    print()

    print(C.C + "┌─────────┬──────────────┬────────┐")
    print("│ STATUS  │ IP           │ PING   │")
    print("├─────────┼──────────────┼────────┤" + C.W)

    with ThreadPoolExecutor(max_workers=25) as ex:
        futures = [ex.submit(check_ip, ip) for ip in ip_list]

        done = 0

        for f in as_completed(futures):
            results.append(f.result())
            done += 1

            percent = int((done / total) * 100)
            sys.stdout.write(C.Y + f"\rProgress: {percent}% ({done}/{total})" + C.W)
            sys.stdout.flush()

    print()

    results.sort(key=lambda x: x[1])

    clean = [(ip, lat) for ip, lat, status in results if status == "OK"]
    clean.sort(key=lambda x: x[1])

    for ip, lat, status in results:
        if status == "OK":
            tag = "ONLINE "
            color = C.G
        else:
            tag = "OFFLINE"
            color = C.R

        ip_show = ip[:15].ljust(15)
        ping_show = f"{lat}ms".ljust(6)

        row = f"{tag} | {ip_show} | {ping_show}"
        space = 54 - len(row)
        if space < 0:
            space = 0

        print(color + "│ " + row + " " * space + "│" + C.W)

    print(C.C + "└─────────┴──────────────┴────────┘" + C.W)

    print(C.G + f"\n✔ CLEAN IPS: {len(clean)}" + C.W)

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
        input(C.Y + "\nPRESS ENTER TO CONTINUE..." + C.W)

if __name__ == "__main__":
    main()
