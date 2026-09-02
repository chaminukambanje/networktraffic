#!/usr/bin/env python3
"""
Subnet & Docker Network Traffic Dashboard Web Application
Serves interactive real-time telemetry, charts, resolved hostnames, and per-device metrics.
"""

import os
import sys
import glob
import json
import csv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

BASE_DIR = os.environ.get("DATA_DIR", "/mnt/pool1/network_traffic")
DEVICES_DIR = os.path.join(BASE_DIR, "devices")
PORT = int(os.environ.get("PORT", 8500))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subnet & Docker Network Traffic Telemetry</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 50: '#eef2ff', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca', 900: '#312e81' }
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        .glass-card { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .scrollbar-slim::-webkit-scrollbar { width: 6px; height: 6px; }
        .scrollbar-slim::-webkit-scrollbar-track { background: #111827; }
        .scrollbar-slim::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
    </style>
</head>
<body class="text-slate-100 min-h-screen pb-12">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 sticky top-0 z-50 backdrop-blur">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                </div>
                <div>
                    <h1 class="text-lg font-bold text-white flex items-center gap-2">
                        Subnet Traffic Telemetry
                        <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> LIVE
                        </span>
                    </h1>
                    <p class="text-xs text-slate-400">Hostname Resolution &bull; ESXi SPAN &bull; Docker Focus</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <span id="lastUpdate" class="text-xs text-slate-400">Updating...</span>
                <button onclick="fetchData()" class="px-3 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md transition">Refresh</button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 space-y-6">
        <!-- Top KPI Summary Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="glass-card p-5 rounded-xl">
                <div class="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Subnet Traffic</div>
                <div id="kpiTotalBytes" class="text-2xl font-extrabold text-white mt-2">--</div>
                <div id="kpiTotalPackets" class="text-xs text-slate-400 mt-1">-- packets</div>
            </div>
            <div class="glass-card p-5 rounded-xl border-indigo-500/40 bg-gradient-to-br from-indigo-950/40 to-slate-900/40">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-medium text-indigo-300 uppercase tracking-wider">docker.npcsolutions.co.uk</span>
                    <span class="px-1.5 py-0.5 text-[10px] bg-indigo-500/30 text-indigo-300 rounded font-bold">192.168.0.218</span>
                </div>
                <div id="kpiDockerBytes" class="text-2xl font-extrabold text-indigo-300 mt-2">--</div>
                <div id="kpiDockerPackets" class="text-xs text-indigo-400/80 mt-1">-- packets</div>
            </div>
            <div class="glass-card p-5 rounded-xl">
                <div class="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Resolved Devices</div>
                <div id="kpiActiveDevices" class="text-2xl font-extrabold text-white mt-2">--</div>
                <div class="text-xs text-emerald-400 mt-1 flex items-center gap-1">
                    <span>&bull;</span> Monitored with DNS Lookups
                </div>
            </div>
            <div class="glass-card p-5 rounded-xl">
                <div class="text-xs font-medium text-slate-400 uppercase tracking-wider">Top Application</div>
                <div id="kpiTopApp" class="text-2xl font-extrabold text-white mt-2">--</div>
                <div id="kpiTopAppBytes" class="text-xs text-slate-400 mt-1">--</div>
            </div>
        </div>

        <!-- Docker Server Focus Card -->
        <div class="glass-card p-6 rounded-xl border-indigo-500/40">
            <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-2">
                <div>
                    <h2 class="text-base font-bold text-white flex items-center gap-2">
                        <svg class="w-5 h-5 text-indigo-400" fill="currentColor" viewBox="0 0 24 24"><path d="M13.983 11.078h2.119a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186h-2.119a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.954-5.43h2.118a.186.186 0 00.186-.186V3.574a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.186.185.186m0 2.714h2.118a.186.186 0 00.186-.185V6.289a.186.186 0 00-.186-.185h-2.118a.185.185 0 00-.185.185v1.888c0 .102.082.185.185.185m-2.953 0h2.118a.186.186 0 00.186-.185V6.289a.186.186 0 00-.186-.185H8.076a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m0 2.716h2.118a.186.186 0 00.186-.185V9.006a.186.186 0 00-.186-.186H8.076a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m-2.954 0h2.119a.186.186 0 00.185-.185V9.006a.185.185 0 00-.185-.186H5.122a.185.185 0 00-.185.185v1.888c0 .102.083.185.185.185m17.654 1.954c-.61-.397-1.785-.52-2.734-.338-.204-.76-.641-1.397-1.282-1.898-.59-.462-1.334-.73-2.146-.777a.186.186 0 00-.197.185v1.077c0 .102.083.185.185.185.58.035 1.114.232 1.54.569.458.361.765.836.883 1.373a.186.186 0 00.18.146c1.036.033 1.99.23 2.68.563.856.415 1.34 1.02 1.34 1.678 0 1.096-1.385 2.146-3.8 2.502-.27.04-.545.068-.824.085a.186.186 0 00-.174.185v.068a11.95 11.95 0 01-1.043.045c-2.31 0-4.43-.538-6.13-1.554-1.306-.78-2.26-1.815-2.83-2.996a.186.186 0 00-.168-.106H2.122a.186.186 0 00-.185.185c0 3.23 2.66 5.86 5.928 5.86 1.83 0 3.52-.83 4.67-2.16 1.15 1.33 2.84 2.16 4.67 2.16 3.65 0 6.62-2.94 6.62-6.55 0-1.04-.26-2.03-.73-2.895"/></svg>
                        Docker Server &bull; docker.npcsolutions.co.uk
                    </h2>
                    <p class="text-xs text-slate-400 mt-0.5">IP: 192.168.0.218 &bull; Ubuntu Linux 26.04</p>
                </div>
                <div id="dockerBandwidthSummary" class="flex items-center gap-4 text-xs">
                    <div>Sent: <span id="dockerSent" class="font-bold text-slate-200">--</span></div>
                    <div>Recv: <span id="dockerRecv" class="font-bold text-slate-200">--</span></div>
                </div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
                <!-- Docker Chart -->
                <div class="h-64 flex items-center justify-center">
                    <canvas id="dockerAppChart"></canvas>
                </div>
                <!-- Docker App List Table -->
                <div class="lg:col-span-2 overflow-x-auto scrollbar-slim max-h-64">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-[11px] uppercase bg-slate-800/60 text-slate-400 sticky top-0">
                            <tr>
                                <th class="py-2 px-3">Application</th>
                                <th class="py-2 px-3">Total Volume</th>
                                <th class="py-2 px-3">Packets</th>
                                <th class="py-2 px-3">Connected Peers</th>
                            </tr>
                        </thead>
                        <tbody id="dockerAppTable" class="divide-y divide-slate-800/60">
                            <tr><td colspan="4" class="py-4 text-center text-slate-500">Loading Docker telemetry...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Global Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Top Devices Chart -->
            <div class="glass-card p-5 rounded-xl">
                <h3 class="text-sm font-bold text-slate-200 mb-4">Top Devices by Volume (Resolved Hostnames)</h3>
                <div class="h-64">
                    <canvas id="topDevicesChart"></canvas>
                </div>
            </div>
            <!-- Protocol Distribution -->
            <div class="glass-card p-5 rounded-xl">
                <h3 class="text-sm font-bold text-slate-200 mb-4">Subnet Application Protocols</h3>
                <div class="h-64">
                    <canvas id="subnetAppChart"></canvas>
                </div>
            </div>
        </div>

        <!-- All Devices Table -->
        <div class="glass-card rounded-xl overflow-hidden">
            <div class="p-4 border-b border-slate-800 flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                <div>
                    <h3 class="text-sm font-bold text-white">All Discovered Devices & Hostnames</h3>
                    <p class="text-xs text-slate-400">DNS Resolved Name, IP Address, Traffic Volume, and Active Applications</p>
                </div>
                <input type="text" id="deviceFilter" onkeyup="filterDevices()" placeholder="Search Hostname, IP or App..." class="px-3 py-1.5 bg-slate-800/80 border border-slate-700 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-64">
            </div>
            <div class="overflow-x-auto scrollbar-slim max-h-96">
                <table class="w-full text-left text-xs text-slate-300">
                    <thead class="text-[11px] uppercase bg-slate-800 text-slate-400 sticky top-0">
                        <tr>
                            <th class="py-2.5 px-4">Resolved Hostname / IP</th>
                            <th class="py-2.5 px-4">Total Volume</th>
                            <th class="py-2.5 px-4">Sent / Recv</th>
                            <th class="py-2.5 px-4">Packets</th>
                            <th class="py-2.5 px-4">Applications</th>
                            <th class="py-2.5 px-4">Last Activity</th>
                        </tr>
                    </thead>
                    <tbody id="devicesTableBody" class="divide-y divide-slate-800">
                        <tr><td colspan="6" class="py-6 text-center text-slate-500">Ingesting device data...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        let dockerChart = null;
        let topDevicesChart = null;
        let subnetAppChart = null;
        let allDevicesCache = [];

        function formatBytes(bytes) {
            if (!bytes || bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        async function fetchData() {
            try {
                const res = await fetch('/api/devices');
                const data = await res.json();
                allDevicesCache = data.devices || [];
                
                document.getElementById('lastUpdate').innerText = 'Last Sync: ' + new Date().toLocaleTimeString();
                
                updateKPIs(data);
                updateDockerSection(data.devices);
                updateCharts(data.devices);
                renderDevicesTable(allDevicesCache);
            } catch (err) {
                console.error('Failed fetching telemetry:', err);
            }
        }

        function updateKPIs(data) {
            let totalBytes = 0;
            let totalPackets = 0;
            const appTotals = {};

            data.devices.forEach(d => {
                totalBytes += (d.total_bytes || 0);
                totalPackets += (d.total_packets || 0);
                if (d.applications) {
                    Object.entries(d.applications).forEach(([app, metrics]) => {
                        appTotals[app] = (appTotals[app] || 0) + (metrics.total_bytes || 0);
                    });
                }
            });

            document.getElementById('kpiTotalBytes').innerText = formatBytes(totalBytes);
            document.getElementById('kpiTotalPackets').innerText = totalPackets.toLocaleString() + ' packets';
            document.getElementById('kpiActiveDevices').innerText = data.devices.length;

            let topApp = '--';
            let topAppB = 0;
            Object.entries(appTotals).forEach(([app, bytes]) => {
                if (bytes > topAppB) {
                    topAppB = bytes;
                    topApp = app;
                }
            });
            document.getElementById('kpiTopApp').innerText = topApp;
            document.getElementById('kpiTopAppBytes').innerText = formatBytes(topAppB);
        }

        function updateDockerSection(devices) {
            const docker = devices.find(d => d.device_ip === '192.168.0.218');
            if (!docker) return;

            document.getElementById('kpiDockerBytes').innerText = formatBytes(docker.total_bytes);
            document.getElementById('kpiDockerPackets').innerText = (docker.total_packets || 0).toLocaleString() + ' packets';

            let totalSent = 0;
            let totalRecv = 0;
            const appLabels = [];
            const appData = [];
            let tableHtml = '';

            if (docker.applications) {
                const sortedApps = Object.entries(docker.applications).sort((a,b) => b[1].total_bytes - a[1].total_bytes);
                sortedApps.forEach(([app, m]) => {
                    totalSent += (m.bytes_sent || 0);
                    totalRecv += (m.bytes_recv || 0);
                    appLabels.push(app);
                    appData.push(m.total_bytes);

                    tableHtml += `<tr>
                        <td class="py-2 px-3 font-semibold text-white">${app}</td>
                        <td class="py-2 px-3">${formatBytes(m.total_bytes)}</td>
                        <td class="py-2 px-3">${(m.total_packets || 0).toLocaleString()}</td>
                        <td class="py-2 px-3 text-slate-400">${m.unique_peers ? m.unique_peers.length : 0} peers</td>
                    </tr>`;
                });
            }

            document.getElementById('dockerSent').innerText = formatBytes(totalSent);
            document.getElementById('dockerRecv').innerText = formatBytes(totalRecv);
            document.getElementById('dockerAppTable').innerHTML = tableHtml || '<tr><td colspan="4" class="py-2 text-center">No active apps</td></tr>';

            const ctx = document.getElementById('dockerAppChart').getContext('2d');
            if (dockerChart) dockerChart.destroy();
            dockerChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: appLabels.slice(0, 6),
                    datasets: [{
                        data: appData.slice(0, 6),
                        backgroundColor: ['#6366f1', '#38bdf8', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#cbd5e1', font: { size: 10 } } }
                    }
                }
            });
        }

        function updateCharts(devices) {
            const sortedDevices = [...devices].sort((a,b) => b.total_bytes - a.total_bytes).slice(0, 7);
            const devCtx = document.getElementById('topDevicesChart').getContext('2d');
            if (topDevicesChart) topDevicesChart.destroy();
            topDevicesChart = new Chart(devCtx, {
                type: 'bar',
                data: {
                    labels: sortedDevices.map(d => (d.hostname ? d.hostname.split('.')[0] : d.device_ip)),
                    datasets: [{
                        label: 'Total Bytes',
                        data: sortedDevices.map(d => d.total_bytes),
                        backgroundColor: sortedDevices.map(d => d.device_ip === '192.168.0.218' ? '#6366f1' : '#38bdf8')
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                        y: { ticks: { color: '#94a3b8', callback: v => formatBytes(v) }, grid: { color: '#1e293b' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });

            const subnetApps = {};
            devices.forEach(d => {
                if (d.applications) {
                    Object.entries(d.applications).forEach(([app, m]) => {
                        subnetApps[app] = (subnetApps[app] || 0) + m.total_bytes;
                    });
                }
            });
            const sortedSubnetApps = Object.entries(subnetApps).sort((a,b) => b[1] - a[1]).slice(0, 6);
            const appCtx = document.getElementById('subnetAppChart').getContext('2d');
            if (subnetAppChart) subnetAppChart.destroy();
            subnetAppChart = new Chart(appCtx, {
                type: 'pie',
                data: {
                    labels: sortedSubnetApps.map(a => a[0]),
                    datasets: [{
                        data: sortedSubnetApps.map(a => a[1]),
                        backgroundColor: ['#10b981', '#6366f1', '#f59e0b', '#38bdf8', '#ec4899', '#94a3b8']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'right', labels: { color: '#cbd5e1', font: { size: 10 } } } }
                }
            });
        }

        function renderDevicesTable(devices) {
            let html = '';
            devices.sort((a,b) => (b.total_bytes || 0) - (a.total_bytes || 0)).forEach(d => {
                const isDocker = d.device_ip === '192.168.0.218';
                let topAppBadges = '';
                let sent = 0, recv = 0;
                if (d.applications) {
                    Object.entries(d.applications).forEach(([app, m]) => {
                        sent += (m.bytes_sent || 0);
                        recv += (m.bytes_recv || 0);
                    });
                    const topA = Object.keys(d.applications).slice(0, 3);
                    topAppBadges = topA.map(a => `<span class="px-1.5 py-0.5 text-[10px] bg-slate-700 text-slate-300 rounded">${a}</span>`).join(' ');
                }

                const hostDisplay = d.hostname ? `<div class="font-bold text-white">${d.hostname}</div><div class="text-[11px] font-mono text-slate-400">${d.device_ip}</div>` : `<div class="font-mono font-medium text-white">${d.device_ip}</div>`;

                html += `<tr class="hover:bg-slate-800/50 ${isDocker ? 'bg-indigo-950/20' : ''}">
                    <td class="py-2.5 px-4">
                        ${hostDisplay} ${isDocker ? '<span class="inline-block mt-0.5 text-[10px] px-1 bg-indigo-500/30 text-indigo-300 rounded font-bold">DOCKER SERVER</span>' : ''}
                    </td>
                    <td class="py-2.5 px-4 font-bold text-indigo-200">${formatBytes(d.total_bytes)}</td>
                    <td class="py-2.5 px-4 text-slate-400">${formatBytes(sent)} / ${formatBytes(recv)}</td>
                    <td class="py-2.5 px-4 text-slate-400">${(d.total_packets || 0).toLocaleString()}</td>
                    <td class="py-2.5 px-4 flex gap-1 flex-wrap">${topAppBadges || '--'}</td>
                    <td class="py-2.5 px-4 text-slate-400 text-[11px]">${d.last_updated || '--'}</td>
                </tr>`;
            });
            document.getElementById('devicesTableBody').innerHTML = html || '<tr><td colspan="6" class="py-4 text-center">No devices found</td></tr>';
        }

        function filterDevices() {
            const query = document.getElementById('deviceFilter').value.toLowerCase();
            const filtered = allDevicesCache.filter(d => {
                const ipMatch = d.device_ip.toLowerCase().includes(query);
                const hostMatch = d.hostname && d.hostname.toLowerCase().includes(query);
                const appMatch = d.applications && Object.keys(d.applications).some(a => a.toLowerCase().includes(query));
                return ipMatch || hostMatch || appMatch;
            });
            renderDevicesTable(filtered);
        }

        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>
"""

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
            return
            
        elif parsed.path == "/api/devices":
            device_dirs = sorted(glob.glob(os.path.join(DEVICES_DIR, "*")))
            devices = []
            for d in device_dirs:
                if not os.path.isdir(d): continue
                summary_file = os.path.join(d, "summary.json")
                if os.path.isfile(summary_file):
                    try:
                        with open(summary_file, 'r') as f:
                            data = json.load(f)
                            devices.append(data)
                    except:
                        pass
                        
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"devices": devices}).encode('utf-8'))
            return
            
        elif parsed.path.startswith("/api/device/"):
            target_ip = parsed.path.replace("/api/device/", "").replace(":", "_")
            summary_file = os.path.join(DEVICES_DIR, target_ip, "summary.json")
            if os.path.isfile(summary_file):
                with open(summary_file, 'r') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
            return
            
        else:
            self.send_response(404)
            self.end_headers()

def run():
    server = HTTPServer(('0.0.0.0', PORT), DashboardHandler)
    print(f"Dashboard server running on http://0.0.0.0:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    run()
