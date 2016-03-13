##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

from pyretic.e2.lg import *
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

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

class PiepeletATopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Add hosts and switches
        internal_host = self.addHost('internal')
        external_host = self.addHost('external')
        internal = self.addSwitch('internal')
        p = self.addSwitch('p')
        n = self.addSwitch('n')
        f = self.addSwitch('f')
        external = self.addSwitch('external')

        # Add links
        self.addLink(internal_host, internal)
        self.addLink(internal, p)
        self.addLink(p, n)
        self.addLink(internal, n)
        self.addLink(n, f)
        self.addLink(f, external)
        self.addLink(external, external_host)

# creating a mininet class
net = Mininet(topo = PiepeletATopo, controller=lambda name: RemoteController(name='c0', ip='127.0.0.1', port=6633))
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

E2(net, [fifa], helper).start()
