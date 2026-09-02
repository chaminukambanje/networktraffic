# Data Structures & Output Schemas

## 1. Directory Structure

```text
/mnt/pool1/network_traffic/
├── devices/
│   ├── 192.168.0.1/
│   │   ├── summary.json          <-- Aggregated device metrics by application
│   │   └── traffic_log.csv       <-- Time-series session log
│   ├── 192.168.0.113/
│   │   ├── summary.json
│   │   └── traffic_log.csv
│   └── 192.168.0.200/
│       ├── summary.json
│       └── traffic_log.csv
├── raw_pcaps/                    <-- Ingest staging for 30s rotating PCAP slices
├── scripts/
│   ├── categorize_traffic.py     <-- Binary parser & flow classifier
│   └── traffic_daemon.sh         <-- Continuous capture & process loop
├── logs/
│   └── monitor.log               <-- Service execution log
└── subnet_summary.csv            <-- High-level periodic subnet metrics
```

---

## 2. File Schemas

### `summary.json` (Per-Device JSON Rollup)

```json
{
  "device_ip": "192.168.0.200",
  "last_updated": "2026-09-02 08:39:53",
  "total_bytes": 13025,
  "total_packets": 87,
  "applications": {
    "HTTPS/TLS": {
      "total_bytes": 9058,
      "bytes_sent": 4448,
      "bytes_recv": 4610,
      "total_packets": 38,
      "unique_peers": [
        "192.168.0.104",
        "192.168.0.113"
      ]
    },
    "DNS": {
      "total_bytes": 2107,
      "bytes_sent": 756,
      "bytes_recv": 1351,
      "total_packets": 20,
      "unique_peers": [
        "192.168.0.1"
      ]
    }
  }
}
```

### `traffic_log.csv` (Per-Device Detailed Activity Log)

| Field | Description |
| :--- | :--- |
| `Timestamp` | Date and time slice was categorized (`YYYY-MM-DD HH:MM:SS`) |
| `Device_IP` | IPv4 or IPv6 address of the device |
| `Application` | Detected protocol / port application (e.g., DNS, HTTPS, SSH, SMB) |
| `Duration_Sec`| Duration of active flows within the slice |
| `Bytes_Sent` | Total outbound payload bytes |
| `Bytes_Recv` | Total inbound payload bytes |
| `Total_Bytes` | Cumulative bytes transferred |
| `Packets_Sent`| Count of outbound packets |
| `Packets_Recv`| Count of inbound packets |
| `Total_Packets`| Cumulative packet count |
| `Unique_Peers`| Number of remote IP endpoints communicated with |

---

## 3. Storage Retention & 10GB Quota Policy

To prevent storage pool saturation and maintain high I/O throughput on TrueNAS:

1. **Strict 10GB Ceiling**: Total storage consumed by `/mnt/pool1/network_traffic/` (including `raw_pcaps/`, `devices/`, and `logs/`) is capped at **10 GB** (`10,485,760 KB`).
2. **Automated Purging Mechanism**:
   * **PCAP Rotation**: `tcpdump` writes 30-second slices into ring buffers (maximum 50 active raw capture files). PCAP files older than 30 minutes are automatically deleted after flow categorization.
   * **CSV Line Truncation**: When total disk usage reaches 10GB, all `traffic_log.csv` and `subnet_summary.csv` files are automatically pruned to retain the most recent 2,500 rows while preserving header definitions.
   * **Daemon Log Rotation**: `monitor.log` is automatically truncated if it exceeds 50MB, preserving the latest 10,000 entries.
3. **Execution Cadence**: Disk usage and log sizes are verified every 10 seconds during the daemon's continuous capture cycle.

