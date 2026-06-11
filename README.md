# ⚡ IP CHECKER v2.0

A fast, multi-threaded IP scanning tool built for speed, simplicity, and clean results.

Powered by **mamad eini**

---

## 🚀 Overview

IP CHECKER is a lightweight Python tool that scans a list of IP addresses, checks their availability, measures latency, and exports clean results automatically.

Designed for:
- Network testing
- IP validation
- Fast bulk scanning
- Learning multithreading in Python

---

## ✨ Features

- ⚡ Multi-threaded scanning (fast performance)
- 📡 Real-time scanning
- 🟢 Clean vs 🔴 Blocked detection
- 📊 Latency measurement (ms)
- 📁 Load IPs from file
- ⌨️ Manual IP input mode
- 💾 Auto-save clean IPs to file

---

## 🧠 How It Works

The tool sends HTTP requests to each IP address and evaluates:

- Response success → Clean IP ✅
- Connection failure → Blocked IP ❌
- Timeout → Slow or unstable IP ⚠️

Then it ranks results by latency.

---

## 📦 Installation

```bash
sudo apt update && sudo apt install python3 python3-pip git -y
```

```bash
pip install request
```

```bash
git clone https://github.com/AKPACKAGE/ipchecker.git  
```

```bash
cd ipchecker
```

```bash
pip install -r requirements.txt  
```

---

## ▶️ Usage

```bash
python scanner.py  
```

---

## 📂 Input Options

When running the tool, you can choose:

1. Default built-in IP list  
2. Load IPs from a file  
3. Manual IP input  

---

## 💾 Output

Clean IPs are automatically saved to:

/storage/emulated/0/Download/clean_ips.txt  

Fallback:  
clean_ips.txt  

---

## ⚙️ Requirements

- Python 3.x
- requests  

---

## 🧩 Tech Stack

- Python 🐍  
- Requests  
- ThreadPoolExecutor  
- ANSI Terminal UI  

---

## 🧠 Notes

- Optimized for Android (Termux)  
- Works on Linux & Windows  
- Best performance with stable internet connection  

---

## 👤 Author

Built with focus and chaos by:

mamad eini  

---

## ⚠️ Disclaimer

This tool is for educational and testing purposes only.  
Do not use it for unauthorized scanning.

---

## ⭐ Support

If you like this project:

- Star the repo  
- Fork it 
-    ⚡
