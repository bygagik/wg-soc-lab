#!/usr/bin/env python3
import time
import re
import requests

#TELEGRAM
BOT_TOKEN = "8958166758:AAEU2D9IEKvGcKXZrJMgCrb_yxNB72QnEAE"
CHAT_ID = "1160469785"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


#LOG FILE
LOG_FILE = "/var/log/audit/audit.log"

#EVENTS
EVENTS = {
    "vpn_config": "MEDIUM",
    "vpn_server_key": "CRITICAL",
    "vpn_exec": "LOW",
}


#PARSER
def parse(line):
    data = {}

    key = re.search(r'key="([^"]+)"', line)
    if key:
        data["key"] = key.group(1)

    exe = re.search(r'exe="([^"]+)"', line)
    if exe:
        data["exe"] = exe.group(1)

    comm = re.search(r'comm="([^"]+)"', line)
    if comm:
        data["comm"] = comm.group(1)

    name = re.search(r'name="([^"]+)"', line)
    if name:
        data["file"] = name.group(1)

    ts = re.search(r'audit\((\d+\.\d+)', line)
    if ts:
        data["ts"] = ts.group(1)

    return data


#ALERT
def alert(ev):
    key = ev.get("key")
    if not key:
        return

    severity = EVENTS.get(key, "INFO")

    msg = (
        f"[{severity}] SECURITY EVENT\n"
        f"Key: {key}\n"
    )

    if "file" in ev:
        msg += f"File: {ev['file']}\n"
    if "exe" in ev:
        msg += f"Exe: {ev['exe']}\n"
    if "comm" in ev:
        msg += f"Command: {ev['comm']}\n"
    if "ts" in ev:
        msg += f"Time: {ev['ts']}\n"

    print(msg)
    send_telegram(msg)


#LOG FOLLOW
def follow(file):
    file.seek(0, 2)

    while True:
        line = file.readline()
        if not line:
            time.sleep(0.2)
            continue

        ev = parse(line)
        alert(ev)


if __name__ == "__main__":
    print("[*] SOC parser started")

    with open(LOG_FILE) as f:
        follow(f)
