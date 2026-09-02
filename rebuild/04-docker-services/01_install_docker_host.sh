#!/bin/bash
# ==============================================================================
# Docker Host Rebuild & Container Stack Deployment Script
# Target Host: 192.168.0.218 (docker.npcsolutions.co.uk)
# ==============================================================================
set -e

echo "=== [1/4] Installing Docker Engine & Dependencies ==="
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release nfs-common

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose

echo "=== [2/4] Mounting TrueNAS Network Storage Volume ==="
mkdir -p /mnt/pool1/network_traffic
if ! grep -q "192.168.0.47:/mnt/pool1/network_traffic" /etc/fstab; then
    echo "192.168.0.47:/mnt/pool1/network_traffic /mnt/pool1/network_traffic nfs ro,defaults,_netdev 0 0" >> /etc/fstab
fi
mount -a 2>/dev/null || true

echo "=== [3/4] Deploying Homelab Docker Compose Stack ==="
mkdir -p /opt/homelab-stacks/traffic-telemetry
cd /opt/homelab-stacks/traffic-telemetry

cat << 'EOF_COMPOSE' > docker-compose.yml
version: '3.8'

services:
  network-traffic-dashboard:
    image: python:3.11-slim
    container_name: network-traffic-dashboard
    restart: unless-stopped
    ports:
      - "8500:8500"
    volumes:
      - /mnt/pool1/network_traffic:/mnt/network_traffic:ro
      - /opt/homelab-stacks/traffic-telemetry/dashboard_app.py:/app/dashboard_app.py:ro
    working_dir: /app
    command: python3 dashboard_app.py
    environment:
      - PORT=8500
      - DATA_DIR=/mnt/network_traffic
EOF_COMPOSE

echo "=== [4/4] Starting Docker Stack ==="
docker compose up -d

echo "Docker Services Rebuild Completed Successfully!"
