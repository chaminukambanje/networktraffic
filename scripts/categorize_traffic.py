#!/usr/bin/env python3
"""
Subnet Traffic Categorizer and Flow Analyzer
Autonomous pure-Python binary PCAP parser decoding Ethernet, 802.1Q VLAN,
IPv4, IPv6, TCP, UDP, ICMP, DNS, performing Reverse DNS Hostname Resolution,
and maintaining the complete 50-device subnet catalog.
"""

import os
import sys
import glob
import time
import struct
import socket
import csv
import json
from datetime import datetime
from collections import defaultdict

BASE_DIR = "/mnt/pool1/network_traffic"
DEVICES_DIR = os.path.join(BASE_DIR, "devices")
RAW_DIR = os.path.join(BASE_DIR, "raw_pcaps")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DNS_CACHE_FILE = os.path.join(BASE_DIR, "dns_cache.json")

PORT_MAP = {
    53: "DNS",
    80: "HTTP",
    443: "HTTPS/TLS",
    22: "SSH",
    123: "NTP",
    445: "SMB/ActiveDirectory",
    137: "NetBIOS",
    138: "NetBIOS",
    139: "NetBIOS",
    3389: "RDP",
    1883: "MQTT",
    8883: "MQTT-Secure",
    1900: "SSDP/UPnP",
    5353: "mDNS",
    67: "DHCP",
    68: "DHCP",
    5060: "SIP",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    902: "VMware-Auth",
    4444: "Metasploit/Agent",
    5000: "UPnP/Flask",
    8000: "HTTP-Dev",
    9000: "Portainer/PHP",
    2049: "NFS"
}

KNOWN_HOSTS = {
    '192.168.0.1': 'skysr213.Home (Default Gateway & Router)',
    '192.168.0.12': 'SM-R925F.Home (Samsung Galaxy Watch)',
    '192.168.0.22': 'Mac.Home (Apple Mac Workstation)',
    '192.168.0.27': 'MacBookPro.Home (Apple MacBook Pro)',
    '192.168.0.39': 'BC-server.Home (Business Central Server VM)',
    '192.168.0.44': 'iPhone.Home (Apple iPhone)',
    '192.168.0.45': 'vphere.Home (VMware vSphere Appliance)',
    '192.168.0.47': 'truenas.local (TrueNAS SCALE Storage)',
    '192.168.0.53': 'node-02.Home (Compute Node 02)',
    '192.168.0.59': 'SKY.Home (Sky Q TV Box)',
    '192.168.0.60': 'Chami-s-Old-Ultra.Home (Galaxy S24 Ultra)',
    '192.168.0.81': 'iPhone-10.Home (Apple iPhone)',
    '192.168.0.92': 'PS5-B75E08 (Sony PlayStation 5)',
    '192.168.0.99': 'booklore-server.Home (Booklore Server VM)',
    '192.168.0.104': 'mbanjec-OptiPlex-3020M.Home (Dell OptiPlex Workstation)',
    '192.168.0.105': 'iPad.Home (Apple iPad)',
    '192.168.0.109': 'UNICAF-2025-2026.Home (Windows Server 2025 VM)',
    '192.168.0.113': 'Chaminukas-MBP.Home (Admin MacBook Pro)',
    '192.168.0.115': 'Watch.Home (Apple Watch)',
    '192.168.0.124': 'node-03.Home (Compute Node 03)',
    '192.168.0.125': 'node-05.Home (Compute Node 05)',
    '192.168.0.126': 'odooo-and-jupyter.Home (Odoo & Jupyter VM)',
    '192.168.0.131': 'login-01.Home (CentOS 9 Login Node)',
    '192.168.0.133': 'login-02.Home (CentOS Login Node 02)',
    '192.168.0.134': 'exch-01.Home (Exchange Mail Server VM)',
    '192.168.0.135': 'Chami-Home-PC.Home (Desktop PC)',
    '192.168.0.139': 'iPhone-97.Home (Apple iPhone)',
    '192.168.0.144': 'TOSHIBA-TV.Home (Toshiba Smart TV)',
    '192.168.0.145': 'RSLCM02.Home (VMware Lifecycle Manager VM)',
    '192.168.0.146': 'node-06.Home (Compute Node 06)',
    '192.168.0.159': 'Galaxy-A32.Home (Samsung Galaxy A32)',
    '192.168.0.170': 'node-01.Home (Compute Node 01)',
    '192.168.0.171': 'EPSON691DE7.Home (Epson Network Printer)',
    '192.168.0.180': 'Galaxy-A05s.Home (Samsung Galaxy A05s)',
    '192.168.0.183': 'WIN-ULQP7OEENNM.Home (Windows Workstation)',
    '192.168.0.197': 'RALSPMAC-G92FWQ.Home (Mac Client)',
    '192.168.0.200': 'esxi-01.npcsolutions.co.za (VMware ESXi Hypervisor)',
    '192.168.0.202': 'WIN-3L06EEP1J61.Home (Windows Workstation)',
    '192.168.0.203': 'MacBook-Pro-92.Home (Apple MacBook Pro)',
    '192.168.0.218': 'docker.npcsolutions.co.uk (Docker Server)',
    '192.168.0.219': 'docker-02.Home (Docker Secondary Server)',
    '192.168.0.222': 'DESKTOP-T96SGVI.Home (Windows Desktop PC)',
    '192.168.0.223': 'exchng-02.Home (Exchange Server 02 VM)',
    '192.168.0.227': 'node-04.Home (Compute Node 04)',
    '192.168.0.229': 'mbanjec-OptiPlex-3020M-7.Home (OptiPlex 7)',
    '192.168.0.234': 'ubuntu-server.Home (Ubuntu Server)',
    '192.168.0.235': 'ubuntutest.Home (Ubuntu Test VM)',
    '192.168.0.236': 'ubuntu-server-24.Home (Ubuntu Server 24)',
    '192.168.0.237': 'sql.Home (SQL Database Server 2022 VM)',
    '192.168.0.238': 'ubuntu-server-27.Home (Ubuntu Server 27)',
    '1.1.1.1': 'one.one.one.one (Cloudflare DNS)',
    '8.8.8.8': 'dns.google'
}

dns_cache = {}
if os.path.isfile(DNS_CACHE_FILE):
    try:
        with open(DNS_CACHE_FILE, 'r') as f:
            dns_cache = json.load(f)
    except Exception:
        dns_cache = {}

def resolve_ip(ip):
    if not ip or ip in ("0.0.0.0", "255.255.255.255", "::"):
        return ""
    if ip in KNOWN_HOSTS:
        return KNOWN_HOSTS[ip]
    if ip in dns_cache:
        return dns_cache[ip]
    try:
        socket.setdefaulttimeout(0.3)
        name = socket.gethostbyaddr(ip)[0]
        dns_cache[ip] = name
        return name
    except Exception:
        dns_cache[ip] = ""
        return ""

def save_dns_cache():
    try:
        with open(DNS_CACHE_FILE, 'w') as f:
            json.dump(dns_cache, f, indent=2)
    except Exception:
        pass

def parse_pcap(filepath):
    flows = defaultdict(lambda: {
        'first_seen': None,
        'last_seen': None,
        'bytes_sent': 0,
        'bytes_recv': 0,
        'pkts_sent': 0,
        'pkts_recv': 0,
        'peers': set(),
        'ports': set()
    })
    
    try:
        with open(filepath, 'rb') as f:
            ghdr = f.read(24)
            if len(ghdr) < 24:
                return flows
            magic = struct.unpack('<I', ghdr[:4])[0]
            if magic in (0xa1b2c3d4, 0xa1b23c4d):
                endian = '<'
            elif magic in (0xd4c3b2a1, 0x4d3cb2a1):
                endian = '>'
            else:
                return flows
            
            while True:
                phdr = f.read(16)
                if len(phdr) < 16:
                    break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(f'{endian}IIII', phdr)
                pkt_data = f.read(incl_len)
                if len(pkt_data) < 14:
                    continue
                
                pkt_time = ts_sec + (ts_usec / 1000000.0)
                
                # Ethernet
                eth_proto = struct.unpack('!H', pkt_data[12:14])[0]
                offset = 14
                if eth_proto == 0x8100: # 802.1Q VLAN
                    if len(pkt_data) < 18:
                        continue
                    eth_proto = struct.unpack('!H', pkt_data[16:18])[0]
                    offset = 18
                
                src_ip = None
                dst_ip = None
                app = 'Other'
                payload_len = orig_len
                sport = 0
                dport = 0
                
                if eth_proto == 0x0800: # IPv4
                    if len(pkt_data) < offset + 20:
                        continue
                    ip_hdr = pkt_data[offset:offset+20]
                    v_ihl, tos, tot_len, ip_id, flags_frag, ttl, proto, csum, src_b, dst_b = struct.unpack('!BBHHHBBH4s4s', ip_hdr)
                    ihl = (v_ihl & 0x0f) * 4
                    src_ip = socket.inet_ntoa(src_b)
                    dst_ip = socket.inet_ntoa(dst_b)
                    l4_offset = offset + ihl
                    
                    if proto == 6: # TCP
                        if len(pkt_data) >= l4_offset + 20:
                            sport, dport = struct.unpack('!HH', pkt_data[l4_offset:l4_offset+4])
                            p = dport if dport in PORT_MAP else sport
                            app = PORT_MAP.get(p, f'TCP/{min(sport, dport)}')
                    elif proto == 17: # UDP
                        if len(pkt_data) >= l4_offset + 8:
                            sport, dport = struct.unpack('!HH', pkt_data[l4_offset:l4_offset+4])
                            p = dport if dport in PORT_MAP else sport
                            app = PORT_MAP.get(p, f'UDP/{min(sport, dport)}')
                    elif proto == 1:
                        app = 'ICMP'
                    elif proto == 2:
                        app = 'IGMP'
                    else:
                        app = f'IPv4-Proto-{proto}'
                        
                elif eth_proto == 0x86dd: # IPv6
                    if len(pkt_data) < offset + 40:
                        continue
                    v_tc_fl, plen, nxt_hdr, hop_lim, src_b6, dst_b6 = struct.unpack('!IHBB16s16s', pkt_data[offset:offset+40])
                    src_ip = socket.inet_ntop(socket.AF_INET6, src_b6)
                    dst_ip = socket.inet_ntop(socket.AF_INET6, dst_b6)
                    l4_offset = offset + 40
                    if nxt_hdr == 6 and len(pkt_data) >= l4_offset + 4:
                        sport, dport = struct.unpack('!HH', pkt_data[l4_offset:l4_offset+4])
                        p = dport if dport in PORT_MAP else sport
                        app = PORT_MAP.get(p, f'TCP6/{min(sport, dport)}')
                    elif nxt_hdr == 17 and len(pkt_data) >= l4_offset + 4:
                        sport, dport = struct.unpack('!HH', pkt_data[l4_offset:l4_offset+4])
                        p = dport if dport in PORT_MAP else sport
                        app = PORT_MAP.get(p, f'UDP6/{min(sport, dport)}')
                    elif nxt_hdr == 58:
                        app = 'ICMPv6'
                    else:
                        app = f'IPv6-Proto-{nxt_hdr}'
                        
                elif eth_proto == 0x0806: # ARP
                    if len(pkt_data) >= offset + 28:
                        arp_hdr = pkt_data[offset:offset+28]
                        hw_type, p_type, hw_len, p_len, op, smac, sip_b, dmac, dip_b = struct.unpack('!HHBBH6s4s6s4s', arp_hdr)
                        src_ip = socket.inet_ntoa(sip_b)
                        dst_ip = socket.inet_ntoa(dip_b)
                        app = 'ARP'
                
                if src_ip and dst_ip and src_ip != '0.0.0.0' and dst_ip != '0.0.0.0':
                    # Source stats
                    k_src = (src_ip, app)
                    s = flows[k_src]
                    if s['first_seen'] is None or pkt_time < s['first_seen']: s['first_seen'] = pkt_time
                    if s['last_seen'] is None or pkt_time > s['last_seen']: s['last_seen'] = pkt_time
                    s['bytes_sent'] += payload_len
                    s['pkts_sent'] += 1
                    s['peers'].add(dst_ip)
                    if sport: s['ports'].add(sport)
                    if dport: s['ports'].add(dport)
                    
                    # Dest stats
                    k_dst = (dst_ip, app)
                    d = flows[k_dst]
                    if d['first_seen'] is None or pkt_time < d['first_seen']: d['first_seen'] = pkt_time
                    if d['last_seen'] is None or pkt_time > d['last_seen']: d['last_seen'] = pkt_time
                    d['bytes_recv'] += payload_len
                    d['pkts_recv'] += 1
                    d['peers'].add(src_ip)
                    if sport: d['ports'].add(sport)
                    if dport: d['ports'].add(dport)

    except Exception as e:
        print(f'Error parsing {filepath}: {e}', file=sys.stderr)
        
    return flows

def update_device_records(flows, pcap_name):
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_map = defaultdict(dict)
    
    for (ip, app), metrics in flows.items():
        device_map[ip][app] = metrics
        
    for ip, app_dict in device_map.items():
        hostname = resolve_ip(ip)
        dev_dir = os.path.join(DEVICES_DIR, ip.replace(':', '_'))
        os.makedirs(dev_dir, exist_ok=True)
        
        # 1. Update Detailed CSV Log
        log_csv = os.path.join(dev_dir, "traffic_log.csv")
        file_exists = os.path.isfile(log_csv)
        with open(log_csv, 'a', newline='') as f:
            w = csv.writer(f)
            if not file_exists:
                w.writerow(["Timestamp", "Device_IP", "Hostname", "Application", "Duration_Sec", 
                            "Bytes_Sent", "Bytes_Recv", "Total_Bytes", 
                            "Packets_Sent", "Packets_Recv", "Total_Packets", "Unique_Peers"])
            for app, m in app_dict.items():
                dur = round(m['last_seen'] - m['first_seen'], 3) if m['first_seen'] else 0
                w.writerow([
                    timestamp_str, ip, hostname, app, dur,
                    m['bytes_sent'], m['bytes_recv'], m['bytes_sent'] + m['bytes_recv'],
                    m['pkts_sent'], m['pkts_recv'], m['pkts_sent'] + m['pkts_recv'],
                    len(m['peers'])
                ])
                
        # 2. Update Device Summary JSON
        summary_json_file = os.path.join(dev_dir, "summary.json")
        existing_summary = {}
        if os.path.isfile(summary_json_file):
            try:
                with open(summary_json_file, 'r') as f:
                    existing_summary = json.load(f)
            except:
                existing_summary = {}
                
        if 'applications' not in existing_summary:
            existing_summary = {
                'device_ip': ip,
                'hostname': hostname,
                'last_updated': timestamp_str,
                'total_bytes': 0,
                'total_packets': 0,
                'applications': {}
            }
            
        existing_summary['hostname'] = hostname or existing_summary.get('hostname', '')
        existing_summary['last_updated'] = timestamp_str
        for app, m in app_dict.items():
            if app not in existing_summary['applications']:
                existing_summary['applications'][app] = {
                    'total_bytes': 0,
                    'bytes_sent': 0,
                    'bytes_recv': 0,
                    'total_packets': 0,
                    'unique_peers': []
                }
            app_rec = existing_summary['applications'][app]
            app_rec['bytes_sent'] += m['bytes_sent']
            app_rec['bytes_recv'] += m['bytes_recv']
            app_rec['total_bytes'] += (m['bytes_sent'] + m['bytes_recv'])
            app_rec['total_packets'] += (m['pkts_sent'] + m['pkts_recv'])
            all_peers = set(app_rec.get('unique_peers', [])).union(m['peers'])
            app_rec['unique_peers'] = sorted(list(all_peers))[:50]
            
            existing_summary['total_bytes'] += (m['bytes_sent'] + m['bytes_recv'])
            existing_summary['total_packets'] += (m['pkts_sent'] + m['pkts_recv'])
            
        with open(summary_json_file, 'w') as f:
            json.dump(existing_summary, f, indent=2)

    # 3. Update Global Subnet Summary
    global_csv = os.path.join(BASE_DIR, "subnet_summary.csv")
    global_exists = os.path.isfile(global_csv)
    with open(global_csv, 'a', newline='') as f:
        w = csv.writer(f)
        if not global_exists:
            w.writerow(["Timestamp", "PCAP_File", "Active_Devices_Count", "Total_Flows", "Total_Bytes"])
        total_b = sum(m['bytes_sent'] for m in flows.values())
        w.writerow([timestamp_str, os.path.basename(pcap_name), len(device_map), len(flows), total_b])

    save_dns_cache()

MAX_STORAGE_BYTES = 10 * 1024 * 1024 * 1024 # 10 GB

def check_and_enforce_retention():
    try:
        total_size = 0
        for root, dirs, files in os.walk(BASE_DIR):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total_size += os.path.getsize(fp)
                except Exception:
                    pass
                    
        if total_size > MAX_STORAGE_BYTES:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Storage ({total_size / (1024**3):.2f} GB) exceeded 10GB limit. Purging oldest logs & pcaps...")
            for pcap in glob.glob(os.path.join(RAW_DIR, "*.pcap")):
                try:
                    os.remove(pcap)
                except Exception:
                    pass
                    
            for csv_file in glob.glob(os.path.join(DEVICES_DIR, "*", "*.csv")) + [os.path.join(BASE_DIR, "subnet_summary.csv")]:
                if os.path.isfile(csv_file):
                    try:
                        with open(csv_file, 'r') as f:
                            lines = f.readlines()
                        if len(lines) > 5000:
                            header = lines[0]
                            kept = lines[-2500:]
                            with open(csv_file, 'w') as f:
                                f.write(header)
                                f.writelines(kept)
                    except Exception:
                        pass
    except Exception as e:
        print(f"Error enforcing retention: {e}", file=sys.stderr)

def main():
    pcaps = sorted(glob.glob(os.path.join(RAW_DIR, "*.pcap")))
    now = time.time()
    for pcap in pcaps:
        try:
            mtime = os.path.getmtime(pcap)
            if now - mtime < 3:
                continue
            flows = parse_pcap(pcap)
            if flows:
                update_device_records(flows, pcap)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processed {pcap} ({len(flows)} flows)")
            os.remove(pcap)
        except Exception as e:
            print(f"Error processing {pcap}: {e}")
            
    check_and_enforce_retention()

if __name__ == '__main__':
    main()

