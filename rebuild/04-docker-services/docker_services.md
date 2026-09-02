# Phase 4: Docker Host & Application Stack Rebuild

## 1. Node Specifications
* **IP Address**: `192.168.0.218`
* **Hostname**: `docker.npcsolutions.co.uk`
* **OS**: Ubuntu Server 22.04 / 24.04 LTS

## 2. Containerized Services
* **Subnet Traffic Dashboard**: Containerized web dashboard running on port `8500`.
* **Homelab Services Hub**: Main homelab navigation launchpad on port `80` / `8080`.

## 3. Automated Execution
```bash
ssh root@192.168.0.218 'bash -s' < rebuild/04-docker-services/01_install_docker_host.sh
```
