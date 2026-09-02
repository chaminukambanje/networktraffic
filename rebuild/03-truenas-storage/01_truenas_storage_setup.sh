#!/bin/bash
# ==============================================================================
# TrueNAS SCALE ZFS Storage & Ingest Daemon Provisioning Script
# Target Host: 192.168.0.47 (truenas.local)
# ==============================================================================
set -e

BASE_DIR="/mnt/pool1/network_traffic"
CAPTURE_IF="ens224"

echo "=== [1/5] Creating Storage Directories ==="
mkdir -p "$BASE_DIR/raw_pcaps"
mkdir -p "$BASE_DIR/scripts"
mkdir -p "$BASE_DIR/logs"
mkdir -p "$BASE_DIR/devices"
chmod -R 777 "$BASE_DIR"

echo "=== [2/5] Configuring Unnumbered Promiscuous Capture Interface ($CAPTURE_IF) ==="
ip link set "$CAPTURE_IF" up
ip link set "$CAPTURE_IF" promisc on
# Ensure no IP address is assigned to keep capture stealthy and conflict-free
ip addr flush dev "$CAPTURE_IF"

echo "=== [3/5] Deploying Traffic Capture Daemon Script ==="
cat << 'EOF_DAEMON' > "$BASE_DIR/scripts/traffic_daemon.sh"
#!/bin/bash
INTERFACE="ens224"
BASE_DIR="/mnt/pool1/network_traffic"
RAW_DIR="$BASE_DIR/raw_pcaps"
SCRIPTS_DIR="$BASE_DIR/scripts"
LOGS_DIR="$BASE_DIR/logs"
LOG_FILE="$LOGS_DIR/monitor.log"
MAX_STORAGE_KB=10485760 # 10 GB retention ceiling

ip link set $INTERFACE up 2>/dev/null || true
ip link set $INTERFACE promisc on 2>/dev/null || true
mkdir -p "$RAW_DIR" "$SCRIPTS_DIR" "$LOGS_DIR" "$BASE_DIR/devices"

enforce_log_quota() {
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE_KB=$(du -k "$LOG_FILE" | cut -f1)
        if [ "$LOG_SIZE_KB" -gt 51200 ]; then
            tail -n 10000 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
        fi
    fi
    TOTAL_USAGE_KB=$(du -sk "$BASE_DIR" 2>/dev/null | cut -f1)
    if [ "$TOTAL_USAGE_KB" -gt "$MAX_STORAGE_KB" ]; then
        find "$RAW_DIR" -type f -name "*.pcap" -mmin +30 -delete 2>/dev/null || true
        TOTAL_USAGE_KB=$(du -sk "$BASE_DIR" 2>/dev/null | cut -f1)
        if [ "$TOTAL_USAGE_KB" -gt "$MAX_STORAGE_KB" ]; then
            for csv_file in $(find "$BASE_DIR" -type f -name "*.csv"); do
                TOTAL_LINES=$(wc -l < "$csv_file")
                if [ "$TOTAL_LINES" -gt 5000 ]; then
                    HEAD_LINE=$(head -n 1 "$csv_file")
                    tail -n 2500 "$csv_file" > "${csv_file}.tmp"
                    echo "$HEAD_LINE" > "$csv_file"
                    cat "${csv_file}.tmp" >> "$csv_file"
                    rm -f "${csv_file}.tmp"
                fi
            done
        fi
    fi
}

/usr/bin/tcpdump -Z root -i $INTERFACE -n -s 0 -G 30 -W 50 -w "$RAW_DIR/capture_%Y%m%d_%H%M%S.pcap" >> "$LOG_FILE" 2>&1 &
TCPDUMP_PID=$!

while kill -0 $TCPDUMP_PID 2>/dev/null; do
    sleep 10
    /usr/bin/python3 "$SCRIPTS_DIR/categorize_traffic.py" >> "$LOG_FILE" 2>&1
    enforce_log_quota
done
EOF_DAEMON
chmod +x "$BASE_DIR/scripts/traffic_daemon.sh"

echo "=== [4/5] Installing Systemd Services ==="
cat << 'EOF_SERVICE1' > /etc/systemd/system/subnet-traffic-monitor.service
[Unit]
Description=Subnet Network Traffic Capture & Categorization Daemon
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash /mnt/pool1/network_traffic/scripts/traffic_daemon.sh
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF_SERVICE1

cat << 'EOF_SERVICE2' > /etc/systemd/system/traffic-dashboard.service
[Unit]
Description=Subnet & Docker Network Traffic Dashboard
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /mnt/pool1/network_traffic/scripts/dashboard_app.py
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF_SERVICE2

echo "=== [5/5] Reloading and Enabling Systemd Services ==="
systemctl daemon-reload
systemctl enable --now subnet-traffic-monitor.service
systemctl enable --now traffic-dashboard.service

echo "TrueNAS SCALE Rebuild & Storage Provisioning Complete!"
