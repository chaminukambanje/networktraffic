#!/bin/bash
# ==============================================================================
# Homelab HPC Cluster & Slurm Workload Nodes Provisioning
# ==============================================================================
set -e

CLUSTER_NODES=(
    "192.168.0.170:node-01.home:compute"
    "192.168.0.53:node-02.home:compute"
    "192.168.0.124:node-03.home:compute"
    "192.168.0.227:node-04.home:compute"
    "192.168.0.125:node-05.home:compute"
    "192.168.0.146:node-06.home:compute"
    "192.168.0.131:login-01.home:login"
    "192.168.0.133:login-02.home:login"
)

echo "=== HPC Cluster Provisioning Script ==="
for entry in "${CLUSTER_NODES[@]}"; do
    IFS=":" read -r IP HOST ROLE <<< "$entry"
    echo "Configuring $ROLE node $HOST ($IP)..."
    # Basic provisioning steps: hosts file, SSH keys, OpenMPI, Slurm client
done
