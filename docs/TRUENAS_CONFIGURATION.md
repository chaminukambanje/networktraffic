# TrueNAS SCALE Setup & Deployment Runbook

## 1. Storage Dataset & Directory Hierarchy

On the TrueNAS server (`192.168.0.47`):

```bash
BASE_DIR="/mnt/pool1/network_traffic"

# Create directories
sudo mkdir -p "$BASE_DIR/raw_pcaps"
sudo mkdir -p "$BASE_DIR/devices"
sudo mkdir -p "$BASE_DIR/scripts"
sudo mkdir -p "$BASE_DIR/logs"

# Symlink to requested alternate folder name
sudo ln -sfn "$BASE_DIR" "/mnt/pool1/netsork traffice"

# Permissions
sudo chmod 777 "$BASE_DIR/raw_pcaps"
sudo chown -R truenas_admin:truenas_admin "$BASE_DIR"
```

---

## 2. Ingest Interface Setup

Bring up the capture interface `ens224` in promiscuous mode without assigning an IP address:

```bash
sudo ip link set ens224 up
sudo ip link set ens224 promisc on
```

---

## 3. Systemd Daemon Deployment

Install the systemd unit `/etc/systemd/system/subnet-traffic-monitor.service`:

```ini
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
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now subnet-traffic-monitor.service
sudo systemctl status subnet-traffic-monitor.service
```
