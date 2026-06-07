# WG SOC Lab

Lightweight SOC telemetry and alerting system for WireGuard servers using Linux Auditd.

## What it does

Monitors security-relevant events on a WireGuard VPN server and sends real-time Telegram alerts.

Targets:
- WireGuard configuration changes
- Private key access
- VPN process execution
- Administrative/system actions

## Architecture

Auditd → log files → Python parser → rule engine → Telegram notifications

## Severity mapping

- CRITICAL: private key access
- MEDIUM: configuration changes
- LOW: VPN command execution

## Example detection flow

WireGuard config modified  
→ auditd event generated  
→ parser processes log  
→ rule engine matches event  
→ Telegram alert sent

## Setup

Install dependencies:
pip install requests

Run manually:
python3 scripts/parser.py

## Systemd

Enable service:
systemctl enable --now parser.service

Service runs the parser continuously in background for real-time monitoring.

## Limitations

- no persistent storage
- no event correlation
- no deduplication
- rule-based detection only
