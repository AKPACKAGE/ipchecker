import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys
import socket
import platform
import os

class C:
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

LOG_FILE = "scan_log.txt"

def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(msg + "\n")
    except:
        pass

def startup_animation():
    steps = [
        "booting core system",
        "loading security modules",
        "initializing network stack",
        "spawning scan engine",
        "warming up dashboard engine"
    ]

    bar_len = 26

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

def banner():
    print(C.C + C.BOLD)
    print(r"""
██╗██████╗  ██████╗  ██████╗  ███████╗███████╗███████╗██████╗
██║██╔══██╗██╔═══██╗██╔════╝  ██╔════╝██╔════╝██╔════╝██╔══██╗
██║██████╔╝██║   ██║██║  ███╗█████╗  ███████╗█████╗  ██████╔╝
██║██╔═══╝ ██║   ██║██║   ██║██╔══╝  ╚════██║██╔══╝  ██╔══██╗
██║██║     ╚██████╔╝╚██████╔╝███████╗███████║███████╗██║  ██║
╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
""")
    print(C.G + "        IP CHECKER v3.0 ENTERPRISE")
    print(C.Y + "        powered by @AKPAC\n" + C.W)

def check_http(ip, timeout=5):
    try:
        start = time.time()
        requests.get(f"http://{ip}", timeout=timeout)
        latency = round((time.time() - start) * 1000)
        return (ip, latency, "OK")
    except:
        return (ip, 9999, "BAD")

def retry_request(ip, retries=2):
    for _ in range(retries):
        try:
            r = requests.get(f"http://{ip}", timeout=3)
            return True
        except:
            time.sleep(0.2)
    return False

def tcp_scan(ip):
    ports = [80, 443, 22, 8080]
    result = {}

    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            code = s.connect_ex((ip, p))

            if code == 0:
                result[p] = "OPEN"
            else:
                result[p] = "CLOSED"

            s.close()
        except:
            result[p] = "FILTERED"

    return result

def geo_lookup(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        d = r.json()
        return {
            "country": d.get("country", "?"),
            "isp": d.get("isp", "?"),
            "city": d.get("city", "?")
        }
    except:
        return {"country": "?", "isp": "?", "city": "?"}

def classify_status(lat, ports):
    if lat < 300 and ports.get(80) == "OPEN":
        return "FAST-ONLINE"
    elif lat < 1000:
        return "SLOW-ONLINE"
    else:
        return "UNSTABLE"

def enhance(result):
    ip, lat, status = result

    ports = tcp_scan(ip)
    geo = geo_lookup(ip)
    retry = retry_request(ip)

    final_status = classify_status(lat, ports)

    log(f"{ip} | {lat}ms | {final_status} | {ports} | {geo} | retry:{retry}")

    return (ip, lat, final_status, ports, geo, retry)

def box(title, lines):
    width = 80
    print(C.C + "┌" + "─" * (width - 2) + "┐" + C.W)
    print(C.C + "│ " + title.ljust(width - 4) + " │" + C.W)
    print(C.C + "├" + "─" * (width - 2) + "┤" + C.W)

    for l in lines:
        l = str(l)[:width - 4]
        print(C.C + "│ " + l.ljust(width - 4) + " │" + C.W)

    print(C.C + "└" + "─" * (width - 2) + "┘" + C.W)

def run():
    results = []

    print(C.Y + "\nENTERPRISE SCAN STARTED...\n" + C.W)

    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = [ex.submit(check_http, ip) for ip in ips]

        for f in as_completed(futures):
            results.append(enhance(f.result()))

    results.sort(key=lambda x: x[1])

    http_box = []
    tcp_box = []
    geo_box = []
    status_box = []

    for ip, lat, status, ports, geo, retry in results:
        http_box.append(f"{status} | {ip} | {lat}ms | retry:{retry}")
        tcp_box.append(f"{ip} | 80:{ports[80]} | 443:{ports[443]} | 22:{ports[22]}")
        geo_box.append(f"{ip} | {geo['country']} | {geo['isp']}")
        status_box.append(f"{ip} | CLASS:{status}")

    box("HTTP LAYER", http_box)
    box("TCP SCAN LAYER", tcp_box)
    box("GEO INTELLIGENCE", geo_box)
    box("STATUS ENGINE", status_box)

def main():
    startup_animation()
    banner()

    while True:
        run()
        input(C.Y + "\nPRESS ENTER TO RESCAN ENTERPRISE..." + C.W)

if __name__ == "__main__":
    main()
