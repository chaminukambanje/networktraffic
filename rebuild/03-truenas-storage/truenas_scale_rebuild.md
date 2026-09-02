# Phase 3: TrueNAS SCALE Storage & Ingest Server Rebuild

## 1. Node Identity
* **IP Address**: `192.168.0.47` (Management `ens192`)
* **Mirror Capture Interface**: `ens224` (Unnumbered, Promiscuous)
* **Hostname**: `truenas.local`
* **Primary Pool**: `pool1` (ZFS RAIDZ / Mirror)

## 2. Ingest Architecture
* **Capture Interface**: `ens224` is attached to `Mirror-Network` on ESXi with promiscuous mode enabled.
* **Storage Ingest Path**: `/mnt/pool1/network_traffic`
* **Retention Policy**: Strict automated ceiling of **10 GB** with automatic 30-minute PCAP rotation and CSV history pruning.

## 3. Execution
```bash
ssh root@192.168.0.47 'bash -s' < rebuild/03-truenas-storage/01_truenas_storage_setup.sh
```
