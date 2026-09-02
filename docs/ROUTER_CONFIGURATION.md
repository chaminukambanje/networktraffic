# Sky Broadband Gateway (SR213) Configuration Runbook

Comprehensive network, routing, Wi-Fi, and security configuration for the primary default gateway (`192.168.0.1`) powering the homelab and residential network.

---

## 1. Gateway & System Overview

| Parameter | Value / Setting | Notes |
| :--- | :--- | :--- |
| **Model** | **Sky Broadband Hub (SR213)** | Sky UK Dual-Band Wi-Fi Gateway |
| **Hostname** | `skysr213.home` | Local DNS resolvable |
| **Local IP Address** | `192.168.0.1` | Default Gateway for Subnet `192.168.0.0/24` |
| **MAC Address (2.4 GHz)** | `00:90:4C:3F:B0:55` | Primary BSSID / LAN Interface |
| **MAC Address (5 GHz)** | `00:90:4C:41:50:35` | Secondary High-Band BSSID |
| **Search Domain** | `Home` (`.home`) | Internal local domain suffix |
| **Management Interface** | `http://192.168.0.1/` (HTTP/80, HTTPS/443) | Web portal (RDK-B UI) |

---

## 2. WAN & Internet Connectivity

| Parameter | Configuration | Details |
| :--- | :--- | :--- |
| **Public IPv4 Address** | `90.208.56.50` | Dynamic WAN IP assigned via Sky UK |
| **Internet Service Provider** | **Sky UK Limited** (AS5607) | FTTC / FTTP Broadband Access |
| **IPv6 Dual-Stack** | **Active / Enabled** | `2a06:5906:1fc4:3200::/64` Prefix Delegation |
| **Primary IPv4 DNS** | `192.168.0.1` | Local Gateway DNS proxy / cache |
| **Primary IPv6 DNS** | `fd31:1624:2a00:5587:c600:ff:fe26:9` | Gateway ULA DNS resolver |

---

## 3. Local Area Network (LAN) & DHCP Services

```
┌─────────────────────────────────────────────────────────────┐
│ Subnet Addressing: 192.168.0.0 / 24 (Netmask: 255.255.255.0)│
├─────────────────────────────────────────────────────────────┤
│ Gateway:         192.168.0.1                                │
│ DHCP Pool:       192.168.0.2 - 192.168.0.254                │
│ Broadcast:       192.168.0.255                              │
└─────────────────────────────────────────────────────────────┘
```

* **DHCP Server**: Built-in dnsmasq / RDK-B DHCP daemon.
* **Lease Allocation**: Automated host reservation & hostname registration under `.home`.

---

## 4. Wireless (Wi-Fi) Network Configuration

* **Network SSID**: `MUNASHE_WIFI`
* **Security Suite**: `WPA3-SAE` (Enhanced open / WPA3-Personal)
* **Band Steering**: Active (Coordinates device transitions between 2.4 GHz and 5 GHz)

### Radio Frequencies & Physical Layer:
* **2.4 GHz Radio**:
  * Status: **Active**
  * Channel Mode: **Auto**
  * Channel Bandwidth: **20 MHz**
  * STBC (Space-Time Block Coding): **Enabled**
  * Reverse Direction Grant (RDG): **Disabled**
* **5 GHz Radio**:
  * Status: **Active**
  * Channel Mode: **Auto** (Operating on Channel **100**)
  * Channel Bandwidth: **80 MHz**
  * DFS (Dynamic Frequency Selection): **Enabled**
  * STBC: **Enabled**
  * Link Rates: Up to **1300 Mbps** (3x3 MIMO / MCS 9)

### Access Control & WPS:
* **MAC Filtering**: `Allow-All` (No active client blocklists).
* **Wi-Fi Protected Setup (WPS)**: Enabled (`PushButton` & `PIN` methods; AP PIN: `20907631`).

---

## 5. Security & Firewall Policies

### IPv4 Firewall (`Minimum Security / Low`)
* **LAN-to-WAN (Egress)**: All outbound connections permitted.
* **WAN-to-LAN (Ingress)**: Unsolicited inbound traffic blocked; Intrusion Detection System (IDS) active; IDENT (Port 113) filtered.

### IPv6 Firewall (`Typical Security / Default`)
* **LAN-to-WAN (Egress)**: All outbound IPv6 traffic allowed.
* **WAN-to-LAN (Ingress)**: Unsolicited inbound packets dropped by stateful inspection engine; IDS active.

### Port Forwarding & DMZ
* **Management Model**: Centralized cloud synchronization via the `My Sky` application framework.

---

## 6. Homelab Infrastructure Mapping

| Device Category | IP Address | Hostname | Role |
| :--- | :--- | :--- | :--- |
| **Gateway** | `192.168.0.1` | `skysr213.home` | Default Gateway & DNS Proxy |
| **TrueNAS SCALE** | `192.168.0.47` | `truenas.local` | ZFS Storage, NFS/SMB Ingest |
| **ESXi Hypervisor** | `192.168.0.200` | `esxi-01.npcsolutions.co.za` | VMware ESXi 8.0 Hypervisor Host |
| **Docker Server** | `192.168.0.218` | `docker.npcsolutions.co.uk` | Application Containers & Dashboard |
| **SQL Database** | `192.168.0.237` | `sql.home` | MS SQL Database Server 2022 |
| **HPC Bastion** | `192.168.0.131` | `login-01.home` | Cluster Access Node |
| **Compute Nodes** | `192.168.0.170`, `53`, `124`, `227` | `node-01` to `node-04` | Rocky / CentOS Compute Nodes |
| **MSc Lab VM** | `192.168.0.109` | `unicaf-2025-2026.home` | UNICAF MSc Computer Science VM |
| **Admin Workstation** | `192.168.0.113` | `chaminukas-mbp.home` | MacBook Pro Administration Node |
