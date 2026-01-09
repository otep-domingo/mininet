#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def delayLossTopology():
    """Create a topology with delay and packet loss"""
    
    net = Mininet(controller=Controller, link=TCLink)
    
    print("*** Creating nodes")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    s1 = net.addSwitch('s1')
    c0 = net.addController('c0')
    
    print("*** Creating links with different characteristics")
    # Normal link
    net.addLink(h1, s1, bw=10, delay='5ms')
    # High latency link
    net.addLink(h2, s1, bw=10, delay='100ms')
    # Lossy link
    net.addLink(h3, s1, bw=10, delay='5ms', loss=10)
    # Congested link (small queue)
    net.addLink(h4, s1, bw=10, delay='5ms', max_queue_size=10)
    
    print("*** Starting network")
    net.start()
    
    print("*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    delayLossTopology()
