# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 19:03:12 2021

@author: JLD
"""

#coding=UTF-8
#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections 
from mininet.log import setLogLevel 
def IperfTest():  
    net=Mininet(host=CPULimitedHost,link=TCLink)
    c0= net.addController()
    h1=net.addHost('h1',cpu=0.5)
    h2=net.addHost('h2',cpu=0.5)
    h3=net.addHost('h3')
    s1=net.addSwitch('s1')
    s2=net.addSwitch('s2')
    s3=net.addSwitch('s3')
    #Creating links between nodes
    net.addLink(h1, s1, bw=10, delay='5ms',max_queue_size=1000, loss=10, use_htb=True)
    net.addLink(h2, s2, bw=10, delay='5ms',max_queue_size=1000, loss=10, use_htb=True)
    net.addLink(h3, s3,bw=10, delay='5ms',max_queue_size=1000, loss=10, use_htb=True)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    # Configure host ip
    h1.setIP('10.0.0.1', 24)
    h2.setIP('10.0.0.2', 24)
    h3.setIP('10.0.0.3', 24)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)  
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth"
    h1, h2, h3 = net.get('h1', 'h2', 'h3')
    net.iperf((h1,h2))
    net.iperf((h2,h3))
    net.iperf((h1,h3))
    net.pingAll()
    net.stop()
if __name__=='__main__':
    setLogLevel('info') #print the log when Configuring hosts, starting switches and controller     
    IperfTest() 