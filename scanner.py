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

def clear_line():
    sys.stdout.write("\r" + " " * 100 + "\r")

def boot():
    steps = ["init core", "load net engine", "sync ports", "start scanner", "ready"]
    for s in steps:
        for i in range(20):
            bar = "█" * i + "░" * (20 - i)
            sys.stdout.write(f"\r{s} [{bar}] {i*5}%")
            sys.stdout.flush()
            time.sleep(0.02)
        print(" ✔")
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
    print(C.G + "        IP CHECKER v4 HYBRID")
    print(C.Y + "        powered by @AKPAC\n" + C.W)

def http_check(ip):
    try:
        t = time.time()
        requests.get(f"http://{ip}", timeout=4)
        return ip, int((time.time() - t) * 1000), "OK"
    except:
        return ip, 9999, "BAD"

def tcp_scan(ip):
    ports = [80, 443, 22]
    res = {}
    for p in ports:
        s = socket.socket()
        s.settimeout(1)
        res[p] = "OPEN" if s.connect_ex((ip, p)) == 0 else "CLOSED"
        s.close()
    return res

def geo(ip):
    try:
        d = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        return f"{d.get('country','?')} | {d.get('isp','?')}"
    except:
        return "UNKNOWN"

def render_box(title, rows):
    width = 85
    print(C.C + "┌" + "─"*(width-2) + "┐")
    print("│ " + title.ljust(width-4) + " │")
    print("├" + "─"*(width-2) + "┤")
    for r in rows:
        print("│ " + str(r)[:width-4].ljust(width-4) + " │")
    print("└" + "─"*(width-2) + "┘" + C.W)

def run():
    results = []
    print(C.Y + "\nLIVE SCANNING...\n" + C.W)

    with ThreadPoolExecutor(max_workers=40) as ex:
        futures = [ex.submit(http_check, ip) for ip in ips]

        for i, f in enumerate(as_completed(futures)):
            ip, lat, status = f.result()
            tcp = tcp_scan(ip)
            g = geo(ip)

            results.append((ip, lat, status, tcp, g))

            clear_line()
            print(f"{C.C}progress {i+1}/{len(ips)}{C.W}", end="")

    print("\n")

    results.sort(key=lambda x: x[1])

    http_box = []
    tcp_box = []
    geo_box = []

    for ip, lat, status, tcp, g in results:
        http_box.append(f"{status} | {ip} | {lat}ms")
        tcp_box.append(f"{ip} | 80:{tcp[80]} | 443:{tcp[443]} | 22:{tcp[22]}")
        geo_box.append(f"{ip} | {g}")

    render_box("HTTP LAYER", http_box)
    render_box("TCP LAYER", tcp_box)
    render_box("GEO LAYER", geo_box)

def main():
    boot()
    banner()
    while True:
        run()
        input(C.Y + "\nPRESS ENTER TO RESCAN..." + C.W)

if __name__ == "__main__":
    main()
