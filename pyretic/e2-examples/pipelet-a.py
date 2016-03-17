##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

from pyretic.e2.lg import *
from pyretic.e2.pipelet import *
from pyretic.lib.corelib import *
from pyretic.lib.std import *
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from pyretic.e2.e2 import *

# Example taken from E2 paper 15(a)
#
#          +------------+
#    +-----+  Internal  |
#    |     +------+-----+
#    |            |
#    |            |
#    v            v
# +--+--+      +--+--+
# |  p  |----->+  n  |
# +-----+      +--+--+
#                 |
#                 |
#                 v
#              +--+--+
#           +--+  f  +--+
#           |  +-----+  |
#           |           |
#           v           v
#       +---+----+   +--+---+
#       |external|   | drop |
#       +--------+   +------+
#


net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

# Add hosts and switches
internal = net.addSwitch('s1', listenPort=7000, mac='00:00:00:00:00:01')
p = net.addSwitch('s2',listenPort=7200, mac='00:00:00:00:00:01')
n = net.addSwitch('s3',listenPort=7400, mac='00:00:00:00:00:01')
f = net.addSwitch('s4',listenPort=7600, mac='00:00:00:00:00:01')
external = net.addSwitch('s5',listenPort=7800, mac='00:00:00:00:00:01')
internal_host = net.addHost('h1', mac='00:00:00:00:00:05', ip='10.0.0.5/8' )
external_host = net.addHost('h2', mac='00:00:00:00:00:05', ip='10.0.0.5/8' )

# Add links
net.addLink(internal_host, internal)
net.addLink(internal, p)
net.addLink(p, n)
net.addLink(internal, n)
net.addLink(n, f)
net.addLink(f, external)
net.addLink(external, external_host)
c8 = net.addController( 'c8', controller=RemoteController, ip='127.0.0.1', port=6633 )

net.start()

# creating NFs
internal_nf = E2NF("s1", 1)
p_nf = E2NF("s2", 1)
n_nf = E2NF("s3", 1)
f_nf = E2NF("s4", 1)
external_nf = E2NF("s5", 1)

# adding filters
fifa = E2Pipelet("pipelet-a")
fifa.add_nodes_from([internal_nf, p_nf, n_nf, f_nf, external_nf])
fifa.add_edges_from([(internal_nf, p_nf, {'filter': match(dstport = 7200)}),
    (internal_nf, n_nf, {'filter': ~match(dstport = 7200)}),
    (p_nf, n_nf, {'filter': ~match(dstport = 7200)}),
    (n_nf, f_nf, {'filter': match()}),
    (f_nf, external_nf, {'filter': ~match(dstport = 7200)})])

def helper():
    dest = LoadGenerator.dest(8000)
    src_s1 = LoadGenerator.src(external_host.IP(), 8000, 100)
    src_s2 = LoadGenerator.src(external_host.IP(), 7000, 100)
    internal_host.sendCmd(src_s1)
    internal_host.sendCmd(src_s2)
    external_host.sendCmd(dest)

nodedict = {}

# for edge in fifa.edges(data=True):
#     if edge[0].name not in nodedict:
#         nodedict[edge[0].name] = []

#     nodedict[edge[0].name].append(edge)

interfaces={}
port={}
for s in net.switches:
    port[s.name] = s.listenPort
#print port
for link in net.links:
    if link.intf1.name.split("-")[0] not in interfaces:
        interfaces[link.intf1.name.split("-")[0]] = {}
    pos = link.intf1.name.split("-")[1].rindex("h")+1
    #print pos
    interfaces[link.intf1.name.split("-")[0]][link.intf2.name.split("-")[0]]= link.intf1.name.split("-")[1][pos:]
#print interfaces
for edge in fifa.edges(data=True):
     if edge[0].name not in nodedict:
        nodedict[edge[0].name] = []
     nodedict[edge[0].name].append(edge)
#print nodedict
allroutes = None
for sw in port.keys():
    route  =None
    #print "Rule for ", sw 
    if sw in nodedict:
        for rule in nodedict[sw]:
            if route is None:
                route = rule[2]['filter'] >> fwd(interfaces[sw][rule[1].name]) 
            else:
                route = route + rule[2]['filter'] >> fwd(interfaces[sw][rule[1].name]) 
        if allroutes is None:
            allroutes = (match(srcport = port[sw]) >> route)
        else:
            allroutes += (match(srcport = port[sw]) >> route)
    #print route
print allroutes
net.stop()
e2(net, [fifa], helper).start()