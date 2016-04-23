import  math
from pyretic.e2.pipelet import *
from pyretic.e2.e2 import *

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
# creating NFs,sources,dests
source1 = E2NF("s1", 1,'src1',inp_load_estimate=l1)
source2 = E2NF("s2", 1,'src2',inp_load_estimate=l2)
source3 = E2NF("s3", 1,'src3',inp_load_estimate=l3)
source4 = E2NF("s4", 1,'src4',inp_load_estimate=l4)
source5 = E2NF("s5", 1,'src5',inp_load_estimate=l5)

NF1 = E2NF("s6", 1,'1_1',nf_capacity=nfc1)
NF2 = E2NF("s7", 1, '2_1',nf_capacity=nfc2)
NF3 = E2NF("s8", 1, '3_1',nf_capacity=nfc3)
dest1 = E2NF("s9", 1, 'dst1')
dest2 = E2NF("s10", 1,'dst2')

# create pipelets
pipe1 = E2Pipelet("pipelet-1")
pipe1.add_nodes_from([source1, NF1, NF3, dest1])
pipe1.add_edges_from([(source1, NF1,{'filter':'r1'}),
    (NF1, NF3,{'filter':'r2'}),
    (NF3, dest1,{'filter':'r3'} )])

pipe2 = E2Pipelet("pipelet-2")
pipe2.add_nodes_from([source2, NF1, NF3, dest1])
pipe2.add_edges_from([(source2, NF1,{'filter':'r4'}),
    (NF1, NF3,{'filter':'r5'}),
    (NF3, dest1,{'filter':'r6'} )])

pipe3 = E2Pipelet("pipelet-3")
pipe3.add_nodes_from([source3, NF2, NF3, dest2])
pipe3.add_edges_from([(source3, NF2,{'filter':'r4'}),
    (NF2, NF3,{'filter':'r5'}),
    (NF3, dest2,{'filter':'r6'} )])

pipe4 = E2Pipelet("pipelet-4")
pipe4.add_nodes_from([source4, NF2, NF3, dest2])
pipe4.add_edges_from([(source4, NF2,{'filter':'r4'}),
    (NF2, NF3,{'filter':'r5'}),
    (NF3, dest2,{'filter':'r6'} )])

pipe5 = E2Pipelet("pipelet-5")
pipe5.add_nodes_from([source5, NF2, NF3, dest2])
pipe5.add_edges_from([(source5, NF2,{'filter':'r4'}),
    (NF2, NF3,{'filter':'r5'}),
    (NF3, dest2,{'filter':'r6'} )])


def main():
    e2_main = e2(net, [[pipe1,pipe2,pipe3,pipe4,pipe5]])
    pgraph = e2_main.merge_pipelets([pipe1,pipe2,pipe3,pipe4,pipe5])
    #igraph= e2.create_igraph(pgraph,[source1,source2,source3,source4,source5])
    #e2.bin_pack(iggraph,[source1,source2,source3,source4,source5],bin_capacity)
    something = 1
    return something



