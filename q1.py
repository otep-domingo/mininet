from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
net = Mininet(host=CPULimitedHost, link=TCLink) 
    # Create network node
c0 = net.addController()
h1 = net.____________
h2 = net.____________
s1 = net.addSwitch('s1')
    # Creating links between nodes
net.addLink(h1, s1)
net.addLink(h2, s2)
    # Configure host ip
___________________________
net.pingAll()
net.stop()
