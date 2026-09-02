# Complete Homelab Disaster Recovery & Rebuild Runbook

Automated, end-to-end blueprint and executable deployment scripts to rebuild the entire physical network, VMware ESXi virtualization cluster, TrueNAS ZFS storage, Docker container platforms, HPC Slurm compute nodes, and database servers.

---

## 🏗️ Rebuild Order of Execution (Step-by-Step)

Follow the phased order below to recover from a complete bare-metal or environment outage:

```
┌────────────────────────────────────────────────────────────┐
│ Phase 1: Physical Network & Sky Hub Gateway (192.168.0.1)   │
└─────────────────────────────┬──────────────────────────────┘
                              │ Subnet 192.168.0.0/24 & DHCP
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 2: VMware ESXi 8.0 Hypervisor Host (192.168.0.200)   │
│  - Standard vSwitch0 (Production)                          │
│  - Promiscuous Mirror vSwitch-Mirror (SPAN / VLAN 4095)    │
└─────────────────────────────┬──────────────────────────────┘
                              │ Virtual Machine Hosting
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 3: TrueNAS SCALE ZFS Storage (192.168.0.47)          │
│  - Pool1 ZFS datasets (/mnt/pool1/network_traffic)         │
│  - Unnumbered Mirror NIC (ens224) & 10GB Retention Daemon  │
└─────────────────────────────┬──────────────────────────────┘
                              │ NFS / Storage Ingest
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 4: Ubuntu Docker Host (192.168.0.218)                │
│  - Docker Engine & Compose Stacks                          │
│  - Telemetry Dashboard (8500) & Homelab Launchpad (80)     │
└─────────────────────────────┬──────────────────────────────┘
                              │ Compute & Database Services
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 5: MS SQL Server 2022 Database VM (192.168.0.237)    │
│ Phase 6: HPC Slurm Cluster (Login: 131/133, Nodes: 170..227)│
│ Phase 7: MSc Computer Science Study Lab (192.168.0.109)    │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 8: Automated Topology & Health Verification          │
│  - rebuild/08-verification/verify_homelab_health.py        │
└────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory & Runbook Catalog

| Phase | Directory & Runbook | Description | Execution Command |
| :--- | :--- | :--- | :--- |
| **01** | [`01-network-gateway/`](01-network-gateway/gateway_config.md) | Gateway WAN/LAN, Wi-Fi WPA3-SAE, and static DHCP allocations | Manual Web UI / DHCP import |
| **02** | [`02-esxi-hypervisor/`](02-esxi-hypervisor/esxi_host_provisioning.md) | vSwitch provisioning, SPAN port groups, and promiscuous mode | `ssh root@192.168.0.200 'sh -s' < 02-esxi-hypervisor/01_esxi_vswitch_setup.sh` |
| **03** | [`03-truenas-storage/`](03-truenas-storage/truenas_scale_rebuild.md) | ZFS pool dataset, unnumbered capture NIC, and capture daemon | `ssh root@192.168.0.47 'bash -s' < 03-truenas-storage/01_truenas_storage_setup.sh` |
| **04** | [`04-docker-services/`](04-docker-services/docker_services.md) | Docker Engine installation, NFS mounts, and Compose stack | `ssh root@192.168.0.218 'bash -s' < 04-docker-services/01_install_docker_host.sh` |
| **05** | [`05-database-sql/`](05-database-sql/mssql_server_runbook.md) | MS SQL Server 2022 database schema & firewall ports | SSMS / `sqlcmd` initialization |
| **06** | [`06-hpc-cluster/`](06-hpc-cluster/slurm_cluster_runbook.md) | HPC Bastion & Worker nodes provisioning and Slurm config | `bash 06-hpc-cluster/01_hpc_cluster_provisioning.sh` |
| **07** | [`07-msc-lab-vm/`](07-msc-lab-vm/unicaf_lab_setup.md) | UNICAF MSc CS Windows Server 2025 VM configuration | ESXi VM deployment |
| **08** | [`08-verification/`](08-verification/verify_homelab_health.py) | Automated concurrent health check of all 25+ subnet endpoints | `python3 rebuild/08-verification/verify_homelab_health.py` |
