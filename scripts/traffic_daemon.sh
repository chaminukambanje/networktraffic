#!/bin/bash
INTERFACE="ens224"
BASE_DIR="/mnt/pool1/network_traffic"
RAW_DIR="/mnt/pool1/network_traffic/raw_pcaps"
SCRIPTS_DIR="/mnt/pool1/network_traffic/scripts"
LOG_FILE="/mnt/pool1/network_traffic/logs/monitor.log"

/usr/sbin/ip link set $INTERFACE up
/usr/sbin/ip link set $INTERFACE promisc on

mkdir -p "$RAW_DIR" "$SCRIPTS_DIR" "/mnt/pool1/network_traffic/logs" "/mnt/pool1/network_traffic/devices"
chmod 777 "$RAW_DIR"

echo "[$(date)] Starting Subnet Traffic Capture Daemon on $INTERFACE..." >> "$LOG_FILE"

# Start tcpdump in background (rotating every 30 seconds, maintaining max 50 files)
/usr/bin/tcpdump -Z root -i $INTERFACE -n -s 0 -G 30 -W 50 -w "$RAW_DIR/capture_%Y%m%d_%H%M%S.pcap" >> "$LOG_FILE" 2>&1 &
TCPDUMP_PID=$!
echo "tcpdump started with PID $TCPDUMP_PID" >> "$LOG_FILE"

# Background Analysis Loop
while kill -0 $TCPDUMP_PID 2>/dev/null; do
    sleep 10
    /usr/bin/python3 "$SCRIPTS_DIR/categorize_traffic.py" >> "$LOG_FILE" 2>&1
done
