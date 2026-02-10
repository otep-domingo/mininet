#!/usr/bin/env python3
"""
Ultra Simple Mininet Example
Quick network creation and basic ping test
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_simple_network():
    """Create the simplest possible network"""
    net = Mininet()
    
    print("*** Creating 2-host network")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    net.addLink(h1, h2)
    
    net.start()
    return net

def quick_test():
    """Run a quick ping test"""
    print("\n" + "="*40)
    print("Quick Ping Test")
    print("="*40)
    
    net = Mininet()
    
    # Add 2 hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    net.addLink(h1, h2)
    
    net.start()
    
    # Test ping
    print("*** Testing ping from h1 to h2")
    result = net.ping([h1, h2])
    
    if result == 0:
        print("✓ Ping successful!")
    else:
        print("✗ Ping failed")
    
    net.stop()

# Even simpler - one liner functions
def run_mininet():
    """Create and run Mininet with default topology"""
    net = Mininet()
    net.start()
    CLI(net)
    net.stop()

def basic_traffic_test():
    """Basic traffic test with 3 hosts"""
    from mininet.link import TCLink
    
    net = Mininet(link=TCLink)
    
    # Create hosts
    for i in range(1, 4):
        net.addHost(f'h{i}')
    
    # Connect all to a switch
    s1 = net.addSwitch('s1')
    for host in net.hosts:
        net.addLink(host, s1, bw=10)  # 10 Mbps
    
    net.start()
    
    print("\n*** Simple Traffic Test")
    print("1. Testing connectivity...")
    net.pingAll()
    
    print("\n2. Starting iperf test...")
    h1, h2 = net.get('h1', 'h2')
    
    # Start server
    h1.cmd('iperf -s &')
    
    # Run client
    print("Running iperf from h2 to h1:")
    print(h2.cmd('iperf -c h1 -t 3'))
    
    h1.cmd('pkill iperf')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    
    print("Choose an option:")
    print("1. Quick ping test")
    print("2. Basic traffic test")
    print("3. Full interactive Mininet")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        quick_test()
    elif choice == '2':
        basic_traffic_test()
    else:
        run_mininet()