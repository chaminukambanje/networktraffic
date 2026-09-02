# Homelab & Network Architecture Context

## Environment Endpoints
* **VMware ESXi 8.0.3**: `192.168.0.200` (`esxi-01.npcsolutions.co.za`)
* **TrueNAS SCALE 26.0**: `192.168.0.47` (`truenas.local`)
* **Docker Server**: `192.168.0.218` (`docker.npcsolutions.co.uk`)
* **Default Gateway**: `192.168.0.1` (`skysr213.Home`)
* **Live Telemetry Dashboard**: `http://192.168.0.218:8500`

## System Guidelines
* TrueNAS storage pool is `/mnt/pool1/network_traffic/` with a strict 10GB retention quota.
* Capture interface on TrueNAS is `ens224` (promiscuous unnumbered mirror).
* Remote Docker host runs 20+ container stacks managed via Docker Compose.
