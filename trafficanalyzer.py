#!/usr/bin/env python3
"""
Enhanced Mininet Traffic Analysis with Real-time Monitoring
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import json

class EnhancedTrafficAnalyzer:
    """Enhanced traffic analysis with statistics collection"""
    
    def __init__(self):
        self.stats = {}
        self.traffic_log = []
    
    def generate_traffic_matrix(self, net):
        """Generate traffic between multiple hosts"""
        info('\n*** Generating traffic matrix\n')
        hosts = net.hosts
        
        # Create traffic pairs
        traffic_pairs = [
            (hosts[0], hosts[2], 'TCP Bulk'),
            (hosts[1], hosts[3], 'TCP Bulk'),
            (hosts[0], hosts[4], 'UDP Streaming'),
            (hosts[2], hosts[4], 'HTTP-like')
        ]
        
        for src, dst, traffic_type in traffic_pairs:
            self._run_traffic_test(src, dst, traffic_type)
    
    def _run_traffic_test(self, src, dst, traffic_type):
        """Run individual traffic test"""
        info(f'\n*** {traffic_type} traffic: {src.name} -> {dst.name}\n')
        
        # Start server on destination
        dst.cmd(f'iperf -s -p 5001 > /tmp/iperf_server_{dst.name}.log 2>&1 &')
        time.sleep(1)
        
        # Run client on source
        if 'UDP' in traffic_type:
            cmd = f'iperf -c {dst.IP()} -u -b 5M -t 5 -i 1'
        else:
            cmd = f'iperf -c {dst.IP()} -t 5 -i 1'
        
        result = src.cmd(cmd)
        
        # Log results
        test_result = {
            'type': traffic_type,
            'source': src.name,
            'destination': dst.name,
            'result': self._parse_iperf_result(result),
            'timestamp': time.time()
        }
        
        self.traffic_log.append(test_result)
        
        # Kill server
        dst.cmd('pkill -f "iperf -s"')
        
        return test_result
    
    def _parse_iperf_result(self, result):
        """Parse iperf output for relevant metrics"""
        lines = result.split('\n')
        for line in lines:
            if 'Gbits/sec' in line or 'Mbits/sec' in line:
                return line.strip()
        return "No throughput data"
    
    def monitor_bandwidth(self, net, duration=10):
        """Monitor bandwidth usage on all links"""
        info(f'\n*** Monitoring bandwidth for {duration} seconds\n')
        
        hosts = net.hosts
        monitor_data = {}
        
        # Start monitoring on each host
        for host in hosts:
            # Get initial stats
            initial = self._get_interface_stats(host)
            monitor_data[host.name] = {'initial': initial}
        
        time.sleep(duration)
        
        # Get final stats and calculate differences
        for host in hosts:
            final = self._get_interface_stats(host)
            monitor_data[host.name]['final'] = final
            
            # Calculate bandwidth
            rx_rate = (final['rx_bytes'] - monitor_data[host.name]['initial']['rx_bytes']) / duration
            tx_rate = (final['tx_bytes'] - monitor_data[host.name]['initial']['tx_bytes']) / duration
            
            info(f'\n*** {host.name} Bandwidth Usage:\n')
            info(f'   RX Rate: {rx_rate/1000:.2f} KB/s\n')
            info(f'   TX Rate: {tx_rate/1000:.2f} KB/s\n')
            
            monitor_data[host.name]['rx_rate'] = rx_rate
            monitor_data[host.name]['tx_rate'] = tx_rate
        
        self.stats['bandwidth'] = monitor_data
    
    def _get_interface_stats(self, host):
        """Get network interface statistics"""
        stats = {}
        output = host.cmd('cat /proc/net/dev')
        
        for line in output.split('\n'):
            if 'eth0' in line:
                parts = line.split()
                stats['rx_bytes'] = int(parts[1])
                stats['tx_bytes'] = int(parts[9])
                break
        
        return stats
    
    def generate_report(self):
        """Generate analysis report"""
        info('\n' + '='*60 + '\n')
        info('*** TRAFFIC ANALYSIS REPORT\n')
        info('='*60 + '\n')
        
        info('\n=== Traffic Test Results ===\n')
        for i, test in enumerate(self.traffic_log, 1):
            info(f'Test {i}:\n')
            info(f'  Type: {test["type"]}\n')
            info(f'  Path: {test["source"]} -> {test["destination"]}\n')
            info(f'  Result: {test["result"]}\n')
        
        if 'bandwidth' in self.stats:
            info('\n=== Bandwidth Usage Summary ===\n')
            for host, data in self.stats['bandwidth'].items():
                if 'rx_rate' in data:
                    info(f'{host}:\n')
                    info(f'  Average RX: {data["rx_rate"]/1000:.2f} KB/s\n')
                    info(f'  Average TX: {data["tx_rate"]/1000:.2f} KB/s\n')
        
        # Save report to file
        report_data = {
            'traffic_tests': self.traffic_log,
            'statistics': self.stats
        }
        
        with open('/tmp/mininet_analysis_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        info('\n*** Report saved to /tmp/mininet_analysis_report.json\n')

def create_simple_topology():
    """Create a simple star topology for testing"""
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink)
    
    info('*** Adding controller\n')
    c0 = net.addController('c0')
    
    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    
    info('*** Adding hosts\n')
    for i in range(1, 6):
        net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
    
    info('*** Creating links\n')
    for host in net.hosts:
        net.addLink(host, s1, bw=50, delay='2ms')
    
    info('*** Building network\n')
    net.build()
    c0.start()
    s1.start([c0])
    
    return net

def install_tools():
    """Install required tools if not present"""
    info('*** Checking/installing required tools\n')
    tools = ['iperf', 'tcpdump', 'netcat']
    
    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0:
            info(f'*** Installing {tool}\n')
            subprocess.run(['apt-get', 'update'], stdout=subprocess.DEVNULL)
            subprocess.run(['apt-get', 'install', '-y', tool], stdout=subprocess.DEVNULL)

if __name__ == '__main__':
    setLogLevel('info')
    
    # Check for required tools
    try:
        import subprocess
        install_tools()
    except:
        info('*** Skipping tool installation\n')
    
    # Create and run network
    net = create_simple_topology()
    analyzer = EnhancedTrafficAnalyzer()
    
    try:
        net.start()
        
        info('\n' + '='*60 + '\n')
        info('*** Starting Enhanced Traffic Analysis\n')
        info('='*60 + '\n')
        
        # Run comprehensive tests
        analyzer.generate_traffic_matrix(net)
        analyzer.monitor_bandwidth(net, duration=5)
        analyzer.generate_report()
        
        info('\n*** Analysis complete. Entering interactive mode...\n')
        info('*** Try these commands:\n')
        info('    h1 ping h2\n')
        info('    h1 iperf -s &\n')
        info('    h2 iperf -c h1 -t 5\n')
        info('    exit\n')
        
        CLI(net)
        
    finally:
        net.stop()
        info('\n*** Network stopped\n')