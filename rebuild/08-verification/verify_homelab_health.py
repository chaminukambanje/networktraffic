#!/usr/bin/env python3
"""
Homelab Health Check & Infrastructure Topology Verifier
Performs automated concurrent ping (ICMP) and service port checks across all
25+ homelab devices, hypervisors, and storage endpoints.
"""

import subprocess, socket, concurrent.futures, time

NODES = [
    ("192.168.0.1", "Sky Hub SR213 Gateway", [80, 443]),
    ("192.168.0.200", "VMware ESXi 8.0 Hypervisor", [443, 902, 22]),
    ("192.168.0.47", "TrueNAS SCALE ZFS Storage", [80, 443, 22, 8500]),
    ("192.168.0.218", "Docker Application Host", [22, 80, 8500]),
    ("192.168.0.237", "Microsoft SQL Server 2022", [1433, 3389]),
    ("192.168.0.131", "HPC Login Node 01", [22]),
    ("192.168.0.133", "HPC Login Node 02", [22]),
    ("192.168.0.170", "HPC Compute Node 01", [22]),
    ("192.168.0.53", "HPC Compute Node 02", [22]),
    ("192.168.0.124", "HPC Compute Node 03", [22]),
    ("192.168.0.227", "HPC Compute Node 04", [22]),
    ("192.168.0.125", "HPC Compute Node 05", [22]),
    ("192.168.0.146", "HPC Compute Node 06", [22]),
    ("192.168.0.109", "UNICAF MSc Lab VM", [3389]),
    ("192.168.0.99", "BookLore Application Server", [22, 80]),
    ("192.168.0.39", "Business Central Server", [22, 7046]),
    ("192.168.0.104", "Dell OptiPlex Workstation", [22]),
    ("192.168.0.171", "Epson Network Printer", [80, 515, 9100])
]

def check_ping(ip):
    res = subprocess.run(["ping", "-c", "1", "-W", "1000", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    res = s.connect_ex((ip, port))
    s.close()
    return res == 0

def probe_node(node):
    ip, name, ports = node
    ping_ok = check_ping(ip)
    open_ports = []
    if ping_ok:
        for p in ports:
            if check_port(ip, p):
                open_ports.append(p)
    return {
        "ip": ip,
        "name": name,
        "ping": ping_ok,
        "open_ports": open_ports,
        "expected_ports": ports
    }

def main():
    print("=" * 80)
    print(" 🏥 HOMELAB INFRASTRUCTURE DISASTER RECOVERY & TOPOLOGY HEALTH CHECK")
    print("=" * 80)
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(probe_node, NODES))
        
    online_count = sum(1 for r in results if r["ping"])
    total_count = len(results)
    
    print(f"\nStatus Summary: {online_count}/{total_count} Monitored Hosts Active\n")
    print(f"{'IP Address':<16} | {'Hostname & Role':<32} | {'Ping':<8} | {'Open Services'}")
    print("-" * 80)
    
    for r in results:
        status_str = "🟢 ONLINE" if r["ping"] else "🔴 OFFLINE"
        ports_str = ", ".join(str(p) for p in r["open_ports"]) if r["open_ports"] else ("N/A" if not r["ping"] else "None")
        print(f"{r['ip']:<16} | {r['name']:<32} | {status_str:<8} | {ports_str}")
        
    print("-" * 80)
    print(f"Health check completed in {time.time() - start:.2f}s\n")

if __name__ == "__main__":
    main()
