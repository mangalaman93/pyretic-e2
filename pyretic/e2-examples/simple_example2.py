##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################
import matplotlib.pyplot as plt
from pyretic.e2.lg import *
from pyretic.e2.pipelet import *
from pyretic.e2.e2 import *
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink

# loads generated
l1 = 5

nfc1 = 5
nfc2 = 6
nfc3 = 5
bin_capacity = 11

# Mininet
net = Mininet(controller=RemoteController,
              link=TCLink,
              switch=OVSKernelSwitch,
              autoStaticArp=True,
              autoSetMacs=True)

# Add hosts and switches

s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
s4 = net.addSwitch('s4')
s5 = net.addSwitch('s5')
s6 = net.addSwitch('s6')
# hws
s7 = net.addSwitch('s7')
# src
s8 = net.addSwitch('s8')
# dest
s9 = net.addSwitch('s9')

h1 = net.addHost('h1')
h2 = net.addHost('h2')

# Add links

#sources
net.addLink(h1, s8)

#dest
net.addLink(h2, s9)

#hws
net.addLink(s1,s7)
net.addLink(s2,s7)
net.addLink(s3,s7)
net.addLink(s4,s7)
net.addLink(s5,s7)
net.addLink(s6,s7)
net.addLink(s8,s7)
net.addLink(s9,s7)

c8 = net.addController('c8', controller=RemoteController, ip='127.0.0.1', port=6633)
net.start()

# creating NFs
source1 = E2NF("h1", 1,'src1',inp_load_estimate=l1, switch_placed='s8')

NF1 = E2NF("NF1", 1,'NF1',nf_capacity=nfc1)
NF2 = E2NF("NF2", 1, 'NF2',nf_capacity=nfc2)
NF3 = E2NF("NF3", 1, 'NF3',nf_capacity=nfc3)

dest1 = E2NF("h2", 1, 'dst1', inp_load_estimate=l1, switch_placed='s9')

# create pipelets
pipe1 = E2Pipelet("pipelet-1")
pipe1.add_nodes_from([source1, NF1, NF2, NF3, dest1])
pipe1.add_edges_from([
    (source1, NF1,{'filter': match(dstport = 80)}),
    (NF1, NF2,{'filter':match(dstport = 80)}),
    (NF2, NF3,{'filter':match(dstport = 80)}),
    (NF3, dest1,{'filter': match(dstport = 80)})
    ])

src_s1 = LoadGenerator.src(h2.IP(), 80, tcp=False, num_request=100000)
h1.cmd(src_s1 + " &")

def main():
  pipelets = [pipe1]
  sources = [source1]
  e2_main = e2(net, pipelets)

  print "==============PIPELETS==============="
  for pipelet in pipelets:
    print pipelet.name
    print pipelet.edges(data=True)

  print "==============PGRAPH==============="
  pgraph = e2_main.merge_pipelets(pipelets, "pgraph1")
  print(pgraph.nodes())
  print(pgraph.edges(data=True))
  pos = nx.shell_layout(pgraph)
  nx.draw(pgraph, pos)
  plt.show()

  print "==============IGRAPH==============="
  igraph= e2_main.create_igraph(pgraph, sources)
  print(igraph.nodes())
  print(igraph.edges(data=True))
  pos = nx.shell_layout(igraph)
  nx.draw(igraph, pos)
  plt.show()

  print "==============BIN PACKING==============="
  new_igraph = e2_main.bin_pack(igraph, sources, bin_capacity)

  print "==============UPDATE PIPELETS==============="
  return e2_main.policy(new_igraph, sources, 's7')
