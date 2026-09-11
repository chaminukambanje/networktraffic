#!/usr/bin/env python3
"""
WhatsApp Alert Webhook Bridge for Grafana & Prometheus Alertmanager.
Receives webhook notifications, formats alert payloads with emojis and metrics,
and dispatches critical alerts to WhatsApp via WAHA (WhatsApp HTTP API).
"""

import os
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

PORT = int(os.environ.get("BRIDGE_PORT", "9097"))
WAHA_URLS = [
    os.environ.get("WAHA_URL", "http://host.docker.internal:8095/api/sendText"),
    "http://127.0.0.1:8095/api/sendText",
    "http://192.168.0.218:8095/api/sendText"
]
WAHA_API_KEY = os.environ.get("WAHA_API_KEY", "npc_whatsapp_secret_key_2026")
RECIPIENT = os.environ.get("ALERT_RECIPIENT", "447565297807@c.us")
GRAFANA_URL = os.environ.get("GRAFANA_URL", "http://192.168.0.218:3002/d/hardware-and-storage-health")

def send_whatsapp(text):
    payload = {
        "session": "default",
        "chatId": RECIPIENT,
        "text": text
    }
    data = json.dumps(payload).encode("utf-8")
    
    for url in WAHA_URLS:
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "X-Api-Key": WAHA_API_KEY,
                    "User-Agent": "Grafana-WhatsApp-Alert-Bridge/1.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                if resp.status in (200, 201):
                    logging.info("Successfully dispatched alert to %s via %s", RECIPIENT, url)
                    return True
        except Exception as e:
            logging.warning("Failed sending to %s: %s", url, e)
            continue
    logging.error("All WAHA endpoints failed to deliver message.")
    return False

def format_grafana_alert(data):
    status = data.get("status", "firing").upper()
    alerts = data.get("alerts", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S BST")
    
    if status == "RESOLVED":
        msg = [
            "✅ *[ALERT RESOLVED]* ✅",
            "━━━━━━━━━━━━━━━━━━━━━",
            f"⏱️ *Resolved At*: {timestamp}"
        ]
        for a in alerts:
            labels = a.get("labels", {})
            ann = a.get("annotations", {})
            name = labels.get("alertname", "Homelab Alert")
            host = labels.get("host", labels.get("instance", "Dell PowerEdge Host"))
            msg.append(f"🟢 *Alert*: {name}")
            msg.append(f"🖥️ *Host*: {host}")
            if "summary" in ann:
                msg.append(f"📝 *Summary*: {ann['summary']}")
            msg.append("━━━━━━━━━━━━━━━━━━━━━")
        return "\n".join(msg)

    msg = [
        "🚨 *[CRITICAL HOMELAB ALERT]* 🚨",
        "━━━━━━━━━━━━━━━━━━━━━",
        f"⏱️ *Triggered At*: {timestamp}",
        "🔥 *Status*: FIRING"
    ]
    
    for idx, a in enumerate(alerts, 1):
        labels = a.get("labels", {})
        ann = a.get("annotations", {})
        vals = a.get("values", {})
        
        alertname = labels.get("alertname", "Unknown Alert")
        severity = labels.get("severity", "critical").upper()
        host = labels.get("host", labels.get("instance", "esxi-01.npcsolutions.co.za"))
        component = labels.get("name", labels.get("datastore", labels.get("device", "System")))
        
        summary = ann.get("summary", "Critical threshold reached or hardware failing")
        desc = ann.get("description", "")
        
        msg.append(f"\n⚠️ *Item #{idx}*: {alertname}")
        msg.append(f"🏷️ *Severity*: {severity}")
        msg.append(f"🖥️ *Host*: {host}")
        msg.append(f"📊 *Component/Sensor*: {component}")
        
        if vals:
            val_strs = [f"{k}: {v}" for k, v in vals.items()]
            joined_vals = ", ".join(val_strs)
            msg.append(f"📈 *Current Values*: {joined_vals}")
            
        msg.append(f"📝 *Summary*: {summary}")
        if desc:
            msg.append(f"ℹ️ *Details*: {desc}")
            
    msg.append("\n━━━━━━━━━━━━━━━━━━━━━")
    msg.append(f"🔗 *Dashboard*: {GRAFANA_URL}")
    return "\n".join(msg)

class AlertWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/healthz", "/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "whatsapp-alert-bridge"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8", errors="ignore")
        
        if self.path == "/test":
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S BST")
            test_msg = (
                "🧪 *[TEST] WhatsApp Alert Bridge Verification*\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "✅ Webhook receiver is healthy and communicating with WAHA.\n"
                f"⏱️ Timestamp: {ts}\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "Alert notifications for Hardware, Temperature, and Disk Failures are active!"
            )
            success = send_whatsapp(test_msg)
            code = 200 if success else 500
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"delivered": success}).encode())
            return
            
        if self.path in ("/webhook", "/alert", "/"):
            try:
                data = json.loads(post_body) if post_body else {}
                logging.info("Received alert webhook with %d alerts", len(data.get("alerts", [])))
                formatted = format_grafana_alert(data)
                success = send_whatsapp(formatted)
                self.send_response(200 if success else 502)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"delivered": success, "alerts_count": len(data.get("alerts", []))}).encode())
            except Exception as e:
                logging.error("Error processing webhook: %s", e)
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), AlertWebhookHandler)
    logging.info("WhatsApp Alert Bridge listening on port %d (Forwarding to %s)...", PORT, RECIPIENT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
