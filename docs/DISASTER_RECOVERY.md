# Homelab Disaster Recovery & Bare-Metal Reconstruction Runbook

Comprehensive step-by-step technical procedures to rebuild the entire homelab infrastructure, virtual switches, storage arrays, Docker application stacks, and traffic monitoring pipeline from scratch in the event of a total system or hardware catastrophe.

---

## 📌 Disaster Recovery Readiness Summary

| Component | Can Be Rebuilt from this Git Repository? | Reconstruction Mechanism |
| :--- | :---: | :--- |
| **Subnet Traffic Telemetry System** | ✅ **100% YES** | Automated deployment of daemon, scripts, parser, and systemd units |
| **ESXi Virtual Switching & SPAN** | ✅ **100% YES** | Declarative `esxcli` scripts restore `vSwitch0`, `vSwitch-Mirror`, port groups & VLAN 4095 |
| **TrueNAS Capture & Ingest Pipeline** | ✅ **100% YES** | Automated unnumbered vNIC setup, directory hierarchy & 10GB retention engine |
| **Docker Application Stacks (20+ Apps)**| ✅ **100% YES** | 10 Compose stacks (`config/docker/compose_stacks/`) rebuild all containers in minutes |
| **Homelab Services Portal** | ✅ **100% YES** | Pre-configured `services.json` and Nginx reverse proxy configuration |
| **VM Operating Systems & Data (VMDKs)** | ⚠️ **PARTIAL** | VM hardware specs & network maps are documented; requires OS install or VMDK backups |

---

## 🛠️ Phase 1: VMware ESXi Hypervisor Reconstruction

### 1.1 Base Hypervisor Installation
1. Install **VMware ESXi 8.0.3** (Build `24677879`) on physical host hardware.
2. Assign static management IP configuration:
   * **IPv4 Address**: `192.168.0.200`
   * **Subnet Mask**: `255.255.255.0`
   * **Default Gateway**: `192.168.0.1`
   * **DNS Server**: `192.168.0.1`
   * **Host Name**: `esxi-01.npcsolutions.co.za`

### 1.2 Virtual Switch & SPAN Port Group Restoration
Execute the following `esxcli` commands via SSH to recreate the exact production and promiscuous switching topology:

```bash
# 1. Enable Promiscuous Mode on Production Switch
esxcli network vswitch standard set -v vSwitch0 -c true -m true -f true

# 2. Create Promiscuous Port Group on vSwitch0
esxcli network vswitch standard portgroup add -p "Mirror-Network" -v vSwitch0
esxcli network vswitch standard portgroup policy security set -p "Mirror-Network" --allow-promiscuous true --allow-mac-change true --allow-forged-transmits true

# 3. Create Dedicated SPAN Virtual Switch
esxcli network vswitch standard add -v vSwitch-Mirror
esxcli network vswitch standard set -v vSwitch-Mirror -c true -m true -f true

# 4. Create VLAN 4095 SPAN Trunking Port Group
esxcli network vswitch standard portgroup add -p "SPAN-Monitoring-PG" -v vSwitch-Mirror
esxcli network vswitch standard portgroup set -p "SPAN-Monitoring-PG" -v 4095
esxcli network vswitch standard portgroup policy security set -p "SPAN-Monitoring-PG" --allow-promiscuous true --allow-mac-change true --allow-forged-transmits true
```

---

## 🗄️ Phase 2: TrueNAS SCALE Storage & Ingest Setup

### 2.1 Virtual Machine Deployment
* Deploy TrueNAS SCALE VM with 2 vNICs:
  * **NIC 1 (`ens192`)**: Connected to `VM Network` (`192.168.0.47/24`).
  * **NIC 2 (`ens224`)**: Connected to `Mirror-Network` (Promiscuous unnumbered capture NIC).
* Recreate ZFS Pool `pool1` and storage dataset `/mnt/pool1/network_traffic`.

### 2.2 Ingest Pipeline & Telemetry Restoration
Clone this Git repository directly on TrueNAS and deploy the background services:

```bash
# Clone repository
git clone https://github.com/chaminukambanje/networktraffic.git /tmp/networktraffic

# Copy pipeline scripts to ZFS pool
mkdir -p /mnt/pool1/network_traffic/{raw_pcaps,devices,scripts,logs}
cp /tmp/networktraffic/scripts/categorize_traffic.py /mnt/pool1/network_traffic/scripts/
cp /tmp/networktraffic/scripts/traffic_daemon.sh /mnt/pool1/network_traffic/scripts/
cp /tmp/networktraffic/scripts/dashboard_app.py /mnt/pool1/network_traffic/scripts/
chmod +x /mnt/pool1/network_traffic/scripts/*

# Install Systemd Daemons
sudo cp /tmp/networktraffic/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now subnet-traffic-monitor.service
sudo systemctl enable --now traffic-dashboard.service
```

---

## 🐳 Phase 3: Docker Application Host Reconstruction (`192.168.0.218`)

### 3.1 Base Host Provisioning
1. Provision an Ubuntu 24.04 / 26.04 VM (VM ID `107` on ESXi) with:
   * **vCPUs**: 8 Cores
   * **RAM**: 32 GB
   * **IP Address**: `192.168.0.218/24` (Gateway: `192.168.0.1`)
   * **Hostname**: `docker.npcsolutions.co.uk`
2. Install Docker Engine and Compose plugin:
```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
```

### 3.2 Instant Stack Deployment via Repository Stacks
Clone the Git repository and bring up all 10 container stacks:

```bash
git clone https://github.com/chaminukambanje/networktraffic.git /tmp/networktraffic

# 1. Homelab Services Launchpad & Portal (Port 80/8080)
mkdir -p /home/mbanjec/homelab-portal
cp /tmp/networktraffic/config/docker/compose_stacks/homelab-portal/docker-compose.yml /home/mbanjec/homelab-portal/
cp /tmp/networktraffic/config/docker/docker_services.json /home/mbanjec/homelab-portal/services.json
cp /tmp/networktraffic/config/docker/nginx.conf /home/mbanjec/homelab-portal/
docker compose -f /home/mbanjec/homelab-portal/docker-compose.yml up -d

# 2. Subnet Network Traffic Dashboard (Port 8500)
mkdir -p /opt/network-traffic-dashboard
cp /tmp/networktraffic/docker-compose.yml /opt/network-traffic-dashboard/
cp /tmp/networktraffic/Dockerfile /opt/network-traffic-dashboard/
cp /tmp/networktraffic/scripts/dashboard_app.py /opt/network-traffic-dashboard/app.py
docker compose -f /opt/network-traffic-dashboard/docker-compose.yml up -d --build

# 3. Monitoring Stack (Grafana :3002, Prometheus :9090, cAdvisor :8085, Node Exporter :9100)
mkdir -p /home/mbanjec/monitoring-stack
cp /tmp/networktraffic/config/docker/compose_stacks/monitoring-stack/docker-compose.yml /home/mbanjec/monitoring-stack/
docker compose -f /home/mbanjec/monitoring-stack/docker-compose.yml up -d

# 4. Security & SIEM Stack (Wazuh Dashboard :8443, Wazuh Manager, OpenSearch Indexer)
mkdir -p /home/mbanjec/wazuh-docker/single-node
cp /tmp/networktraffic/config/docker/compose_stacks/wazuh-single-node/docker-compose.yml /home/mbanjec/wazuh-docker/single-node/
docker compose -f /home/mbanjec/wazuh-docker/single-node/docker-compose.yml up -d

# 5. Remote Access (Guacamole Web RDP :8084 & :8086, WireGuard VPN :51821)
mkdir -p /home/mbanjec/ubuntu-rdp-web /home/mbanjec/unicf-rdp /home/mbanjec/wg-easy
cp /tmp/networktraffic/config/docker/compose_stacks/ubuntu-rdp-web/docker-compose.yml /home/mbanjec/ubuntu-rdp-web/
cp /tmp/networktraffic/config/docker/compose_stacks/unicf-rdp/docker-compose.yml /home/mbanjec/unicf-rdp/
cp /tmp/networktraffic/config/docker/compose_stacks/wg-easy/docker-compose.yml /home/mbanjec/wg-easy/
docker compose -f /home/mbanjec/ubuntu-rdp-web/docker-compose.yml up -d
docker compose -f /home/mbanjec/unicf-rdp/docker-compose.yml up -d
docker compose -f /home/mbanjec/wg-easy/docker-compose.yml up -d

# 6. Jasmin HPC & Business Applications (:8880-:8888, :8098)
mkdir -p /home/mbanjec/jasmin-cluster /home/mbanjec/fast-cash-uk-app /home/mbanjec/news-dashboard /home/mbanjec/cloudflare-ddns
cp /tmp/networktraffic/config/docker/compose_stacks/jasmin-cluster/docker-compose.yml /home/mbanjec/jasmin-cluster/
cp /tmp/networktraffic/config/docker/compose_stacks/fast-cash-uk-app/docker-compose.yml /home/mbanjec/fast-cash-uk-app/
cp /tmp/networktraffic/config/docker/compose_stacks/news-dashboard/docker-compose.yml /home/mbanjec/news-dashboard/
cp /tmp/networktraffic/config/docker/compose_stacks/cloudflare-ddns/docker-compose.yml /home/mbanjec/cloudflare-ddns/
docker compose -f /home/mbanjec/jasmin-cluster/docker-compose.yml up -d
docker compose -f /home/mbanjec/fast-cash-uk-app/docker-compose.yml up -d
docker compose -f /home/mbanjec/news-dashboard/docker-compose.yml up -d
docker compose -f /home/mbanjec/cloudflare-ddns/docker-compose.yml up -d
```

---

## 💻 Phase 4: Virtual Machine Reconstruction Map

Use [`config/esxi/vm_inventory.md`](../config/esxi/vm_inventory.md) and [`docs/DEVICE_INVENTORY.md`](DEVICE_INVENTORY.md) to reconstruct VMs with matching CPU, RAM, and static IPs:

| VM Name | OS / Template | vCPUs | RAM | Assigned Static IP | Role |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`UNICAF-2025-2026`** | Windows Server 2025 | 8 | 32 GB | `192.168.0.109` | Active Directory / Core Windows Server |
| **`sql`** | Windows Server / MS SQL 2022 | 8 | 32 GB | `192.168.0.237` | Microsoft SQL Database Server |
| **`BC-server`** | Windows Server 2022 | 4 | 16 GB | `192.168.0.39` | Microsoft Dynamics Business Central |
| **`login-01` / `login-02`**| CentOS 9 Stream | 4 | 16 GB | `192.168.0.131` / `.133` | Slurm HPC Cluster Login Gateways |
| **`node-01` to `node-06`** | CentOS 9 / Rocky Linux | 8 | 32 GB | `192.168.0.170`, `.53`, `.124`, `.227`, `.125`, `.146` | HPC Cluster Compute Nodes |
| **`booklore-server`** | CentOS 8 | 4 | 8 GB | `192.168.0.99` | Booklore Production Application |
| **`ubuntutest`** | Ubuntu 24.04 | 2 | 4 GB | `192.168.0.235` | Testing Environment VM |

---

## 🔒 Recommended Disaster Recovery Best Practices

To achieve **100% Zero-Loss Disaster Recovery**, supplement this Git repository with:
1. **Periodic VMDK Snapshots**: Store full ZFS VMDK backups on an external drive or secondary storage.
2. **Database Dumps**: Enable daily automated SQL `.bak` dumps to `/mnt/pool1/backups/`.
3. **TrueNAS Config Backup**: Save TrueNAS configuration `.tar` file periodically.
