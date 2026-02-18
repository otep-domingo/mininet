#!/usr/bin/env python
"""
Laboratory Activity: Coffee Shop Network Packet Analysis
Author: [Your Name]
Date: [Current Date]
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def create_coffee_shop():
    """Create a coffee shop network with customers and server"""
    
    # Create network
    net = Mininet(controller=Controller)
    
    # Add controller
    info('*** Adding controller\n')
    net.addController('c0')
    
    # Add network devices
    info('*** Adding hosts\n')
    ap = net.addHost('ap', ip='192.168.1.1/24')  # Access Point/Router
    
    # Customers (with different device types)
    customer1 = net.addHost('alice', ip='192.168.1.10/24')  # Laptop
    customer2 = net.addHost('bob', ip='192.168.1.11/24')    # Smartphone
    customer3 = net.addHost('charlie', ip='192.168.1.12/24') # Tablet
    
    # Coffee shop server (for website, menu, etc.)
    server = net.addHost('server', ip='192.168.1.100/24')
    
    # Switch
    info('*** Adding switch\n')
    switch = net.addSwitch('s1')
    
    # Create links
    info('*** Creating links\n')
    net.addLink(ap, switch)
    net.addLink(customer1, switch)
    net.addLink(customer2, switch)
    net.addLink(customer3, switch)
    net.addLink(server, switch)
    
    # Start network
    info('*** Starting network\n')
    net.start()
    
    # Configure routing
    info('*** Configuring routing\n')
    for customer in [customer1, customer2, customer3]:
        customer.cmd('route add default gw 192.168.1.1')
    
    # Start services
    info('*** Starting coffee shop services\n')
    server.cmd('python3 -m http.server 80 > /dev/null 2>&1 &')
    
    # Display network information
    info('\n' + '='*50)
    info('\nCoffee Shop Network Ready!\n')
    info('='*50)
    info('\nNetwork Layout:')
    info('\n    [Alice]    [Bob]    [Charlie]')
    info('\n       |         |         |')
    info('\n    -------------------------')
    info('\n           [Switch]')
    info('\n         /         \\')
    info('\n     [AP]        [Server]')
    info('\n')
    info('='*50)
    info('\nIP Addresses:')
    info('  Alice (laptop):   192.168.1.10')
    info('  Bob (smartphone): 192.168.1.11')
    info('  Charlie (tablet): 192.168.1.12')
    info('  Server:           192.168.1.100')
    info('  AP/Router:        192.168.1.1')
    info('='*50 + '\n')
    
    return net

if __name__ == '__main__':
    setLogLevel('info')
    network = create_coffee_shop()
    
    # Start interactive CLI
    info('*** Entering Mininet CLI. Type "exit" to stop.\n')
    CLI(network)
    
    # Stop network
    info('*** Stopping network\n')
    network.stop()