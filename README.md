# IP Checker

A lightweight Python tool for checking IP reachability and response latency using multithreading.

It scans a list of IPs, detects their status, and saves reachable ones automatically.

---

## Features

- Fast multithreaded scanning (ThreadPoolExecutor)
- IP status detection (Clean / Blocked / Timeout)
- Latency measurement in milliseconds
- Supports default IPs, file input, and manual input
- Simple CLI interface
- Auto-save results

---

## How it works

The tool sends HTTP requests to each IP and measures response time. Based on the response, it classifies IPs as:

- Clean (reachable)
- Blocked (connection error)
- Timeout
- Error

---

## Installation

## 1. Clone the repository
```bash
git clone https://github.com/AKPACKAGE/ipchecker.git
```

## 2. Enter the project directory
```bash
cd ipchecker
```

## 3. Install dependencies
```bash
pip install requests
```

## Usage

```bash
python scanner.py
```

---

## Input Modes

When you run the script, you can choose:

1. Default IPs (built-in list)
2. Load IPs from a file
3. Manual input (comma-separated)

---

## Output Example

```text
✅ Clean | 1.1.1.1 | 34ms
❌ Blocked | 8.8.8.8 | -
⏱️ Timeout | 4.4.4.4 | -
```

---

## Saved Results

Clean IPs are saved to:

/storage/emulated/0/Download/clean_ips.txt

If not accessible:

clean_ips.txt (project directory)

---

## Requirements

requests

---

## Notes

- Built for Termux and Python environments
- Uses up to 20 concurrent workers for faster scanning
- Lightweight and easy to modify
```
