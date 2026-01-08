#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def bandwidthTopology():
    """Create a topology with different bandwidth links"""
    
    net = Mininet(controller=Controller, link=TCLink)
    
    print("*** Creating nodes")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    s1 = net.addSwitch('s1')
    c0 = net.addController('c0')
    
    print("*** Creating links with different bandwidths")
    # Fast link: 100 Mbps
    net.addLink(h1, s1, bw=100)
    # Medium link: 10 Mbps
    net.addLink(h2, s1, bw=10)
    # Slow link: 1 Mbps
    net.addLink(h3, s1, bw=1)
    
    print("*** Starting network")
    net.start()
    
    print("*** Testing bandwidth")
    print("Testing h1 (100Mbps) to h2 (10Mbps)")
    net.iperf((h1, h2))
    
    print("Testing h1 (100Mbps) to h3 (1Mbps)")
    net.iperf((h1, h3))
    
    print("*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    bandwidthTopology()
