# Homelab Docker Server & Application Services Architecture

Comprehensive documentation of the Homelab Docker Host (`docker.npcsolutions.co.uk` at `192.168.0.218`), container stacks, network bridges, and the unified Homelab Services Launchpad.

---

## 🖥️ Docker Host Infrastructure

* **Hostname**: `docker.npcsolutions.co.uk` (IP: `192.168.0.218` / VM ID `107` on ESXi 8.0)
* **Operating System**: Ubuntu Linux (Kernel `6.8.0-52-generic`)
* **Hardware Allocation**:
  * **vCPU**: 8 Cores (AMD Ryzen / EPYC Virtualized)
  * **Memory**: 32 GB RAM
  * **Storage**: Primary root ext4 + attached ZFS iSCSI / NFS storage
* **Default Gateway**: `192.168.0.1` (`skysr213.Home`)

---

## 🐳 Running Container Stacks & Port Mappings

| Container Name | Image | Published Ports | Role & Function |
| :--- | :--- | :--- | :--- |
| **`homelab-dashboard`** | `nginx:alpine` | `80:80`, `8080:80` | Unified Homelab Launchpad & Services Portal |
| **`network-traffic-dashboard`** | `python:3.12-alpine` | `8500:8500` | Subnet & Docker Real-time Traffic Telemetry |
| **`grafana`** | `grafana/grafana` | `3002:3000` | Infrastructure & Telemetry Visualization Dashboards |
| **`prometheus`** | `prom/prometheus` | `9090:9090` | Time-series Metrics Scraper & Storage Engine |
| **`cadvisor`** | `gcr.io/cadvisor/cadvisor` | `8085:8080` | Real-time Container Resource & Hardware Metrics |
| **`node-exporter`** | `prom/node-exporter` | `9100:9100` | Host Linux Hardware Metrics Collector |
| **`ubuntu-rdp-web`** | `oznu/guacamole` | `8084:8080` | HTML5 Browser Remote Desktop for Ubuntu Workstation |
| **`unicaf-rdp-web`** | `oznu/guacamole` | `8086:8080` | HTML5 Browser Remote Desktop for Windows Server 2025 |
| **`jasmin-portal`** | `jasmin/portal` | `8880:8880` | High Performance SMS Gateway Web Management |
| **`jasmin-cluster-api`** | `jasmin/cluster-api` | `8881:8881` | REST API for Cluster Management |
| **`jasmin-xfer`** | `jasmin/xfer` | `8882:5000` | Transfer & Batch Dispatch Service |
| **`jasmin-notebooks`** | `jupyter/minimal-notebook` | `8888:8888` | Data Science & Automation Notebooks |
| **`single-node-wazuh.dashboard`** | `wazuh/wazuh-dashboard` | `8443:5601` | SIEM & Security Operations Center Dashboard |
| **`single-node-wazuh.manager`** | `wazuh/wazuh-manager` | `1514-1515:1514-1515`, `55000:55000` | Wazuh SIEM Agent Manager & Threat Engine |
| **`single-node-wazuh.indexer`** | `wazuh/wazuh-indexer` | `9200:9200` | Elastic OpenSearch Security Event Indexer |
| **`wg-easy`** | `ghcr.io/wg-easy/wg-easy` | `51820:51820/udp`, `51821:51821` | WireGuard VPN Gateway & Client Manager |
| **`cloudflare-ddns`** | `favonia/cloudflare-ddns` | Internal | Dynamic DNS Sync for `docker.npcsolutions.co.uk` |
| **`news-dashboard`** | `custom/news-dashboard` | `8090:8090` | Financial & Global Telemetry Aggregator |
| **`fast-cash-uk-app`** | `custom/fast-cash-app` | `8098:8098` | Core Business Application Stack |
| **`bc-nginx-proxy`** | `nginx:alpine` | `8097:8097` | Microsoft Business Central Reverse Proxy |

---

## 🚪 Homelab Portal Integration (`homelab-dashboard`)

* **Configuration**: Defined in `/home/mbanjec/homelab-portal/services.json` and served via `/home/mbanjec/homelab-portal/nginx.conf`.
* **Integrated Tiles**:
  * **Monitoring & Metrics**: *Subnet Network Traffic Telemetry*, *Grafana*, *Prometheus*, *cAdvisor*, *Node Exporter*.
  * **Remote Desktop**: *Ubuntu PC Desktop (8084)*, *UNICAF Windows Server 2025 (8086)*.
  * **Security & SIEM**: *Wazuh Security Operations Center (8443)*, *WireGuard VPN (51821)*.
  * **Enterprise Services**: *Microsoft Business Central Proxy (8097)*, *Jasmin HPC Cluster (8880-8888)*.
