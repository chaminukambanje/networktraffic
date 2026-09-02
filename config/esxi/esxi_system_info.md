# VMware ESXi Host Hardware & System Configuration

* **Host**: `esxi-01.npcsolutions.co.za` (`192.168.0.200`)
* **Product**: VMware ESXi 8.0.3 (Build 24677879)

## System Version
```text
Product: VMware ESXi
   Version: 8.0.3
   Build: Releasebuild-24677879
   Update: 3
   Patch: 70
```

## Hardware Platform & CPU
```text
Platform Information
   UUID: 0x4c 0x4c 0x45 0x44 0x0 0x59 0x34 0x10 0x80 0x4b 0xb8 0xc0 0x4f 0x35 0x32 0x32
   Product Name: PowerEdge R620
   Vendor Name: Dell Inc.
   Serial Number: 8Y4K522
   Enclosure Serial Number: 8Y4K522
   BIOS Asset Tag: 
   IPMI Supported: true

CPU Packages: 2
   CPU Cores: 20
   CPU Threads: 40
   Hyperthreading Active: true
   Hyperthreading Supported: true
   Hyperthreading Enabled: true
   HV Support: 3
```

## Hardware Memory
```text
Physical Memory: 240470433792 Bytes
   Reliable Memory: 0 Bytes
   NUMA Node Count: 2
```

## Datastores & Storage
```text
Mount Point                                        Volume Name                                 UUID                                 Mounted  Type             Size          Free
-------------------------------------------------  ------------------------------------------  -----------------------------------  -------  ------  -------------  ------------
/vmfs/volumes/6893488d-c4dfd4bb-20bb-90b11c3cc561  datastore2                                  6893488d-c4dfd4bb-20bb-90b11c3cc561     true  VMFS-6  2399007670272  696270192640
/vmfs/volumes/6a4fb9d9-3b7d8b33-0da4-90b11c3cc561  datastore3                                  6a4fb9d9-3b7d8b33-0da4-90b11c3cc561     true  VMFS-6  2399007670272  544598917120
/vmfs/volumes/6824ca0f-0b857519-707b-90b11c3cc561  datastore1                                  6824ca0f-0b857519-707b-90b11c3cc561     true  VMFS-6  1861599887360  362729701376
/vmfs/volumes/6824ca0f-f9173a53-55ca-90b11c3cc561  OSDATA-6824ca0f-f9173a53-55ca-90b11c3cc561  6824ca0f-f9173a53-55ca-90b11c3cc561     true  VMFSOS   128580583424  122972798976
/vmfs/volumes/1625b350-a74a0254-b68c-3f9c8a969ecd  BOOTBANK1                                   1625b350-a74a0254-b68c-3f9c8a969ecd     true  vfat       4293591040    4077060096
/vmfs/volumes/f904d0cb-b0472b50-b19e-0f73a37f49da  BOOTBANK2                                   f904d0cb-b0472b50-b19e-0f73a37f49da     true  vfat       4293591040    4021878784
```

## Physical Network Adapters (NICs)
```text
Name    PCI Device    Driver  Admin Status  Link Status  Speed  Duplex  MAC Address         MTU  Description
------  ------------  ------  ------------  -----------  -----  ------  -----------------  ----  -----------
vmnic0  0000:01:00.0  ntg3    Up            Up            1000  Full    90:b1:1c:3c:c5:61  1500  Broadcom Corporation NetXtreme BCM5720 Gigabit Ethernet
vmnic1  0000:01:00.1  ntg3    Up            Down             0  Half    90:b1:1c:3c:c5:62  1500  Broadcom Corporation NetXtreme BCM5720 Gigabit Ethernet
vmnic2  0000:02:00.0  ntg3    Up            Up            1000  Full    90:b1:1c:3c:c5:63  1500  Broadcom Corporation NetXtreme BCM5720 Gigabit Ethernet
vmnic3  0000:02:00.1  ntg3    Up            Down             0  Half    90:b1:1c:3c:c5:64  1500  Broadcom Corporation NetXtreme BCM5720 Gigabit Ethernet
```
