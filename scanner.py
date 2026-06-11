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

def load_ips_from_file(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def animate(stop_event):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r🔍 Scanning IPs {chars[i % len(chars)]}")
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

def get_ip_list():
    print("\n1) Default IPs")
    print("2) Load from file")
    print("3) Manual input")
    c = input("> ").strip()

    if c == "1":
        return ips
    elif c == "2":
        p = input("File path: ").strip()
        return load_ips_from_file(p) if os.path.exists(p) else ips
    elif c == "3":
        return [i.strip() for i in input("IPs: ").split(",") if i.strip()]
    return ips

def print_table(results):
    results.sort(key=lambda x: x[1])

    print("\n====================================")
    print("        FASTEST IP RESULTS")
    print("====================================")
    print(" RANK | STATUS   | LATENCY | IP")
    print("------------------------------------")

    rank = 1
    for ip, lat, status in results:
        if status == "OK":
            tag = "🟢"
        elif status == "TIMEOUT":
            tag = "🟡"
        else:
            tag = "🔴"

        print(f" {rank:>4} | {tag} {status:<6} | {lat:>6}ms | {ip}")
        rank += 1

    print("====================================\n")

def main():
    ip_list = get_ip_list()
    print(f"\nLoaded {len(ip_list)} IPs\n")

    stop = threading.Event()
    t = threading.Thread(target=animate, args=(stop,))
    t.start()

    with ThreadPoolExecutor(max_workers=25) as ex:
        results = list(ex.map(check_ip, ip_list))

    stop.set()
    t.join()
    sys.stdout.write("\r" + " " * 50 + "\r")

    print_table(results)

    clean = [r for r in results if r[2] == "OK"]
    clean.sort(key=lambda x: x[1])

    out = "/storage/emulated/0/Download/clean_ips.txt"
    try:
        with open(out, "w") as f:
            for ip, lat, _ in clean:
                f.write(f"{ip} | {lat}ms\n")
        print(f"Saved -> {out}")
    except:
        with open("clean_ips.txt", "w") as f:
            for ip, lat, _ in clean:
                f.write(f"{ip} | {lat}ms\n")
        print("Saved -> local file")

if __name__ == "__main__":
    main()
