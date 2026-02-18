#!/usr/bin/env python
"""
Simple Packet Capture Laboratory
A basic 2-host network for learning packet analysis
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def simple_network():
    """Create a minimal network with 2 hosts"""
    
    # Create network
    net = Mininet(controller=Controller)
    
    # Add controller
    info('*** Adding controller\n')
    net.addController('c0')
    
    # Add two hosts
    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1/8')
    h2 = net.addHost('h2', ip='10.0.0.2/8')
    
    # Add switch
    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    
    # Connect hosts to switch
    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    
    # Start network
    info('*** Starting network\n')
    net.start()
    
    info('\n' + '='*40)
    info('\nSimple Network Ready!')
    info('\n' + '='*40)
    info('\nHost IPs:')
    info('  h1: 10.0.0.1')
    info('  h2: 10.0.0.2')
    info('\nCommands to remember:')
    info('  ping - test connectivity')
    info('  python3 -m http.server - start web server')
    info('  curl - download web page')
    info('  tcpdump - capture packets')
    info('='*40 + '\n')
    
    return net

if __name__ == '__main__':
    setLogLevel('info')
    network = simple_network()
    
    # Start CLI
    info('*** Mininet CLI started (type "exit" to quit)\n')
    CLI(network)
    
    # Stop network
    info('*** Stopping network\n')
    network.stop()