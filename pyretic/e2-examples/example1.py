##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

from pyretic.e2.lg import *
from pyretic.e2.pipelet import *
from pyretic.e2.e2 import *
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
import pdb

##loads generated
l1 = 4
l2 = 4
l3 = 4
l4 = 4
l5 = 4
nfc1 = 5
nfc2 = 10
nfc3 = 4
bin_capacity = 10

##Mininet
net = Mininet(controller=RemoteController,
              link=TCLink,
              switch=OVSKernelSwitch,
              autoStaticArp=True)

# Add hosts and switches

s1 = net.addSwitch('s1', mac='00:00:00:00:00:01')
s2 = net.addSwitch('s2', mac='00:00:00:00:00:02')
s3 = net.addSwitch('s3', mac='00:00:00:00:00:03')
s4 = net.addSwitch('s4', mac='00:00:00:00:00:04')
s5 = net.addSwitch('s5', mac='00:00:00:00:00:05')
s6 = net.addSwitch('s6', mac='00:00:00:00:00:06')
#hws
s7 = net.addSwitch('s7', mac='00:00:00:00:00:07')
#src
s8 = net.addSwitch('s8', mac='00:00:00:00:00:08')
#dest
s9 = net.addSwitch('s9', mac='00:00:00:00:00:09')

h1 = net.addHost('h1', mac='00:00:00:00:00:10')
h2 = net.addHost('h2', mac='00:00:00:00:00:11')
h3 = net.addHost('h3', mac='00:00:00:00:00:12')
h4 = net.addHost('h4', mac='00:00:00:00:00:13')
h5 = net.addHost('h5', mac='00:00:00:00:00:14')
h6 = net.addHost('h4', mac='00:00:00:00:00:15')
h7 = net.addHost('h5', mac='00:00:00:00:00:16')

# Add links

#sources
net.addLink(h1, s8)
net.addLink(h2, s8)
net.addLink(h3, s8)
net.addLink(h4, s8)
net.addLink(h5, s8)

#dest
net.addLink(h6, s9)
net.addLink(h7, s9)

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
source2 = E2NF("h2", 1,'src2',inp_load_estimate=l2, switch_placed='s8')
source3 = E2NF("h3", 1,'src3',inp_load_estimate=l3, switch_placed='s8')
source4 = E2NF("h4", 1,'src4',inp_load_estimate=l4, switch_placed='s8')
source5 = E2NF("h5", 1,'src5',inp_load_estimate=l5, switch_placed='s8')

NF1 = E2NF("NF1", 1,'NF1',nf_capacity=nfc1)
NF2 = E2NF("NF2", 1, 'NF2',nf_capacity=nfc2)
NF3 = E2NF("NF3", 1, 'NF3',nf_capacity=nfc3)

dest1 = E2NF("h6", 1, 'dst1', switch_placed='s9')
dest2 = E2NF("h7", 1,'dst2', switch_placed='s9')

# create pipelets
pipe1 = E2Pipelet("pipelet-1")
pipe1.add_nodes_from([source1, NF1, NF3, dest1])
pipe1.add_edges_from([
    (source1, NF1,{'filter': match(srcport = 80)}),
    (NF1, NF3,{'filter':match(srcport = 80)}),
    (NF3, dest1,{'filter': match(srcport = 80)}),
    (NF1, source1,{'filter': match(dstport = 80)}),
    (NF3,NF1,{'filter': match(dstport = 80)}),
    (dest1, NF3,{'filter': match(dstport = 80)}),
    ])

pipe2 = E2Pipelet("pipelet-2")
pipe2.add_nodes_from([source2, NF1, NF3, dest1])
pipe2.add_edges_from([
    (source2, NF1, {'filter': match(srcport = 80)}),
    (NF1, NF3, {'filter':match(srcport = 80)}),
    (NF3, dest1, {'filter': match(srcport = 80)}),
    (NF1, source2, {'filter': match(dstport = 80)}),
    (NF3, NF1, {'filter': match(dstport = 80)}),
    (dest2, NF3, {'filter': match(dstport = 80)}),
    ])

pipe3 = E2Pipelet("pipelet-3")
pipe3.add_nodes_from([source3, NF2, NF3, dest2])
pipe3.add_edges_from([
    (source3, NF2, {'filter': match(srcport = 8000)}),
    (NF2, NF3, {'filter':match(srcport = 8000)}),
    (NF3, dest2, {'filter': match(srcport = 8000)}),
    (NF2, source3, {'filter': match(dstport = 8000)}),
    (NF3, NF2, {'filter': match(dstport = 8000)}),
    (dest2, NF3, {'filter': match(dstport = 8000)}),
    ])

pipe4 = E2Pipelet("pipelet-4")
pipe4.add_nodes_from([source4, NF2, NF3, dest2])
pipe4.add_edges_from([
    (source4, NF2,{'filter':match(srcport = 8000)}),
    (NF2, NF3,{'filter':match(srcport = 8000)}),
    (NF3, dest2,{'filter':match(srcport = 8000)}),
    (NF2, source4, {'filter':match(dstport = 8000)}),
    (NF3, NF2, {'filter':match(dstport = 8000)}),
    (dest2, NF3,{'filter':match(dstport = 8000)})
    ])

pipe5 = E2Pipelet("pipelet-5")
pipe5.add_nodes_from([source5, NF2, NF3, dest2])
pipe5.add_edges_from([
    (source5, NF2,{'filter':match(srcport = 8000)}),
    (NF2, NF3,{'filter':match(srcport = 8000)}),
    (NF3, dest2,{'filter':match(srcport = 8000)}),
    (NF2, source5, {'filter':match(dstport = 8000)}),
    (NF3, NF2, {'filter':match(dstport = 8000)}),
    (dest2, NF3,{'filter':match(dstport = 8000)})
    ])
    
def main():
  pipelets = [pipe1, pipe2, pipe3, pipe4, pipe5]
  e2_main = e2(net, pipelets)
  
  print "==============PGRAPH==============="
  pgraph = e2_main.merge_pipelets(pipelets, "pgraph1")
  print(pgraph.nodes())
  print(pgraph.edges())
  
  # pdb.set_trace()
  
  print "==============IGRAPH==============="
  igraph= e2_main.create_igraph(pgraph, [source1, source2, source3, source4, source5])
  print(igraph.nodes())
  print(igraph.edges(data=True))

  print "==============BIN PACKING==============="
  new_igraph = e2_main.bin_pack(igraph, [source1,source2,source3,source4,source5], bin_capacity)
  
  print "==============UPDATE PIPELETS==============="
  e2_main.policy(new_igraph)
