#!/bin/sh
# ==============================================================================
# VMware ESXi 8.0.3 Rebuild & Virtual Switch Provisioning Script
# Target Host: 192.168.0.200 (esxi-01.npcsolutions.co.za)
# ==============================================================================
set -e

echo "=== [1/4] Checking Existing Virtual Switches ==="
esxcli network vswitch standard list

echo "=== [2/4] Creating Dedicated Mirror Switch (vSwitch-Mirror) ==="
if ! esxcli network vswitch standard list | grep -q "vSwitch-Mirror"; then
    esxcli network vswitch standard add -v vSwitch-Mirror
    echo "vSwitch-Mirror created successfully."
else
    echo "vSwitch-Mirror already exists."
fi

echo "=== [3/4] Creating SPAN-Monitoring Port Group (VLAN 4095 Trunk) ==="
if ! esxcli network vswitch standard portgroup list | grep -q "SPAN-Monitoring-PG"; then
    esxcli network vswitch standard portgroup add -p SPAN-Monitoring-PG -v vSwitch-Mirror
    esxcli network vswitch standard portgroup set -p SPAN-Monitoring-PG -v 4095
    esxcli network vswitch standard portgroup policy security set -p SPAN-Monitoring-PG         --allow-promiscuous true --allow-mac-change true --allow-forged-transmits true
    echo "SPAN-Monitoring-PG created with promiscuous mode enabled."
else
    echo "SPAN-Monitoring-PG already exists."
fi

echo "=== [4/4] Creating Mirror-Network Port Group on vSwitch0 ==="
if ! esxcli network vswitch standard portgroup list | grep -q "Mirror-Network"; then
    esxcli network vswitch standard portgroup add -p Mirror-Network -v vSwitch0
    esxcli network vswitch standard portgroup policy security set -p Mirror-Network         --allow-promiscuous true --allow-mac-change true --allow-forged-transmits true
    echo "Mirror-Network created with promiscuous mode enabled."
else
    echo "Mirror-Network already exists."
fi

echo "=== Verification of Port Groups ==="
esxcli network vswitch standard portgroup list
echo "ESXi Network Configuration Completed Successfully."
