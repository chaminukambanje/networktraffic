# Subnet Traffic Monitoring & Device Categorization System

Enterprise-grade automated network traffic capture, flow inspection, reverse DNS hostname resolution, and real-time dashboard telemetry using VMware ESXi Promiscuous Port Mirroring, TrueNAS ZFS Storage, and Docker.

---

## 📌 Overview

This repository documents the end-to-end implementation of an automated subnet traffic monitoring system. The system ingests mirrored subnet traffic directly into a TrueNAS storage pool via an ESXi Promiscuous Virtual Switch, automatically parses and categorizes network flows with reverse DNS hostname resolution, and serves a live interactive dashboard across the homelab network.

```
[Physical Network & ESXi VMs]
              │ (Subnet Traffic)
              ▼
┌────────────────────────────────────────────────────────────┐
│ VMware ESXi Host (192.168.0.200)                           │
│  [vSwitch0]                                                │
│   ├── PortGroup: VM Network (Production)                   │
│   └── PortGroup: Mirror-Network (Promiscuous Mode = ON)    │
│  [vSwitch-Mirror]                                          │
│   └── PortGroup: SPAN-Monitoring-PG (VLAN 4095 Trunk)      │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ TrueNAS SCALE Storage (192.168.0.47)                       │
│  ├── NIC 1 (ens192): Management Network                    │
│  └── NIC 2 (ens224): Mirror Ingest (Unnumbered Capture)    │
│            │                                               │
│            ▼                                               │
│   [subnet-traffic-monitor.service (30s Rolling PCAP)]      │
│            │                                               │
│            ▼                                               │
│   [categorize_traffic.py Flow & DNS Name Classifier]       │
│            │                                               │
│            ▼                                               │
│   /mnt/pool1/network_traffic/devices/<DEVICE_IP>/          │
│    ├── summary.json    (Device metrics & resolved hostname)│
│    └── traffic_log.csv (Time-series session activity)      │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼ Telemetry API
┌────────────────────────────────────────────────────────────┐
│ Docker Server (192.168.0.218)                              │
│  ├── Container: network-traffic-dashboard (Port 8500)      │
│  └── Homelab Portal: homelab-dashboard (Port 80 / 8080)     │
│        └── Tile: "Subnet Network Traffic Telemetry"        │
└────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Capabilities

* **Zero Hardware Overhead**: Utilizes ESXi virtual switches with promiscuous mode to capture virtual machine and physical uplink traffic.
* **Non-Disruptive Capture**: TrueNAS capture NIC (`ens224`) is unnumbered (no IP assigned), preventing IP conflicts and securing the capture interface.
* **Reverse DNS Hostname Resolution**: Automatically maps IP addresses to local homelab hostnames (`docker.npcsolutions.co.uk`, `esxi-01`, `truenas.local`, `skysr213.home`, `chaminukas-mbp.home`) and external CDN/DNS endpoints.
* **Lightweight Ring Buffers**: Uses 30-second rolling `.pcap` slices to prevent memory exhaustion and disk lockups.
* **Autonomous Packet Inspection**: Pure-Python binary PCAP parser decoding Ethernet, 802.1Q VLAN tags, IPv4, IPv6, TCP, UDP, ICMP, DNS, and application layer protocols.
* **Live Interactive WebApp**: Modern Tailwind CSS dashboard with Chart.js visualization, search filters, and real-time 5-second auto-refresh.
* **Homelab Portal Integration**: Integrated as a primary tile on the Docker host Homelab Services Launchpad (`http://192.168.0.218`).

---

## 🌐 Endpoints & Access

| Service | Endpoint | Description |
| :--- | :--- | :--- |
| **Docker Traffic Dashboard** | `http://192.168.0.218:8500` | Primary containerized dashboard on Docker host |
| **TrueNAS Direct Dashboard** | `http://192.168.0.47:8500` | Direct backend telemetry dashboard on TrueNAS |
| **Homelab Hub Portal** | `http://192.168.0.218` | Unified homelab dashboard with Telemetry tile |
| **Local Repository Browser** | `http://localhost:8000` | Local web server for project documentation |

---

## 📂 Repository Contents

* [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): System architecture and network topology.
* [`docs/ESXI_CONFIGURATION.md`](docs/ESXI_CONFIGURATION.md): Step-by-step ESXi vSwitch & vNIC commands.
* [`docs/TRUENAS_CONFIGURATION.md`](docs/TRUENAS_CONFIGURATION.md): TrueNAS interface, daemon, and systemd deployment.
* [`docs/DATA_STRUCTURE.md`](docs/DATA_STRUCTURE.md): Log schemas, folder organization, and JSON structure.
* [`scripts/categorize_traffic.py`](scripts/categorize_traffic.py): Core binary PCAP parser and DNS aggregator.
* [`scripts/traffic_daemon.sh`](scripts/traffic_daemon.sh): Continuous capture rotation and execution loop.
* [`scripts/dashboard_app.py`](scripts/dashboard_app.py): Real-time web dashboard server and REST API.
* [`Dockerfile`](Dockerfile): Docker container definition for the dashboard.
* [`docker-compose.yml`](docker-compose.yml): Compose stack for deploying to Docker host.
* [`systemd/subnet-traffic-monitor.service`](systemd/subnet-traffic-monitor.service): Capture daemon service unit.
* [`systemd/traffic-dashboard.service`](systemd/traffic-dashboard.service): Dashboard systemd service unit.
