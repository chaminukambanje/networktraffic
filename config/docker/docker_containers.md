# Docker Application Server Host & Container Stacks

## Host System
* **Hostname**: `docker.npcsolutions.co.uk` (IP: `192.168.0.218`)
* **Kernel & OS**:
```text
Linux docker.npcsolutions.co.uk 7.0.0-30-generic #30-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 18:22:54 UTC 2026 x86_64 GNU/Linux
```

## CPU, Memory & Disk
```text
Memory:
total        used        free      shared  buff/cache   available
Mem:            60Gi       5.8Gi        46Gi        31Mi       9.6Gi        55Gi
Swap:          8.0Gi          0B       8.0Gi

Disk Usage:
Filesystem                         Size  Used Avail Use% Mounted on
tmpfs                               13G  3.3M   13G   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv  489G   47G  421G  11% /
tmpfs                               31G     0   31G   0% /dev/shm
efivarfs                           256K   64K  188K  26% /sys/firmware/efi/efivars
none                               1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
tmpfs                               31G     0   31G   0% /tmp
none                               1.0M     0  1.0M   0% /run/credentials/systemd-resolved.service
/dev/sda2                          2.0G   97M  1.7G   6% /boot
/dev/sda1                          1.1G  6.4M  1.1G   1% /boot/efi
none                               1.0M     0  1.0M   0% /run/credentials/systemd-networkd.service
tmpfs                              6.1G  8.0K  6.1G   1% /run/user/1000
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/a80b13012a549d162d9c131425cadebf3d3ec683e51a595f2ce8e5619c6de8d7
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/e0d61f34ae9b38f5a843570268a5a2760340261d908180f2e2f23082bf9a8b33
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/a485993b8da14ddc356a6f5dbd5ccfbb7a79fb30b62495a3f472de260b42deb6
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/03303c382b1eac755ebf6a62474c278a927ba9374b1e9394d4c8baa8877c030a
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/7e0a092d8221cdb43fec643665f21d1e328b0b93b8d81caf520026e06931b8d9
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/28a1afe32a4ea23aeae0f84af838a7dbca86a01833a12b54d6de66188be7c063
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/9285be2d271015fb708de0c06943ee466a843305f0a4e07d9a33905445092cf4
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/6278d0d117a47eb4b2e88e9fc05d039ed0ea886d93220e3f5fab7d3efcc7cb47
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/c93d13768895aef218c08ce160cb211397b9af33a06f3c2064eef08e349ff786
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/bf778f5420742ff47534f86adb093c260b018e935f97751e837257dad49d57d3
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/34c1fc3a2524497aadcdcdd8912e91ce3ecc1cc06efed8752d0676eae5830422
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/5554bb738634e6686c90b9d60ac1244e5dcd78def672beb3f55f11d652378e6e
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/f9fea73da10b782a4508ae85f0755877c0c92a5a5ce3735f9dd7acfec6e499d3
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/9a159542596a3563179d22b3220b5d53be89c3c52f7392767c9a1c8acd735151
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/da4c6b5e84cf0a1e1b6b576c274a992bfa66f838b2a4b7a372e2ce7b232ddcce
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/b6dd030799dc45acc6ffa49b9cbb55648dd99775afcda8a81207376d17b75ef8
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/27a6854b7ee743b72caf46d3cafd170df18c77292e9eae3db5e37d705b8b5b29
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/e868a3fcc999dd73c95932b99c0367a34b80b1e772dce1855707f8d661e9e3a1
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/e1721b38e01c19cbec0fe58582fa3f65120cfcb74233b0dcc37f5ea820e57672
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/9eb105b2e5fb36e901cbcfa108743903369d137583adbe109b6b9bc43bebd3fd
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/37d9623a164cb0b550c91094dd21505666fdff11c7ff8ded1e5378e1f1fcdeb0
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/e58ff41379103d7dd19993c38d226b94077b9c3160273990359e9740e88998c7
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/06673954572a98a22cc3e7e48580339c7c82d38e02bb6a025c08ec81dbdcaa87
none                               1.0M     0  1.0M   0% /run/credentials/getty@tty1.service
overlay                            489G   47G  421G  11% /var/lib/docker/rootfs/overlayfs/46c230edf15e2fec34fa72d38dd0769889a50ce420a4b31d8319c6793228b50a
tmpfs                              6.1G  8.0K  6.1G   1% /run/user/0
```

## Running Docker Containers
```text
CONTAINER ID   NAMES                         IMAGE                                                 STATUS                    PORTS
46c230edf15e   network-traffic-dashboard     network-traffic-dashboard-network-traffic-dashboard   Up 31 minutes             0.0.0.0:8500->8500/tcp, [::]:8500->8500/tcp
9285be2d2710   homelab-dashboard             nginx:alpine                                          Up 21 minutes (healthy)   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
205daf51b1a1   test-postgres                 postgres:15-alpine                                    Exited (0) 2 days ago     
d5dc49a88d27   ubuntu-rdp-tunnel             node:alpine                                           Exited (0) 2 days ago     
06673954572a   ubuntu-rdp-web                oznu/guacamole:latest                                 Up 55 minutes             0.0.0.0:8084->8080/tcp, [::]:8084->8080/tcp
803fa4e87ffb   fastcash-localtunnel          node:alpine                                           Exited (1) 2 days ago     
aedb8d974cbd   bc-localtunnel                node:alpine                                           Exited (0) 2 days ago     
28a1afe32a4e   bc-nginx-proxy                nginx:alpine                                          Up 55 minutes             80/tcp, 0.0.0.0:8097->8097/tcp, [::]:8097->8097/tcp
37d9623a164c   unicaf-rdp-web                oznu/guacamole:latest                                 Up 55 minutes             0.0.0.0:8086->8080/tcp, [::]:8086->8080/tcp
c93d13768895   fast-cash-uk-app              fast-cash-uk-app-fast-cash-uk                         Up 55 minutes             0.0.0.0:8098->8098/tcp, [::]:8098->8098/tcp
6278d0d117a4   network-power-exporter        network-power-exporter:latest                         Up 55 minutes (healthy)   
b6dd030799dc   prometheus                    prom/prometheus:latest                                Up 55 minutes             0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp
bf778f542074   news-dashboard                news-dashboard:latest                                 Up 55 minutes (healthy)   0.0.0.0:8090->8090/tcp, [::]:8090->8090/tcp
e0d61f34ae9b   jasmin-xfer                   sigoden/dufs:latest                                   Up 55 minutes             0.0.0.0:8882->5000/tcp, [::]:8882->5000/tcp
03303c382b1e   jasmin-portal                 jasmin-cluster-jasmin-portal                          Up 55 minutes             80/tcp, 0.0.0.0:8880->8880/tcp, [::]:8880->8880/tcp
f9fea73da10b   jasmin-cluster-api            jasmin-cluster-jasmin-cluster-api                     Up 55 minutes             0.0.0.0:8881->8881/tcp, [::]:8881->8881/tcp
5554bb738634   jasmin-notebooks              jasmin-cluster-jasmin-notebooks                       Up 55 minutes             0.0.0.0:8888->8888/tcp, [::]:8888->8888/tcp
e58ff4137910   single-node-wazuh.manager     wazuh/wazuh-manager:4.9.2                             Up 55 minutes (healthy)   0.0.0.0:1514-1515->1514-1515/tcp, [::]:1514-1515->1514-1515/tcp, 0.0.0.0:514->514/udp, [::]:514->514/udp, 0.0.0.0:55000->55000/tcp, [::]:55000->55000/tcp, 1516/tcp
9a159542596a   esxi-exporter                 esxi-exporter:latest                                  Up 55 minutes             0.0.0.0:9272->9272/tcp, [::]:9272->9272/tcp
34c1fc3a2524   grafana                       grafana/grafana:latest                                Up 55 minutes             0.0.0.0:3002->3000/tcp, [::]:3002->3000/tcp
7e0a092d8221   cadvisor                      gcr.io/cadvisor/cadvisor:latest                       Up 55 minutes (healthy)   0.0.0.0:8085->8080/tcp, [::]:8085->8080/tcp
a485993b8da1   node-exporter                 prom/node-exporter:latest                             Up 55 minutes             0.0.0.0:9100->9100/tcp, [::]:9100->9100/tcp
da4c6b5e84cf   telegraf                      telegraf:latest                                       Up 55 minutes             8092/udp, 8125/udp, 8094/tcp, 0.0.0.0:9273->9273/tcp, [::]:9273->9273/tcp
27a6854b7ee7   single-node-wazuh.dashboard   wazuh/wazuh-dashboard:4.9.2                           Up 55 minutes             443/tcp, 0.0.0.0:8443->5601/tcp, [::]:8443->5601/tcp
e868a3fcc999   single-node-wazuh.indexer     wazuh/wazuh-indexer:4.9.2                             Up 55 minutes (healthy)   0.0.0.0:9200->9200/tcp, [::]:9200->9200/tcp
e1721b38e01c   tiktok-browser                lscr.io/linuxserver/chromium:latest                   Up 55 minutes             0.0.0.0:3000-3001->3000-3001/tcp, [::]:3000-3001->3000-3001/tcp
9eb105b2e5fb   wg-easy                       ghcr.io/wg-easy/wg-easy:latest                        Up 55 minutes (healthy)   0.0.0.0:51820->51820/udp, [::]:51820->51820/udp, 0.0.0.0:51821->51821/tcp, [::]:51821->51821/tcp
a80b13012a54   cloudflare-ddns               favonia/cloudflare-ddns:latest                        Up 55 minutes
```

## Docker Networks
```text
NETWORK ID     NAME                                DRIVER    SCOPE
5177d6d2e9ef   bridge                              bridge    local
16f006824a53   fast-cash-uk-app_default            bridge    local
c7261e7e1090   homelab-portal_default              bridge    local
241efd0a4447   host                                host      local
f2a44eee1280   jasmin-net                          bridge    local
845ea63d25d7   monitoring-stack_monitoring-net     bridge    local
0ce83a33ce3e   network-traffic-dashboard_default   bridge    local
d30b159f5f18   news-dashboard_default              bridge    local
8eaaf1452660   none                                null      local
8005f249bd81   single-node_default                 bridge    local
41a915e42a44   ubuntu-rdp-web_default              bridge    local
fbfd41c172b7   unicf-rdp_default                   bridge    local
af6775419d9b   wg-easy_default                     bridge    local
```
