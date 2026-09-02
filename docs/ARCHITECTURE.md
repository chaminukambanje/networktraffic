# System Architecture & Technical Specifications

## 1. Network Topology

* **Subnet**: `192.168.0.0/24`
* **ESXi Hypervisor**: `192.168.0.200` (VMware ESXi 8.0.3, build 24677879)
* **TrueNAS Server**: `192.168.0.47` (TrueNAS SCALE 26.0.0, Linux Kernel 6.18)
* **Storage Dataset**: `pool1` (`/mnt/pool1/network_traffic` and `/mnt/pool1/netsork traffice`)

---

## 2. Ingest Architecture

### ESXi Switching Layer
1. **`vSwitch0`** (Standard Switch):
   * Uplinks: `vmnic0` (1Gbps Full Duplex), `vmnic2` (1Gbps Full Duplex).
   * Port Groups:
     * `VM Network`: Standard production traffic for VMs.
     * `Mirror-Network`: Promiscuous mode enabled (`allow-promiscuous = true`, `allow-mac-change = true`, `allow-forged-transmits = true`).
2. **`vSwitch-Mirror`** (Dedicated Ingest Switch):
   * Port Group `SPAN-Monitoring-PG` with VLAN `4095` (Trunk Mode / All VLANs) and Promiscuous mode enabled.

### TrueNAS Ingest Layer
* **Primary NIC (`ens192`)**: Connected to `VM Network` with static IP `192.168.0.47/24` for management and ZFS network storage.
* **Capture NIC (`ens224`)**: Connected to `Mirror-Network`. Unnumbered (no IP address assigned), brought `UP` in promiscuous mode to passively capture packets without interfering with routing or generating ARP responses.

---

## 3. Data Processing Pipeline

```
┌─────────────┐     30s Slice      ┌──────────────────┐     Extract Metadata    ┌────────────────────┐
│   tcpdump   │ ─────────────────> │ Raw PCAP Storage │ ──────────────────────> │ Python Flow Parser │
│  (ens224)   │  /mnt/pool1/.../   │  (raw_pcaps/)    │  Every 10 seconds       │   (Memory-Safe)    │
└─────────────┘                    └──────────────────┘                         └────────────────────┘
                                                                                          │
                                                                                          │ Update Records
                                                                                          ▼
                                                                                ┌────────────────────┐
                                                                                │ Per-Device Folders │
                                                                                │   devices/<IP>/    │
                                                                                │ - traffic_log.csv  │
                                                                                │ - summary.json     │
                                                                                └────────────────────┘
```
