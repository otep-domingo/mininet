# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:20:40 2021

@author: JLD
"""
    # coding=UTF-8
from mininet.net import Mininet
from mininet.node import CPULimitedHost #cpu Related settings
from mininet.link import TCLink # addLink Related settings
net = Mininet(host=CPULimitedHost, link=TCLink) # If performance is not limited, the parameter is empty
    # Create network node
c0 = net.addController()
h1 = net.addHost('h1', cpu=0.5) #cpu Performance limitations
h2 = net.addHost('h2', cpu=0.5) #cpu Performance limitations
h3 = net.addHost('h3')
h4 = net.addHost('h4')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
    # Creating links between nodes
net.addLink(h1, s1, bw=10, delay='5ms',max_queue_size=1000, loss=10, use_htb=True) #bandwidth bw,delayed delay Etc
net.addLink(h3, s1)
net.addLink(h2, s2, bw=10, delay='5ms',max_queue_size=1000, loss=10, use_htb=True) #bandwidth bw,delayed delay Etc
net.addLink(h4, s2)
net.addLink(s1, s2)
    # Configure host ip
h1.setIP('10.0.0.1', 24)
h2.setIP('10.0.0.2', 24)
h3.setIP('10.0.0.3', 24)
h4.setIP('10.0.0.4', 24)
net.start()
net.pingAll()
net.stop()

