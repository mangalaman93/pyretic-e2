##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

from pyretic.e2.lg import *
from pyretic.e2.pipelet import *
from pyretic.e2.e2 import *
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

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

net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

# Add hosts and switches
internal = net.addSwitch('s1', mac='00:00:00:00:00:01')
p = net.addSwitch('s2', mac='00:00:00:00:00:01')
n = net.addSwitch('s3', mac='00:00:00:00:00:01')
f = net.addSwitch('s4', mac='00:00:00:00:00:01')
external = net.addSwitch('s5', mac='00:00:00:00:00:01')
internal_host = net.addHost('h1', mac='00:00:00:00:00:05', ip='10.0.0.5/8')
external_host = net.addHost('h2', mac='00:00:00:00:00:05', ip='10.0.0.6/8')

# Add links
net.addLink(internal_host, internal)
net.addLink(internal, p)
net.addLink(p, n)
net.addLink(internal, n)
net.addLink(n, f)
net.addLink(f, external)
net.addLink(external, external_host)
c8 = net.addController('c8', controller=RemoteController, ip='127.0.0.1', port=6633)
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
fifa.add_edges_from([(internal_nf, p_nf, {'filter': match(dstport = 8000)}),
    (internal_nf, n_nf, {'filter': ~match(dstport = 7000)}),
    (p_nf, n_nf, {'filter': match(dstport = 8000)}),
    (n_nf, f_nf, {'filter': match()}),
    (f_nf, external_nf, {'filter': match(dstport = 8000)})])

# all_pids_to_stop = []
dest = LoadGenerator.dest(8000)
src_s1 = LoadGenerator.src(external_host.IP(), 8000, 1)
src_s2 = LoadGenerator.src(external_host.IP(), 7000, 1)
internal_host.cmd(src_s1 + " &")
# all_pids_to_stop.append(int(internal_host.cmd('echo $!')))
internal_host.cmd(src_s2 + " &")
# all_pids_to_stop.append(int(internal_host.cmd('echo $!')))
external_host.cmd(dest + " &")
# all_pids_to_stop.append(int(internal_host.cmd('echo $!')))

def main():
    return e2(net, [fifa]).policy()
