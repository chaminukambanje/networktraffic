# VMware ESXi Virtual Switch & Port Group Topology

## Virtual Switches (vSwitch0 & vSwitch-Mirror)
```text
vSwitch0
   Name: vSwitch0
   Class: cswitch
   Num Ports: 7680
   Used Ports: 26
   Configured Ports: 128
   MTU: 1500
   CDP Status: listen
   Beacon Enabled: false
   Beacon Interval: 1
   Beacon Threshold: 3
   Beacon Required By: 
   Uplinks: vmnic2, vmnic3, vmnic0, vmnic1
   Portgroups: Mirror-Network, VM Network, Management Network

vSwitch-Mirror
   Name: vSwitch-Mirror
   Class: cswitch
   Num Ports: 7680
   Used Ports: 1
   Configured Ports: 128
   MTU: 1500
   CDP Status: listen
   Beacon Enabled: false
   Beacon Interval: 1
   Beacon Threshold: 3
   Beacon Required By: 
   Uplinks: 
   Portgroups: SPAN-Monitoring-PG
```

## Port Groups (Including Mirror-Network & SPAN-Monitoring-PG)
```text
Name                Virtual Switch  Active Clients  VLAN ID
------------------  --------------  --------------  -------
Management Network  vSwitch0                     1        0
Mirror-Network      vSwitch0                     1        0
SPAN-Monitoring-PG  vSwitch-Mirror               0     4095
VM Network          vSwitch0                    15        0
```

## VMkernel Interfaces & IP Routing
```text
vmk0
   Name: vmk0
   MAC Address: 90:b1:1c:3c:c5:62
   Enabled: true
   Portset: vSwitch0
   Portgroup: Management Network
   Netstack Instance: defaultTcpipStack
   VDS Name: N/A
   VDS UUID: N/A
   VDS Port: N/A
   VDS Connection: -1
   Opaque Network ID: N/A
   Opaque Network Type: N/A
   External ID: N/A
   MTU: 1500
   TSO MSS: 65535
   RXDispQueue Size: 4
   Port ID: 67108879

IPv4 Routing:
Network      Netmask        Gateway      Interface  Source
-----------  -------------  -----------  ---------  ------
default      0.0.0.0        192.168.0.1  vmk0       MANUAL
192.168.0.0  255.255.255.0  0.0.0.0      vmk0       MANUAL

DNS Servers:
Error: Unknown command or namespace network ip dns server get
```
