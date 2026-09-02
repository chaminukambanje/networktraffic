# Homelab Subnet Traffic Monitoring, ESXi & Infrastructure Repository

Enterprise-grade automated network traffic capture, flow inspection, reverse DNS hostname resolution, real-time dashboard telemetry, and complete homelab infrastructure configuration management using VMware ESXi 8.0, TrueNAS SCALE, and Docker.

---

## 📌 Architecture Topology

```
[Physical Network & ESXi Virtual Machines]
              │ (Subnet Traffic: 192.168.0.0/24)
              ▼
┌────────────────────────────────────────────────────────────┐
│ VMware ESXi 8.0.3 Hypervisor (192.168.0.200)               │
│  [vSwitch0]                                                │
│   ├── PortGroup: VM Network (Production Virtual Machines)  │
│   └── PortGroup: Mirror-Network (Promiscuous Mode = Accept)│
│  [vSwitch-Mirror]                                          │
│   └── PortGroup: SPAN-Monitoring-PG (VLAN 4095 Trunk)      │
└─────────────────────────────┬──────────────────────────────┘
                              │ Mirrored Frames (SPAN)
                              ▼
┌────────────────────────────────────────────────────────────┐
│ TrueNAS SCALE Storage & Ingest Host (192.168.0.47)         │
│  ├── NIC 1 (ens192): Management Network                    │
│  └── NIC 2 (ens224): Mirror Ingest (Unnumbered Capture)    │
│            │                                               │
│            ▼                                               │
│   [subnet-traffic-monitor.service (30s Rolling PCAP)]      │
│            │                                               │
│            ▼                                               │
│   [categorize_traffic.py (Flow Classifier & DNS Resolver)] │
│            │                                               │
│            ▼                                               │
│   /mnt/pool1/network_traffic/devices/<DEVICE_IP>/          │
│    ├── summary.json    (Device metrics & resolved hostname)│
│    └── traffic_log.csv (Time-series session activity)      │
│            │                                               │
│            ▼ (Automatic 10GB Quota & Log Retention Engine) │
└─────────────────────────────┬──────────────────────────────┘
                              │ Telemetry REST API
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Docker Application Host (192.168.0.218)                    │
│  ├── Container: network-traffic-dashboard (Port 8500)      │
│  ├── Container: homelab-dashboard (Port 80 / 8080)         │
│  │     └── Tile: "Subnet Network Traffic Telemetry"        │
│  ├── Monitoring: Grafana (3002), Prometheus (9090), cAdvisor│
│  ├── Security: Wazuh SIEM SOC (8443), WireGuard VPN (51821)│
│  └── Remote Desktop: Guacamole Web RDP (Ubuntu & Windows)   │
└────────────────────────────────────────────────────────────┘
```

---

## 🌐 Quick Access Links

| Service | Endpoint | Description |
| :--- | :--- | :--- |
| **Homelab Hub Portal** | 👉 [http://192.168.0.218](http://192.168.0.218) | Central launchpad for all 20+ homelab services |
| **Docker Traffic Dashboard** | 👉 [http://192.168.0.218:8500](http://192.168.0.218:8500) | Live Subnet & Docker Telemetry Dashboard |
| **TrueNAS Direct Dashboard** | 👉 [http://192.168.0.47:8500](http://192.168.0.47:8500) | Direct TrueNAS Telemetry Backend & API |
| **Local Documentation Browser** | 👉 [http://localhost:8000](http://localhost:8000) | Markdown repository browser on local Mac |
| **GitHub Repository** | 👉 [github.com/chaminukambanje/networktraffic](https://github.com/chaminukambanje/networktraffic) | Master Git version control repository |

---

## 📂 Documentation & Configuration Map

### 1. Documentation Guides (`docs/` & `rebuild/`)
* [`rebuild/README.md`](rebuild/README.md): **Master Homelab Disaster Recovery & Rebuild Blueprint** (Complete scripts, configs, and multi-phase runbooks).
* [`docs/DISASTER_RECOVERY.md`](docs/DISASTER_RECOVERY.md): **Bare-Metal Disaster Recovery Runbook** & step-by-step restoration procedures.
* [`docs/ROUTER_CONFIGURATION.md`](docs/ROUTER_CONFIGURATION.md): Sky Broadband Hub (SR213) router, LAN/WAN, and Wi-Fi configuration.
* [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): Network topology, ESXi vSwitch layer, and ingest architecture.
* [`docs/DEVICE_INVENTORY.md`](docs/DEVICE_INVENTORY.md): Verified online homelab catalog (26 active devices) and pruned stale list.
* [`docs/ESXI_CONFIGURATION.md`](docs/ESXI_CONFIGURATION.md): Step-by-step ESXi port mirroring, vSwitch, and vNIC commands.
* [`docs/TRUENAS_CONFIGURATION.md`](docs/TRUENAS_CONFIGURATION.md): TrueNAS SCALE interface, ZFS pool, and daemon runbooks.
* [`docs/DOCKER_HOMELAB_CONFIG.md`](docs/DOCKER_HOMELAB_CONFIG.md): Docker container stacks, port maps, and homelab portal config.
* [`docs/DATA_STRUCTURE.md`](docs/DATA_STRUCTURE.md): JSON/CSV log schemas and the **10GB automated retention policy**.

### 2. Live Infrastructure Snapshots & Compose Stacks (`config/`)
* **Docker Compose Stacks**: [`config/docker/compose_stacks/`](config/docker/compose_stacks/) (Complete compose files for all 10 services including Wazuh, Guacamole, Jasmin, Monitoring, Portal, WireGuard).
* **ESXi Host**:
  * [`config/esxi/esxi_system_info.md`](config/esxi/esxi_system_info.md): Hardware, CPU, Memory, Datastores, and physical NICs.
  * [`config/esxi/vswitches.md`](config/esxi/vswitches.md): vSwitch0, vSwitch-Mirror, port groups, and VMkernel interfaces.
  * [`config/esxi/vm_inventory.md`](config/esxi/vm_inventory.md): Complete list of all registered virtual machines and power states.
* **Docker Server**:
  * [`config/docker/docker_containers.md`](config/docker/docker_containers.md): Running containers, networks, images, and system resources.
  * [`config/docker/docker_services.json`](config/docker/docker_services.json): Full catalog of services registered on the Homelab Portal.
  * [`config/docker/nginx.conf`](config/docker/nginx.conf): Nginx reverse proxy configuration for the portal.
* **TrueNAS Storage**:
  * [`config/truenas/zpool_layout.md`](config/truenas/zpool_layout.md): ZFS `pool1` topology, datasets, and storage utilization.

### 3. Core Software & Systemd Units
* [`scripts/categorize_traffic.py`](scripts/categorize_traffic.py): Binary PCAP packet parser, DNS resolver, and 10GB retention engine.
* [`scripts/traffic_daemon.sh`](scripts/traffic_daemon.sh): Continuous rolling 30s capture loop and quota enforcement.
* [`scripts/dashboard_app.py`](scripts/dashboard_app.py): Real-time web application and REST API server.
* [`Dockerfile`](Dockerfile) & [`docker-compose.yml`](docker-compose.yml): Production Docker container deployment.
* [`systemd/subnet-traffic-monitor.service`](systemd/subnet-traffic-monitor.service): Capture daemon systemd unit.
* [`systemd/traffic-dashboard.service`](systemd/traffic-dashboard.service): Web dashboard systemd unit.

