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
    "185.200.232.49",
    "23.202.138.125",
    "185.255.89.101",
    "62.3.41.131",
    "185.13.230.155",
    "37.255.243.44",
    "194.5.205.51",
    "5.160.68.233",
    "178.173.190.222",
    "85.133.193.54",
    "185.8.175.249",
    "185.50.37.52",
    "92.123.106.90",
    "92.123.102.160",
    "104.103.72.80",
    "96.16.248.159",
    "104.89.170.140",
    "184.86.103.158",
    "72.246.28.215",
    "23.73.2.75",
    "184.51.133.123",
    "88.221.168.204",
    "88.221.169.205",
    "96.16.122.137",
    "23.72.248.210",
    "2.18.190.27",
    "23.58.223.224",
    "23.58.223.171",
    "184.24.77.25",
    "96.16.249.11",
    "2.23.154.99",
    "96.16.249.12",
    "23.55.161.38",
    "95.101.137.34",
    "23.58.223.225",
    "185.208.174.167",
    "185.208.175.228",
    "2.23.170.80",
    "95.101.35.74",
    "95.101.35.91",
    "2.23.168.254",
    "2.23.168.144",
    "2.23.168.47",
    "2.21.2.104",
    "2.23.168.213",
    "2.23.168.96",
    "2.23.168.174",
    "63.141.252.203",
    "185.255.91.60",
    "185.200.232.8",
    "185.200.232.9",
    "185.200.232.11",
    "185.200.232.16",
    "185.200.232.17",
    "185.200.232.19",
    "185.200.232.24",
    "185.200.232.25",
    "185.200.232.26",
    "185.200.232.34",
    "185.200.232.40",
    "185.200.232.42",
    "185.200.232.43",
    "185.200.232.56",
    "185.200.232.57",
    "185.200.232.58",
    "185.200.232.64",
    "185.200.232.65",
    "185.200.232.66",
    "185.200.232.67",
]


def load_ips_from_file(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def animate(stop_event):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r🔍 Scanning... {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def check_ip(ip, timeout=5):
    result = {"ip": ip, "status": "unknown", "latency": None}
    try:
        start = time.time()
        requests.get(f"http://{ip}", timeout=timeout)
        latency = round((time.time() - start) * 1000)
        result["status"] = "✅ Clean"
        result["latency"] = f"{latency}ms"
    except requests.exceptions.ConnectionError:
        result["status"] = "❌ Blocked"
    except requests.exceptions.Timeout:
        result["status"] = "⏱️ Timeout"
    except Exception:
        result["status"] = "⚠️ Error"
    return result

def get_ip_list():
    print("\n📌 Select Input Mode:")
    print("1) Default IPs")
    print("2) Load from file")
    print("3) Manual input")

    choice = input("\n> ").strip()

    if choice == "1":
        return ips

    elif choice == "2":
        path = input("📂 Enter file path: ").strip()
        if os.path.exists(path):
            return load_ips_from_file(path)
        else:
            print("❌ File not found! Using default IPs.")
            return ips

    elif choice == "3":
        raw = input("✍️ Enter IPs (comma separated): ")
        return [ip.strip() for ip in raw.split(",") if ip.strip()]

    else:
        print("⚠️ Invalid choice, using default IPs.")
        return ips

def main():
    output_path = "/storage/emulated/0/Download/clean_ips.txt"

    ip_list = get_ip_list()
    print(f"\n📋 Loaded {len(ip_list)} IPs\n")

    stop_event = threading.Event()
    t = threading.Thread(target=animate, args=(stop_event,))
    t.start()

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_ip, ip_list))

    stop_event.set()
    t.join()
    sys.stdout.write("\r" + " " * 40 + "\r")

    clean_ips = []

    for r in results:
        print(f"{r['status']} | {r['ip']} | {r.get('latency', '-')}")
        if "Clean" in r["status"]:
            clean_ips.append(r["ip"])

    print(f"\n✅ Clean IPs: {len(clean_ips)}")

    try:
        with open(output_path, "w") as f:
            f.write("\n".join(clean_ips))
        print(f"💾 Saved to Downloads/clean_ips.txt")
    except Exception:
        fallback = "clean_ips.txt"
        with open(fallback, "w") as f:
            f.write("\n".join(clean_ips))
        print(f"💾 Saved locally as clean_ips.txt")


if __name__ == "__main__":
    main()
