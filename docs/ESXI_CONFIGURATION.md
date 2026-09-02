# VMware ESXi Setup & Configuration Runbook

## 1. Virtual Switch & Port Group Creation

Execute the following commands via SSH on the ESXi Host (`192.168.0.200`):

```bash
# 1. Create Dedicated Mirror Virtual Switch
esxcli network vswitch standard add -v vSwitch-Mirror

# 2. Add Monitoring Port Group with VLAN Trunking (4095)
esxcli network vswitch standard portgroup add -p SPAN-Monitoring-PG -v vSwitch-Mirror
esxcli network vswitch standard portgroup set -p SPAN-Monitoring-PG -v 4095
esxcli network vswitch standard portgroup policy security set -p SPAN-Monitoring-PG \
    --allow-promiscuous true --allow-mac-change true --allow-forged-transmits true

# 3. Add Promiscuous Mirror Port Group to Production vSwitch0
esxcli network vswitch standard portgroup add -p Mirror-Network -v vSwitch0
esxcli network vswitch standard portgroup policy security set -p Mirror-Network \
    --allow-promiscuous true --allow-mac-change true --allow-forged-transmits true
```

---

## 2. TrueNAS Virtual Machine NIC Attachment

To hot-add a secondary network adapter directly attached to the promiscuous port group:

```bash
# Obtain TrueNAS VM ID (e.g., VMID 76)
vim-cmd vmsvc/getallvms | grep -i truenas

# Add secondary vmxnet3 adapter mapped to Mirror-Network
vim-cmd vmsvc/devices.createnic 76 vmxnet3 "Mirror-Network"

# Verify connected networks
vim-cmd vmsvc/get.networks 76
```

---

## 3. Verification

Verify that promiscuous policies are active:

```bash
esxcli network vswitch standard portgroup list
```
