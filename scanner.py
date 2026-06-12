import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys
import socket

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

def startup_animation():
    steps = [
        "booting core system",
        "loading modules",
        "initializing network stack",
        "spawning scan engine",
        "warming up dashboard"
    ]

    bar_len = 24

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
    print(C.G + "        IP CHECKER v2.0")
    print(C.Y + "        powered by @AKPAC\n" + C.W)

def check_ip(ip, timeout=5):
    try:
        start = time.time()
        requests.get(f"http://{ip}", timeout=timeout)
        latency = round((time.time() - start) * 1000)
        return (ip, latency, "OK")
    except:
        return (ip, 9999, "BAD")

def check_ports(ip):
    ports = [80, 443, 22]
    result = {}

    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            if s.connect_ex((ip, p)) == 0:
                result[p] = "OPEN"
            else:
                result[p] = "CLOSED"

            s.close()
        except:
            result[p] = "FILTERED"

    return result

def geo_ip(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        d = r.json()
        return f"{d.get('country','?')} | {d.get('isp','?')}"
    except:
        return "UNKNOWN"

def enhance(result):
    ip, lat, status = result
    ports = check_ports(ip)
    geo = geo_ip(ip)
    return (ip, lat, status, ports, geo)

def box(title, lines):
    width = 75
    print(C.C + "┌" + "─" * (width - 2) + "┐" + C.W)
    print(C.C + "│ " + title.ljust(width - 4) + " │" + C.W)
    print(C.C + "├" + "─" * (width - 2) + "┤" + C.W)

    for l in lines:
        l = str(l)[:width - 4]
        print(C.C + "│ " + l.ljust(width - 4) + " │" + C.W)

    print(C.C + "└" + "─" * (width - 2) + "┘" + C.W)

def run():
    results = []
    print(C.Y + "\nSCANNING TARGETS...\n" + C.W)

    with ThreadPoolExecutor(max_workers=25) as ex:
        futures = [ex.submit(check_ip, ip) for ip in ips]

        for f in as_completed(futures):
            results.append(enhance(f.result()))

    results.sort(key=lambda x: x[1])

    http_box = []
    tcp_box = []
    geo_box = []

    for ip, lat, status, ports, geo in results:
        http_box.append(f"{status} | {ip} | {lat}ms")
        tcp_box.append(f"{ip} | 80:{ports[80]} | 443:{ports[443]} | 22:{ports[22]}")
        geo_box.append(f"{ip} | {geo}")

    box("HTTP STATUS", http_box)
    box("TCP PORT SCAN", tcp_box)
    box("GEO LOCATION", geo_box)

def main():
    startup_animation()
    banner()

    while True:
        run()
        input(C.Y + "\nPRESS ENTER TO RESCAN..." + C.W)

if __name__ == "__main__":
    main()
