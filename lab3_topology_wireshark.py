#!/usr/bin/python
"""
Lab 3: Traffic Analysis Topology
Creates a simple network with web server for packet analysis
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def labTopology():
    """Create a topology for traffic analysis lab"""
    
    # Create network with TCLink support
    net = Mininet(controller=Controller, link=TCLink)
    
    print("*** Creating nodes")
    # Create hosts
    server = net.addHost('server', ip='10.0.0.10/24')
    client1 = net.addHost('client1', ip='10.0.0.11/24')
    client2 = net.addHost('client2', ip='10.0.0.12/24')
    
    # Create switch
    s1 = net.addSwitch('s1')
    
    # Create controller
    c0 = net.addController('c0')
    
    print("*** Creating links")
    # Add links with realistic parameters
    net.addLink(server, s1, bw=100, delay='2ms')
    net.addLink(client1, s1, bw=10, delay='5ms')
    net.addLink(client2, s1, bw=10, delay='5ms')
    
    print("*** Starting network")
    net.start()
    
    print("*** Network is ready!")
    print("Server IP: %s" % server.IP())
    print("Client1 IP: %s" % client1.IP())
    print("Client2 IP: %s" % client2.IP())
    
    # Start web server on server host
    print("*** Starting web server on server")
    server.cmd('cd /tmp')
    server.cmd('echo "Hello from Mininet Server!" > index.html')
    server.cmd('python -m SimpleHTTPServer 80 &')
    
    print("\n*** Lab topology ready for packet capture")
    print("*** Use 'xterm server' to open a terminal on the server")
    print("*** Use 'xterm client1' to open a terminal on client1")
    
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    labTopology()