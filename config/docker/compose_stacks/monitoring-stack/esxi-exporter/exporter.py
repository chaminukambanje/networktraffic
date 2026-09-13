import os
import ssl
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from prometheus_client import CollectorRegistry, Gauge, generate_latest

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ESXI_HOST = os.environ.get("ESXI_HOST", "192.168.0.200")
ESXI_USER = os.environ.get("ESXI_USER", "root")
ESXI_PASS = os.environ.get("ESXI_PASS", "")
PORT = 9272

class ESXiCollector:
    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.si = None
        self.ssl_ctx = ssl._create_unverified_context()
        self.counter_map = {}

    def get_connection(self):
        try:
            if self.si:
                self.si.CurrentTime()
                return self.si
        except Exception:
            logging.info("Reconnecting to ESXi host...")
        
        try:
            self.si = SmartConnect(host=self.host, user=self.user, pwd=self.pwd, sslContext=self.ssl_ctx)
            content = self.si.RetrieveContent()
            perf_manager = content.perfManager
            self.counter_map = {c.key: f"{c.groupInfo.key}.{c.nameInfo.key}.{c.rollupType}" for c in perf_manager.perfCounter}
            return self.si
        except Exception as e:
            logging.error(f"Failed to connect to ESXi: {e}")
            self.si = None
            return None

    def collect(self):
        registry = CollectorRegistry()
        
        # Host gauges
        g_host_cpu_total_mhz = Gauge('esxi_host_cpu_total_mhz', 'Host total CPU capacity in MHz', ['host'], registry=registry)
        g_host_cpu_usage_mhz = Gauge('esxi_host_cpu_usage_mhz', 'Host used CPU in MHz', ['host'], registry=registry)
        g_host_cpu_usage_pct = Gauge('esxi_host_cpu_usage_percent', 'Host CPU usage percentage', ['host'], registry=registry)
        g_host_mem_total_bytes = Gauge('esxi_host_memory_total_bytes', 'Host total memory in bytes', ['host'], registry=registry)
        g_host_mem_usage_bytes = Gauge('esxi_host_memory_usage_bytes', 'Host used memory in bytes', ['host'], registry=registry)
        g_host_mem_usage_pct = Gauge('esxi_host_memory_usage_percent', 'Host memory usage percentage', ['host'], registry=registry)
        g_host_uptime_seconds = Gauge('esxi_host_uptime_seconds', 'Host uptime in seconds', ['host'], registry=registry)
        
        # Datastore gauges
        g_ds_capacity_bytes = Gauge('esxi_datastore_capacity_bytes', 'Datastore capacity in bytes', ['datastore', 'type'], registry=registry)
        g_ds_free_bytes = Gauge('esxi_datastore_free_bytes', 'Datastore free space in bytes', ['datastore', 'type'], registry=registry)
        g_ds_used_bytes = Gauge('esxi_datastore_used_bytes', 'Datastore used space in bytes', ['datastore', 'type'], registry=registry)
        g_ds_usage_pct = Gauge('esxi_datastore_usage_percent', 'Datastore usage percentage', ['datastore', 'type'], registry=registry)
        
        # VM gauges
        g_vm_power = Gauge('esxi_vm_power_state', 'VM power state (1=on, 0=off)', ['vm', 'guest_os', 'ip', 'hostname', 'tools_status'], registry=registry)
        g_vm_num_cpu = Gauge('esxi_vm_num_cpu', 'Number of allocated vCPUs', ['vm'], registry=registry)
        g_vm_mem_allocated_bytes = Gauge('esxi_vm_memory_allocated_bytes', 'Allocated RAM in bytes', ['vm'], registry=registry)
        g_vm_cpu_usage_mhz = Gauge('esxi_vm_cpu_usage_mhz', 'VM CPU usage in MHz', ['vm'], registry=registry)
        g_vm_cpu_usage_pct = Gauge('esxi_vm_cpu_usage_percent', 'VM CPU usage estimated percent of assigned cores', ['vm'], registry=registry)
        g_vm_guest_mem_bytes = Gauge('esxi_vm_guest_memory_usage_bytes', 'Guest OS active RAM usage in bytes', ['vm'], registry=registry)
        g_vm_host_mem_bytes = Gauge('esxi_vm_host_memory_usage_bytes', 'Host consumed RAM for VM in bytes', ['vm'], registry=registry)
        g_vm_mem_usage_pct = Gauge('esxi_vm_memory_usage_percent', 'Guest RAM usage percentage', ['vm'], registry=registry)
        g_vm_uptime_seconds = Gauge('esxi_vm_uptime_seconds', 'VM uptime in seconds', ['vm'], registry=registry)
        
        # VM Traffic & Disk IO Real-time throughput
        g_vm_net_rx_bytes_sec = Gauge('esxi_vm_network_receive_bytes_per_second', 'VM network receive throughput in bytes/s', ['vm'], registry=registry)
        g_vm_net_tx_bytes_sec = Gauge('esxi_vm_network_transmit_bytes_per_second', 'VM network transmit throughput in bytes/s', ['vm'], registry=registry)
        g_vm_disk_read_bytes_sec = Gauge('esxi_vm_disk_read_bytes_per_second', 'VM disk read throughput in bytes/s', ['vm'], registry=registry)
        g_vm_disk_write_bytes_sec = Gauge('esxi_vm_disk_write_bytes_per_second', 'VM disk write throughput in bytes/s', ['vm'], registry=registry)

        # VM Disk partition gauges
        g_vm_disk_capacity = Gauge('esxi_vm_disk_capacity_bytes', 'VM guest disk capacity in bytes', ['vm', 'disk_path'], registry=registry)
        g_vm_disk_free = Gauge('esxi_vm_disk_free_bytes', 'VM guest disk free space in bytes', ['vm', 'disk_path'], registry=registry)
        g_vm_disk_used = Gauge('esxi_vm_disk_used_bytes', 'VM guest disk used space in bytes', ['vm', 'disk_path'], registry=registry)
        g_vm_disk_usage_pct = Gauge('esxi_vm_disk_usage_percent', 'VM guest disk usage percent', ['vm', 'disk_path'], registry=registry)
        
        # VM Network interface gauges
        g_vm_net_connected = Gauge('esxi_vm_network_connected', 'VM network interface connected state', ['vm', 'network', 'mac', 'ip'], registry=registry)

        si = self.get_connection()
        if not si:
            return registry
            
        content = si.RetrieveContent()
        perf_manager = content.perfManager
        
        # 1. Collect Host Metrics
        host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        host_cpu_mhz_per_core = 2500
        for host in host_view.view:
            h_summary = host.summary
            h_name = h_summary.config.name
            h_quick = h_summary.quickStats
            h_hw = h_summary.hardware
            
            if h_hw:
                total_cpu_mhz = h_hw.cpuMhz * h_hw.numCpuCores
                total_mem_bytes = h_hw.memorySize
                if h_hw.numCpuCores > 0:
                    host_cpu_mhz_per_core = h_hw.cpuMhz
            else:
                total_cpu_mhz = 0
                total_mem_bytes = 0
                
            used_cpu_mhz = h_quick.overallCpuUsage or 0
            used_mem_bytes = (h_quick.overallMemoryUsage or 0) * 1024 * 1024
            uptime = h_quick.uptime or 0
            
            cpu_pct = (used_cpu_mhz / total_cpu_mhz * 100.0) if total_cpu_mhz > 0 else 0.0
            mem_pct = (used_mem_bytes / total_mem_bytes * 100.0) if total_mem_bytes > 0 else 0.0
            
            g_host_cpu_total_mhz.labels(host=h_name).set(total_cpu_mhz)
            g_host_cpu_usage_mhz.labels(host=h_name).set(used_cpu_mhz)
            g_host_cpu_usage_pct.labels(host=h_name).set(cpu_pct)
            g_host_mem_total_bytes.labels(host=h_name).set(total_mem_bytes)
            g_host_mem_usage_bytes.labels(host=h_name).set(used_mem_bytes)
            g_host_mem_usage_pct.labels(host=h_name).set(mem_pct)
            g_host_uptime_seconds.labels(host=h_name).set(uptime)
        host_view.Destroy()

        # 2. Collect Datastore Metrics
        ds_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)
        for ds in ds_view.view:
            try:
                ds_summary = ds.summary
                ds_name = ds_summary.name
                ds_type = ds_summary.type
                capacity = ds_summary.capacity or 0
                free_space = ds_summary.freeSpace or 0
                used_space = capacity - free_space
                pct = (used_space / capacity * 100.0) if capacity > 0 else 0.0
                
                g_ds_capacity_bytes.labels(datastore=ds_name, type=ds_type).set(capacity)
                g_ds_free_bytes.labels(datastore=ds_name, type=ds_type).set(free_space)
                g_ds_used_bytes.labels(datastore=ds_name, type=ds_type).set(used_space)
                g_ds_usage_pct.labels(datastore=ds_name, type=ds_type).set(pct)
            except Exception:
                pass
        ds_view.Destroy()

        # 3. Collect VM Metrics & Performance
        vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        perf_specs = []
        powered_on_vms = []

        for vm in vm_view.view:
            try:
                summary = vm.summary
                cfg = summary.config
                rt = summary.runtime
                quick = summary.quickStats
                guest = summary.guest
                
                vm_name = cfg.name
                is_on = 1 if rt.powerState == "poweredOn" else 0
                guest_os = cfg.guestFullName or "unknown"
                ip = (guest.ipAddress or "none") if guest else "none"
                hostname = (guest.hostName or "unknown") if guest else "unknown"
                tools_status = str(guest.toolsStatus) if guest else "toolsNotInstalled"
                
                g_vm_power.labels(
                    vm=vm_name,
                    guest_os=guest_os,
                    ip=ip,
                    hostname=hostname,
                    tools_status=tools_status
                ).set(is_on)
                
                num_cpu = cfg.numCpu or 1
                alloc_mem_mb = cfg.memorySizeMB or 0
                alloc_mem_bytes = alloc_mem_mb * 1024 * 1024
                
                g_vm_num_cpu.labels(vm=vm_name).set(num_cpu)
                g_vm_mem_allocated_bytes.labels(vm=vm_name).set(alloc_mem_bytes)
                
                if is_on and quick:
                    cpu_usage_mhz = quick.overallCpuUsage or 0
                    guest_mem_mb = quick.guestMemoryUsage or 0
                    host_mem_mb = quick.hostMemoryUsage or 0
                    uptime = quick.uptimeSeconds or 0
                    
                    vm_total_cpu_cap = num_cpu * host_cpu_mhz_per_core
                    vm_cpu_pct = (cpu_usage_mhz / vm_total_cpu_cap * 100.0) if vm_total_cpu_cap > 0 else 0.0
                    vm_mem_pct = (guest_mem_mb / alloc_mem_mb * 100.0) if alloc_mem_mb > 0 else 0.0
                    
                    g_vm_cpu_usage_mhz.labels(vm=vm_name).set(cpu_usage_mhz)
                    g_vm_cpu_usage_pct.labels(vm=vm_name).set(vm_cpu_pct)
                    g_vm_guest_mem_bytes.labels(vm=vm_name).set(guest_mem_mb * 1024 * 1024)
                    g_vm_host_mem_bytes.labels(vm=vm_name).set(host_mem_mb * 1024 * 1024)
                    g_vm_mem_usage_pct.labels(vm=vm_name).set(vm_mem_pct)
                    g_vm_uptime_seconds.labels(vm=vm_name).set(uptime)
                    
                    # Prepare for batch perf query
                    perf_specs.append(vim.PerformanceManager.QuerySpec(entity=vm, maxSample=1, intervalId=20))
                    powered_on_vms.append(vm_name)
                else:
                    g_vm_cpu_usage_mhz.labels(vm=vm_name).set(0)
                    g_vm_cpu_usage_pct.labels(vm=vm_name).set(0)
                    g_vm_guest_mem_bytes.labels(vm=vm_name).set(0)
                    g_vm_host_mem_bytes.labels(vm=vm_name).set(0)
                    g_vm_mem_usage_pct.labels(vm=vm_name).set(0)
                    g_vm_uptime_seconds.labels(vm=vm_name).set(0)
                    g_vm_net_rx_bytes_sec.labels(vm=vm_name).set(0)
                    g_vm_net_tx_bytes_sec.labels(vm=vm_name).set(0)
                    g_vm_disk_read_bytes_sec.labels(vm=vm_name).set(0)
                    g_vm_disk_write_bytes_sec.labels(vm=vm_name).set(0)

                # Disks
                if vm.guest and vm.guest.disk:
                    for d in vm.guest.disk:
                        disk_path = d.diskPath
                        cap = d.capacity or 0
                        free = d.freeSpace or 0
                        used = cap - free
                        pct = (used / cap * 100.0) if cap > 0 else 0.0
                        g_vm_disk_capacity.labels(vm=vm_name, disk_path=disk_path).set(cap)
                        g_vm_disk_free.labels(vm=vm_name, disk_path=disk_path).set(free)
                        g_vm_disk_used.labels(vm=vm_name, disk_path=disk_path).set(used)
                        g_vm_disk_usage_pct.labels(vm=vm_name, disk_path=disk_path).set(pct)
                
                # Networks
                if vm.guest and vm.guest.net:
                    for n in vm.guest.net:
                        net_name = n.network or "unknown"
                        mac = n.macAddress or "none"
                        net_ip = n.ipAddress[0] if (n.ipAddress and len(n.ipAddress) > 0) else "none"
                        conn = 1 if n.connected else 0
                        g_vm_net_connected.labels(vm=vm_name, network=net_name, mac=mac, ip=net_ip).set(conn)
            except Exception as e:
                logging.debug(f"Error parsing VM {vm}: {e}")
                pass
        vm_view.Destroy()
        
        # Batch query Performance Manager for Traffic and Disk I/O rates
        if perf_specs and perf_manager:
            try:
                perf_results = perf_manager.QueryPerf(querySpec=perf_specs)
                for i, res in enumerate(perf_results):
                    v_name = powered_on_vms[i]
                    rx_kbps, tx_kbps, r_kbps, w_kbps = 0, 0, 0, 0
                    for val in res.value:
                        cname = self.counter_map.get(val.id.counterId, "")
                        if val.id.instance == "": # Overall VM aggregate
                            val_latest = val.value[-1] if val.value else 0
                            if cname == "net.received.average":
                                rx_kbps = val_latest
                            elif cname == "net.transmitted.average":
                                tx_kbps = val_latest
                            elif cname == "disk.read.average":
                                r_kbps = val_latest
                            elif cname == "disk.write.average":
                                w_kbps = val_latest
                    
                    g_vm_net_rx_bytes_sec.labels(vm=v_name).set(rx_kbps * 1024)
                    g_vm_net_tx_bytes_sec.labels(vm=v_name).set(tx_kbps * 1024)
                    g_vm_disk_read_bytes_sec.labels(vm=v_name).set(r_kbps * 1024)
                    g_vm_disk_write_bytes_sec.labels(vm=v_name).set(w_kbps * 1024)
            except Exception as e:
                logging.error(f"Error in batch QueryPerf: {e}")

        # 4. Physical Hardware Health, Temperature & Environmental Sensors
        g_hw_temp = Gauge("esxi_hardware_temperature_celsius", "Temperature sensor reading in Celsius", ["name", "sensor_type"], registry=registry)
        g_hw_fan = Gauge("esxi_hardware_fan_rpm", "Fan speed in RPM", ["name"], registry=registry)
        g_hw_power = Gauge("esxi_hardware_power_watts", "Power consumption reading in Watts", ["name"], registry=registry)
        g_hw_voltage = Gauge("esxi_hardware_voltage_volts", "Voltage reading in Volts", ["name"], registry=registry)
        g_hw_current = Gauge("esxi_hardware_current_amperes", "Current reading in Amperes", ["name"], registry=registry)
        g_hw_sensor_health = Gauge("esxi_hardware_sensor_health", "Hardware sensor health state (1=Green/OK, 0=Degraded/Warning/Critical)", ["name", "sensor_type"], registry=registry)
        g_hw_storage_state = Gauge("esxi_hardware_storage_state", "SCSI LUN disk operational state (1=ok, 0=degraded/failed)", ["canonical_name", "vendor", "model"], registry=registry)
        g_hw_memory_health = Gauge("esxi_hardware_memory_health", "Memory DIMM health state (1=Green/OK, 0=Error)", ["name"], registry=registry)
        g_hw_cpu_health = Gauge("esxi_hardware_cpu_health", "CPU socket health state (1=Green/OK, 0=Error)", ["name"], registry=registry)

        try:
            hs = host.runtime.healthSystemRuntime
            if hs and hs.systemHealthInfo and hs.systemHealthInfo.numericSensorInfo:
                for s in hs.systemHealthInfo.numericSensorInfo:
                    s_name = s.name.strip()
                    s_type = (s.sensorType or "unknown").strip()
                    val = s.currentReading * (10 ** s.unitModifier)
                    is_healthy = 1 if (s.healthState and s.healthState.key == "Green") else 0
                    
                    g_hw_sensor_health.labels(name=s_name, sensor_type=s_type).set(is_healthy)
                    
                    if s_type == "temperature":
                        g_hw_temp.labels(name=s_name, sensor_type=s_type).set(val)
                    elif s_type == "fan":
                        g_hw_fan.labels(name=s_name).set(val)
                    elif s_type == "systemBoard" and "Pwr" in s_name:
                        g_hw_power.labels(name=s_name).set(val)
                    elif s_type == "voltage":
                        g_hw_voltage.labels(name=s_name).set(val)
                    elif s_type == "power":
                        g_hw_current.labels(name=s_name).set(val)

            if hs and hs.hardwareStatusInfo:
                for mem in hs.hardwareStatusInfo.memoryStatusInfo or []:
                    m_name = mem.name.strip()
                    is_ok = 1 if (mem.status and mem.status.key == "Green") else 0
                    g_hw_memory_health.labels(name=m_name).set(is_ok)
                
                for cpu in hs.hardwareStatusInfo.cpuStatusInfo or []:
                    c_name = cpu.name.strip()
                    is_ok = 1 if (cpu.status and cpu.status.key == "Green") else 0
                    g_hw_cpu_health.labels(name=c_name).set(is_ok)

            sd = host.config.storageDevice
            for lun in sd.scsiLun or []:
                if getattr(lun, "deviceType", None) == "disk":
                    c_name = lun.canonicalName
                    vendor = (lun.vendor or "Unknown").strip()
                    model = (lun.model or "Unknown").strip()
                    op_states = [str(st).lower() for st in (lun.operationalState or [])]
                    is_ok = 1 if ("ok" in op_states and "degraded" not in op_states and "error" not in op_states) else 0
                    g_hw_storage_state.labels(canonical_name=c_name, vendor=vendor, model=model).set(is_ok)
        except Exception as e:
            logging.error(f"Error collecting hardware health & storage sensors: {e}")

        return registry

collector = ESXiCollector(ESXI_HOST, ESXI_USER, ESXI_PASS)

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            registry = collector.collect()
            output = generate_latest(registry)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
            self.end_headers()
            self.wfile.write(output)
        elif self.path == "/healthz" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK\n")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found\n")

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), MetricsHandler)
    logging.info(f"ESXi Exporter listening on port {PORT}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
