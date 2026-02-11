#!/usr/bin/env python
# coffee_shop.py
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSController

def coffeeShopNetwork():
    """Create a simple coffee shop network"""
    net = Mininet(controller=OVSController)
    
    info('*** Adding controller\n')
    net.addController('c0')
    
    info('*** Adding hosts (customers and access point)\n')
    # Access Point/Router
    ap = net.addHost('ap', ip='192.168.1.1/24')
    
    # Customers with their devices
    customer1 = net.addHost('cust1', ip='192.168.1.10/24')
    customer2 = net.addHost('cust2', ip='192.168.1.11/24')
    customer3 = net.addHost('cust3', ip='192.168.1.12/24')
    
    # Coffee shop server
    server = net.addHost('server', ip='192.168.1.100/24')
    
    info('*** Adding switch\n')
    switch = net.addSwitch('s1')
    
    info('*** Creating links\n')
    net.addLink(ap, switch)
    net.addLink(customer1, switch)
    net.addLink(customer2, switch)
    net.addLink(customer3, switch)
    net.addLink(server, switch)
    
    info('*** Starting network\n')
    net.start()
    
    # Set up default route through AP
    info('*** Setting up routes\n')
    for host in [customer1, customer2, customer3]:
        host.cmd('route add default gw 192.168.1.1')
    
    info('*** Starting services\n')
    # Start simple HTTP server on coffee shop server
    server.cmd('python3 -m http.server 80 &')
    
    info('\n*** Coffee Shop Network Ready!\n')
    info('Network Layout:\n')
    info('    [cust1]    [cust2]    [cust3]\n')
    info('       |         |         |\n')
    info('      ---[Switch]---\n')
    info('          |     |\n')
    info('       [AP]   [Server]\n')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')

    coffeeShopNetwork()
