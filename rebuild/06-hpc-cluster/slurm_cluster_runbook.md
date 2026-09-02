# Phase 6: HPC Cluster Nodes & Slurm Workload Provisioning

## 1. Node Inventory & Roles

| Node Hostname | IP Address | OS Distribution | Cluster Role |
| :--- | :--- | :--- | :--- |
| **`login-01.home`** | `192.168.0.131` | CentOS Stream 9 | Primary Login / Head Node |
| **`login-02.home`** | `192.168.0.133` | CentOS Stream 9 | Secondary Login / Bastion |
| **`node-01.home`** | `192.168.0.170` | CentOS Stream 9 | Compute Worker Node 01 |
| **`node-02.home`** | `192.168.0.53` | CentOS Stream 9 | Compute Worker Node 02 |
| **`node-03.home`** | `192.168.0.124` | CentOS Stream 9 | Compute Worker Node 03 |
| **`node-04.home`** | `192.168.0.227` | Rocky Linux 9 | Compute Worker Node 04 |
| **`node-05.home`** | `192.168.0.125` | Linux Compute | Compute Worker Node 05 |
| **`node-06.home`** | `192.168.0.146` | Linux Compute | Compute Worker Node 06 |

## 2. Shared File Systems & MPI Setup
* **Shared Storage**: `/mnt/scratch` NFS mounted from TrueNAS (`192.168.0.47`).
* **Environment Modules**: Lmod with GCC, OpenMPI, and Python scientific stack (matching JASMIN environment).
