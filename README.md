# WG SOC Lab

Lightweight SOC telemetry and alerting system for WireGuard servers using Linux Auditd.

## What it does

Monitors security-relevant events and sends Telegram alerts in real time.

Targets:

- WireGuard config changes
- Private key access
- VPN execution
- Admin/system actions


## Architecture

Auditd → log → Python parser → rule engine → Telegram notifier


## Severity mapping

- CRITICAL: private key access
- MEDIUM: config changes
- LOW: VPN command execution

## Run

pip install requests
python3 scripts/parser.py

## Systemd

systemctl enable --now parser.service

## Limitations

- no storage
- no correlation
- no deduplication
- rule-based only
