# Subnet Traffic Monitoring & Device Categorization System

Enterprise-grade automated network traffic capture, flow inspection, and per-device activity categorization using VMware ESXi Promiscuous Port Mirroring and TrueNAS ZFS Storage.

---

## 📌 Overview

This repository documents the end-to-end implementation of an automated subnet traffic monitoring system. The system ingests mirrored subnet traffic directly into a TrueNAS storage pool via an ESXi Promiscuous Virtual Switch and automatically parses, categorizes, and logs per-device network activity.

```
[Physical Network & ESXi VMs]
              │ (Subnet Traffic)
              ▼
┌──────────────────────────────────────────────┐
│ VMware ESXi Host (192.168.0.200)             │
│                                              │
│  [vSwitch0]                                  │
│   ├── PortGroup: VM Network                  │
│   └── PortGroup: Mirror-Network (Promiscuous)│
│                                              │
│  [vSwitch-Mirror]                            │
│   └── PortGroup: SPAN-Monitoring-PG (VLAN 4095)
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │ TrueNAS Server (192.168.0.47)           │ │
│  │  ├── NIC 1 (ens192): Management Network │ │
│  │  └── NIC 2 (ens224): Mirror Ingest      │ │
│  │            │ (Unnumbered / Promiscuous) │ │
│  │            ▼                            │ │
│  │    [tcpdump Ring Buffer Service]        │ │
│  │            ▼                            │ │
│  │    [Python Flow Analyzer Worker]        │ │
│  │            ▼                            │ │
│  │    /mnt/pool1/network_traffic/devices/  │ │
│  └─────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

---

## 🚀 Key Features

* **Zero Hardware Overhead**: Utilizes ESXi virtual switches with promiscuous mode to capture both virtual machine and physical uplink traffic.
* **Non-Disruptive Capture**: TrueNAS capture NIC (`ens224`) is unnumbered (no IP assigned), preventing IP conflict and securing the capture interface.
* **Lightweight Ring Buffers**: Uses 30-second rolling `.pcap` slices to prevent memory exhaustion and disk lockups.
* **Autonomous Packet Inspection**: Pure-Python binary PCAP parser decoding Ethernet, 802.1Q VLAN tags, IPv4, IPv6, TCP, UDP, ICMP, DNS, and application layer protocols.
* **Hierarchical Storage**: Creates per-device directories (`/mnt/pool1/network_traffic/devices/<device_ip>/`) containing detailed CSV session logs and JSON activity rollups.
* **Systemd Integration**: Runs as a resilient `subnet-traffic-monitor.service` with automatic crash recovery.

---

## 📂 Repository Contents

* [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): System architecture and data flow.
* [`docs/ESXI_CONFIGURATION.md`](docs/ESXI_CONFIGURATION.md): Step-by-step ESXi vSwitch & vNIC commands.
* [`docs/TRUENAS_CONFIGURATION.md`](docs/TRUENAS_CONFIGURATION.md): TrueNAS interface, daemon, and systemd deployment.
* [`docs/DATA_STRUCTURE.md`](docs/DATA_STRUCTURE.md): Log schemas, folder organization, and JSON structure.
* [`scripts/categorize_traffic.py`](scripts/categorize_traffic.py): Core binary PCAP parser and device aggregator.
* [`scripts/traffic_daemon.sh`](scripts/traffic_daemon.sh): Continuous capture rotation and execution loop.
* [`systemd/subnet-traffic-monitor.service`](systemd/subnet-traffic-monitor.service): Systemd service unit.
