#!/bin/bash
# Subnet Network Traffic Capture & Retention Daemon
# Automatically captures raw packets, categorizes traffic flows, and enforces
# a strict 10GB maximum storage quota for logs and PCAPs.

INTERFACE="ens224"
BASE_DIR="/mnt/pool1/network_traffic"
RAW_DIR="$BASE_DIR/raw_pcaps"
SCRIPTS_DIR="$BASE_DIR/scripts"
LOGS_DIR="$BASE_DIR/logs"
LOG_FILE="$LOGS_DIR/monitor.log"
MAX_STORAGE_KB=10485760 # 10 GB in Kilobytes (10 * 1024 * 1024)

# Ensure capture interface is up and promiscuous
/usr/sbin/ip link set $INTERFACE up 2>/dev/null || true
/usr/sbin/ip link set $INTERFACE promisc on 2>/dev/null || true

mkdir -p "$RAW_DIR" "$SCRIPTS_DIR" "$LOGS_DIR" "$BASE_DIR/devices"
chmod 777 "$RAW_DIR" "$LOGS_DIR" "$BASE_DIR/devices" 2>/dev/null || true

echo "[$(date)] Starting Subnet Traffic Capture Daemon (Retention Quota: 10GB)..." >> "$LOG_FILE"

# Function to enforce 10GB log retention ceiling
enforce_log_quota() {
    # 1. Truncate monitor.log if it exceeds 50MB
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE_KB=$(du -k "$LOG_FILE" | cut -f1)
        if [ "$LOG_SIZE_KB" -gt 51200 ]; then
            tail -n 10000 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
            echo "[$(date)] monitor.log rotated (kept last 10,000 lines)." >> "$LOG_FILE"
        fi
    fi

    # 2. Check total directory size
    TOTAL_USAGE_KB=$(du -sk "$BASE_DIR" 2>/dev/null | cut -f1)
    if [ "$TOTAL_USAGE_KB" -gt "$MAX_STORAGE_KB" ]; then
        echo "[$(date)] WARNING: Storage usage (${TOTAL_USAGE_KB} KB) exceeded 10GB limit (${MAX_STORAGE_KB} KB). Running purge..." >> "$LOG_FILE"
        
        # Delete raw pcaps older than 1 hour or oldest first
        find "$RAW_DIR" -type f -name "*.pcap" -mmin +30 -delete 2>/dev/null || true
        
        # If still over quota, prune oldest 50% of lines in all CSV logs
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
            echo "[$(date)] Pruned CSV history to restore 10GB quota." >> "$LOG_FILE"
        fi
    fi
}

# Start rolling tcpdump capture (30-second slices, max 50 ring files)
/usr/bin/tcpdump -Z root -i $INTERFACE -n -s 0 -G 30 -W 50 -w "$RAW_DIR/capture_%Y%m%d_%H%M%S.pcap" >> "$LOG_FILE" 2>&1 &
TCPDUMP_PID=$!
echo "[$(date)] tcpdump started with PID $TCPDUMP_PID" >> "$LOG_FILE"

# Background Analysis & Log Quota Loop
while kill -0 $TCPDUMP_PID 2>/dev/null; do
    sleep 10
    /usr/bin/python3 "$SCRIPTS_DIR/categorize_traffic.py" >> "$LOG_FILE" 2>&1
    enforce_log_quota
done
