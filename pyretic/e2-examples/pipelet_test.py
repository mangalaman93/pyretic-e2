##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.e2.pipelet import *

import networkx as nx
import matplotlib.pyplot as plt

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

# creating NFs
internal = E2NF("internal", 1)
p = E2NF("p", 1)
n = E2NF("n", 1)
f = E2NF("f", 1)
external = E2NF("external", 1)

# adding filters
fifa = E2Pipelet("pipelet-a")
fifa.add_nodes_from([internal, p, n, f, external])
fifa.add_edges_from([(internal, p, {'filter': match(dstport = 80)}),
    (internal, n, {'filter': ~match(dstport=80)}),
    (p, n, {'filter': ~ match(srcip='10.0.0.0/8')}),
    (n, f, {'filter': match()}),
    (f, external, {'filter': ~match(srcip='130.207.0.0/16')})])

nx.draw(fifa)
plt.savefig("graph.png")

def main():
    return flood()
