# Phase 2: VMware ESXi 8.0.3 Hypervisor Host Rebuild

## 1. Host Specifications
* **IP Address**: `192.168.0.200`
* **Hostname**: `esxi-01.npcsolutions.co.za`
* **Hypervisor Version**: VMware ESXi 8.0.3 (Build 24022510)
* **Default Production vSwitch**: `vSwitch0` (Uplink to Physical Gateway `192.168.0.1`)

## 2. Virtual Networking Architecture
To support the real-time Subnet Traffic Telemetry and VM communication, two virtual switches and port groups are required:

1. **`vSwitch0` (Production)**:
   * **`VM Network`**: Standard production VM traffic.
   * **`Mirror-Network`**: Promiscuous mode enabled (`Allow Promiscuous = Yes`, `MAC Address Changes = Yes`, `Forged Transmits = Yes`).
2. **`vSwitch-Mirror` (Isolated SPAN)**:
   * **`SPAN-Monitoring-PG`**: Dedicated mirror switch with VLAN ID `4095` (VGT trunking) and promiscuous mode enabled.

## 3. Automated Execution
Run the provisioning script via SSH on ESXi:
```bash
ssh root@192.168.0.200 'sh -s' < rebuild/02-esxi-hypervisor/01_esxi_vswitch_setup.sh
```

## 4. TrueNAS Secondary Capture Interface Attachment
After deploying the TrueNAS SCALE virtual machine, attach the secondary mirror interface:
```bash
# Locate TrueNAS VMID
TRUENAS_VMID=$(vim-cmd vmsvc/getallvms | grep -i truenas | awk '{print $1}')
echo "TrueNAS VMID: $TRUENAS_VMID"

# Hot-add secondary vmxnet3 adapter mapped to Mirror-Network
vim-cmd vmsvc/devices.createnic $TRUENAS_VMID vmxnet3 "Mirror-Network"

# Verify attached networks
vim-cmd vmsvc/get.networks $TRUENAS_VMID
```
