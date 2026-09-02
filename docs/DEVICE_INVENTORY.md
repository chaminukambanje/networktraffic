# Active Homelab Network Device Catalog

Verified active hosts, virtual machines, gaming consoles, mobile clients, and infrastructure devices monitored in real-time by the Subnet Traffic Telemetry system across `192.168.0.0/24`.

> **Note**: Stale DHCP leases and offline virtual machines have been actively ping-verified and pruned from telemetry records.

---

## 🟢 Verified Active Subnet Devices

| IP Address | Hostname & Identification | Device Role | Status & Probe |
| :--- | :--- | :--- | :--- |
| `192.168.0.1` | **`skysr213.Home`** | Default Gateway & Sky Hub Router | `ONLINE` (ICMP Echo) |
| `192.168.0.27` | **`MacBookPro.Home`** | Apple MacBook Pro Laptop | `ONLINE` (ICMP Echo) |
| `192.168.0.39` | **`BC-server.Home`** | Microsoft Business Central Server VM | `ONLINE` (ICMP Echo) |
| `192.168.0.44` | **`iPhone.Home`** | Apple iPhone Mobile Device | `ONLINE` (ICMP Echo) |
| `192.168.0.47` | **`truenas.local`** | TrueNAS SCALE Storage & Ingest Server | `ONLINE` (ICMP Echo) |
| `192.168.0.53` | **`node-02.Home`** | Linux Compute Node 02 | `ONLINE` (ICMP Echo) |
| `192.168.0.92` | **`PS5-B75E08.Home`** | **Sony PlayStation 5 Console** | `ONLINE` (ICMP Echo / mDNS) |
| `192.168.0.99` | **`booklore-server.Home`** | CentOS 8 Booklore Application Server | `ONLINE` (ICMP Echo) |
| `192.168.0.104` | **`mbanjec-OptiPlex-3020M.Home`** | Dell OptiPlex 3020M Ubuntu Workstation | `ONLINE` (ICMP Echo) |
| `192.168.0.109` | **`UNICAF-2025-2026.Home`** | Windows Server 2025 Data Center VM | `ONLINE` (ARP / Active Flow) |
| `192.168.0.113` | **`Chaminukas-MBP.Home`** | Primary MacBook Pro Admin Workstation | `ONLINE` (ICMP Echo) |
| `192.168.0.124` | **`node-03.Home`** | CentOS 9 Compute Node 03 | `ONLINE` (ICMP Echo) |
| `192.168.0.125` | **`node-05.Home`** | Linux Compute Node 05 | `ONLINE` (ICMP Echo) |
| `192.168.0.131` | **`login-01.Home`** | CentOS 9 HPC Login Node 01 | `ONLINE` (ICMP Echo) |
| `192.168.0.133` | **`login-02.Home`** | CentOS 9 HPC Login Node 02 | `ONLINE` (ICMP Echo) |
| `192.168.0.139` | **`iPhone-97.Home`** | Apple iPhone Client | `ONLINE` (ICMP Echo) |
| `192.168.0.144` | **`TOSHIBA-TV.Home`** | Toshiba 4K Smart TV | `ONLINE` (ARP / Active Flow) |
| `192.168.0.146` | **`node-06.Home`** | Linux Compute Node 06 | `ONLINE` (ICMP Echo) |
| `192.168.0.170` | **`node-01.Home`** | CentOS 9 Compute Node 01 | `ONLINE` (ICMP Echo) |
| `192.168.0.171` | **`EPSON691DE7.Home`** | Epson Multi-Function Network Printer | `ONLINE` (ICMP Echo) |
| `192.168.0.197` | **`RALSPMAC-G92FWQ.Home`** | Apple Mac Workstation Client | `ONLINE` (ICMP Echo) |
| `192.168.0.200` | **`esxi-01.npcsolutions.co.za`** | VMware ESXi 8.0.3 Hypervisor Host | `ONLINE` (ICMP Echo) |
| `192.168.0.218` | **`docker.npcsolutions.co.uk`** | Ubuntu Docker Application Host | `ONLINE` (ICMP Echo) |
| `192.168.0.227` | **`node-04.Home`** | Rocky Linux Compute Node 04 | `ONLINE` (ICMP Echo) |
| `192.168.0.229` | **`mbanjec-OptiPlex-3020M-7.Home`**| Dell OptiPlex Node 7 | `ONLINE` (ARP / Active Flow) |
| `192.168.0.235` | **`ubuntutest.Home`** | Ubuntu Linux Test Environment VM | `ONLINE` (ICMP Echo) |
| `192.168.0.237` | **`sql.Home`** | Microsoft SQL Database Server 2022 VM | `ONLINE` (ARP / Active Flow) |

---

## 🧹 Pruned Stale / Inactive Entries (24 Devices)
The following IP addresses were identified as stale DHCP leases, dormant devices, or powered-off virtual machines (no ICMP response, no ARP entries, 0 traffic volume) and have been removed from active telemetry:
* `192.168.0.12` (SM-R925F Watch)
* `192.168.0.22` (Mac.Home)
* `192.168.0.45` (vphere.Home)
* `192.168.0.59` (SKY.Home)
* `192.168.0.60` (Chami-s-Old-Ultra)
* `192.168.0.81` (iPhone-10)
* `192.168.0.105` (iPad.Home)
* `192.168.0.115` (Watch.Home)
* `192.168.0.126` (odooo-and-jupyter)
* `192.168.0.134` (exch-01)
* `192.168.0.135` (Chami-Home-PC)
* `192.168.0.145` (RSLCM02)
* `192.168.0.159` (Galaxy-A32)
* `192.168.0.180` (Galaxy-A05s)
* `192.168.0.183` (WIN-ULQP7OEENNM)
* `192.168.0.202` (WIN-3L06EEP1J61)
* `192.168.0.203` (MacBook-Pro-92)
* `192.168.0.219` (docker-02)
* `192.168.0.222` (DESKTOP-T96SGVI)
* `192.168.0.223` (exchng-02)
* `192.168.0.234` (ubuntu-server)
* `192.168.0.236` (ubuntu-server-24)
* `192.168.0.238` (ubuntu-server-27)
