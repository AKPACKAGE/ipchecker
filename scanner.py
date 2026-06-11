import requests
from concurrent.futures import ThreadPoolExecutor
import time
import os
import sys
import threading

ips = [
    "1.1.1.1",
    "8.8.8.8",
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
