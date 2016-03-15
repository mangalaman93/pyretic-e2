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
internal_host = net.addHost('h1')
external_host = net.addHost('h2')
internal = net.addSwitch('s1')
p = net.addSwitch('s2')
n = net.addSwitch('s3')
f = net.addSwitch('s4')
external = net.addSwitch('s5')

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
internal = E2NF("internal", 1)
p = E2NF("p", 1)
n = E2NF("n", 1)
f = E2NF("f", 1)
external = E2NF("external", 1)

# adding filters
fifa = E2Pipelet("pipelet-a")
fifa.add_nodes_from([internal, p, n, f, external])
fifa.add_edges_from([(internal, p, {'filter': match(dstport = 8000)}),
    (internal, n, {'filter': ~match(dstport = 7000)}),
    (p, n, {'filter': ~match(dstport = 8000)}),
    (n, f, {'filter': match()}),
    (f, external, {'filter': ~match(dstport = 8000)})])

def helper():
    dest = LoadGenerator.dest(8000)
    src_s1 = LoadGenerator.src(external_host.IP(), 8000, 100)
    src_s2 = LoadGenerator.src(external_host.IP(), 7000, 100)
    internal_host.sendCmd(src_s1)
    internal_host.sendCmd(src_s2)
    external_host.sendCmd(dest)

e2(net, [fifa], helper).start()
