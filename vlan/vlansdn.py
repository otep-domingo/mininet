#!/usr/bin/env python3
"""
SDN with two VLANs (Student VLAN 10, Faculty VLAN 20), 3 hosts each.
Written without any loops: every host, link and flow is declared explicitly.
 
    stud1 stud2 stud3  (10.0.10.1-3, switch ports 1-3)  -> STUDENT
    fac1  fac2  fac3   (10.0.20.1-3, switch ports 4-6)  -> FACULTY
 
Run:  sudo python3 vlan_sdn_noloop.py
"""
 
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
 
 
def main():
    setLogLevel("info")
 
    net = Mininet(switch=OVSSwitch, controller=None)
 
    info("*** Adding switch\n")
    s1 = net.addSwitch("s1", protocols="OpenFlow13", failMode="secure")
 
    info("*** Adding Student VLAN hosts\n")
    stud1 = net.addHost("stud1", ip="10.0.10.1/24", mac="00:00:00:00:00:01")
    stud2 = net.addHost("stud2", ip="10.0.10.2/24", mac="00:00:00:00:00:02")
    stud3 = net.addHost("stud3", ip="10.0.10.3/24", mac="00:00:00:00:00:03")
 
    info("*** Adding Faculty VLAN hosts\n")
    fac1 = net.addHost("fac1", ip="10.0.20.1/24", mac="00:00:00:00:00:04")
    fac2 = net.addHost("fac2", ip="10.0.20.2/24", mac="00:00:00:00:00:05")
    fac3 = net.addHost("fac3", ip="10.0.20.3/24", mac="00:00:00:00:00:06")
 
    info("*** Adding links (fixed switch port numbers)\n")
    net.addLink(stud1, s1, port2=1)
    net.addLink(stud2, s1, port2=2)
    net.addLink(stud3, s1, port2=3)
    net.addLink(fac1, s1, port2=4)
    net.addLink(fac2, s1, port2=5)
    net.addLink(fac3, s1, port2=6)
 
    info("*** Starting network\n")
    net.start()
 
    info("*** Installing flow rules\n")
    of = "ovs-ofctl -O OpenFlow13 add-flow s1"
    s1.cmd("ovs-ofctl -O OpenFlow13 del-flows s1")
 
    # Student VLAN 10: ports 1,2,3 only talk to each other
    s1.cmd(of, '"priority=100,in_port=1,actions=output:2,output:3"')
    s1.cmd(of, '"priority=100,in_port=2,actions=output:1,output:3"')
    s1.cmd(of, '"priority=100,in_port=3,actions=output:1,output:2"')
 
    # Faculty VLAN 20: ports 4,5,6 only talk to each other
    s1.cmd(of, '"priority=100,in_port=4,actions=output:5,output:6"')
    s1.cmd(of, '"priority=100,in_port=5,actions=output:4,output:6"')
    s1.cmd(of, '"priority=100,in_port=6,actions=output:4,output:5"')
 
    # Anything else is dropped
    s1.cmd(of, '"priority=0,actions=drop"')
 
    info("*** Testing: same VLAN (should work)\n")
    net.ping([stud1, stud2, stud3])
    net.ping([fac1, fac2, fac3])
 
    info("*** Testing: different VLANs (should fail)\n")
    net.ping([stud1, fac1])
    net.ping([stud2, fac2])
    net.ping([stud3, fac3])
 
    info(s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1"))
 
    CLI(net)
    net.stop()
 
 
if __name__ == "__main__":
    main()
 