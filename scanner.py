import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os
import sys
import threading

ips = [
    "184.24.77.16",
    "184.24.77.42",
    "2.19.205.33",
    "2.19.205.27",
    "2.19.205.105",
]

def load_ips_from_file(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def animate(stop_event):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r🔍 Scanning {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def check_ip(ip, timeout=5):
    try:
        start = time.time()
        requests.get(f"http://{ip}", timeout=timeout)
        latency = round((time.time() - start) * 1000)
        return (ip, latency, "OK")
    except requests.exceptions.Timeout:
        return (ip, 9999, "TIMEOUT")
    except requests.exceptions.ConnectionError:
        return (ip, 9999, "BLOCKED")
    except:
        return (ip, 9999, "ERROR")

def print_table(results):
    results.sort(key=lambda x: x[1])

    print("\n======================================")
    print("        IP SCANNER RESULTS")
    print("======================================")
    print(" RANK | STATUS   | LATENCY | IP")
    print("--------------------------------------")

    for i, (ip, lat, status) in enumerate(results, 1):
        icon = "🟢" if status == "OK" else "🟡" if status == "TIMEOUT" else "🔴"
        print(f" {i:>4} | {icon} {status:<6} | {lat:>6}ms | {ip}")

    print("======================================\n")

def get_ip_list():
    print("\n╔════════════════════════════╗")
    print("║        IP SCANNER          ║")
    print("╠════════════════════════════╣")
    print("║ 1) Default IPs            ║")
    print("║ 2) Load from file         ║")
    print("║ 3) Manual input           ║")
    print("║ 4) Exit                   ║")
    print("╚════════════════════════════╝")

    c = input("\nSelect > ").strip()

    if c == "1":
        return ips

    elif c == "2":
        path = input("📂 File path: ").strip()

        if os.path.exists(path):
            loaded = load_ips_from_file(path)
            print(f"📥 Loaded {len(loaded)} IPs from file")
            return loaded
        else:
            print("❌ File not found!")
            return []

    elif c == "3":
        raw = input("✍️ Enter IPs (comma separated): ")
        return [i.strip() for i in raw.split(",") if i.strip()]

    elif c == "4":
        print("👋 Exiting...")
        exit()

    else:
        print("⚠️ Invalid choice")
        return []

def run_scanner():
    ip_list = get_ip_list()

    if not ip_list:
        print("⚠️ No IPs loaded\n")
        return

    print(f"\n📋 Loaded {len(ip_list)} IPs\n")

    stop = threading.Event()
    t = threading.Thread(target=animate, args=(stop,))
    t.start()

    with ThreadPoolExecutor(max_workers=25) as ex:
        results = list(ex.map(check_ip, ip_list))

    stop.set()
    t.join()
    sys.stdout.write("\r" + " " * 50 + "\r")

    print_table(results)

    clean = [(ip, lat) for ip, lat, st in results if st == "OK"]
    clean.sort(key=lambda x: x[1])

    out = "/storage/emulated/0/Download/clean_ips.txt"

    try:
        with open(out, "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(f"💾 Saved: {out}")
    except:
        with open("clean_ips.txt", "w") as f:
            for ip, lat in clean:
                f.write(f"{ip} | {lat}ms\n")
        print("💾 Saved locally")

def main():
    while True:
        run_scanner()
        input("\n🔁 Press Enter to return to menu...")

if __name__ == "__main__":
    main()
