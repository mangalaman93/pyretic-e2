import networkx as nx
class E2NF(object):
    """Network Function for E2"""
    def __init__(self, name, num_instance,node_id,nf_capacity=None,switch_placed=None):
        super(E2NF, self).__init__()
        self.name = name
        self.num_instance = num_instance
        self.node_id = node_id
        self.nf_capacity=nf_capacity
        self.switch_placed = switch_placed

    def __hash__(self):
        return self.name.__hash__()

class E2Pipelet(nx.DiGraph):
    """E2 Pipelet defining end to end flow"""
    def __init__(self, name):
        super(E2Pipelet, self).__init__()
        self.name = name

##loads generated
l1 = 10
l2 = 10

# creating NFs
source1 = E2NF("s1", 1,'src1',l1)
source2 = E2NF("s2", 1,'src2',l2)
NF1 = E2NF("s3", 1,'1_1',l1)
NF2 = E2NF("s4", 1, '1_1',l1/2)
NF3 = E2NF("s5", 1, '1_1',l1/3)
dest1 = E2NF("s6", 1, 'dst1')
dest2 = E2NF("s7", 1,'dst2')

# adding filters
fifa1 = E2Pipelet("pipelet-x")
fifa1.add_nodes_from([source1, NF1, NF2, dest1])
fifa1.add_edges_from([(source1, NF1,{'filter':'r1'}),
    (NF1, NF2,{'filter':'r2'}),
    (NF2, dest1,{'filter':'r3'} )])

# adding filters
fifa2 = E2Pipelet("pipelet-y")
fifa2.add_nodes_from([source2, NF1, NF3, dest2])
fifa2.add_edges_from([(source2, NF1,{'filter':'r4'}),
    (NF1, NF3,{'filter':'r5'}),
    (NF3, dest2,{'filter':'r6'} )])




def placement_output(input_pipelets,Source_nodes, Source_Loads):
	"""
	this function returns the placed output as a pipelet class itself
	"""
    ##do all placement algo
    l1=10
    l2 =10
    source1 = E2NF("s1", 1,'src1',l1,'s7')
    source2 = E2NF("s2", 1,'src2',l2,'s8')
    NF1_1 = E2NF("s3", 1, '1_1',l1,'s4')
    NF2_1 = E2NF("s4", 1, '2_1',l1/2,'s3')
    NF3_1 = E2NF("s5", 1, '3_1',l1/3,'s5')
    dest1 = E2NF("s6", 1,'dst1','s9')
    dest2 = E2NF("s7", 1,'dst2','s10')

    NF1_2= E2NF("s8",1,'1_2',l1,'s1')
    NF2_2= E2NF("s9",1,'2_2',l1/2,'s3')
    NF3_2= E2NF("s10",1,'3_2',l1/2,'s2')
    NF3_3= E2NF("s11",1,'3_3',l1/3,'s5')


    fifa = E2Pipelet("placed_out")
    fifa.add_nodes_from([source1,NF1_1,NF1_2,NF2_1,NF2_2,dest1,source2,NF3_1,NF3_2,NF3_3,dest2])

    fifa.add_edges_from([
        (source1, NF1_1,{'filter':'r1','weight':l1/2}),
        (source1, NF1_2,{'filter':'r1','weight':l1/2}),
        (NF1_1, NF2_1,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_1, NF2_2,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_1, NF3_1,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_1, NF3_2,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_1, NF3_3,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_2, NF2_1,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_2, NF2_2,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_2, NF3_1,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_2, NF3_2,{'filter':'r2','weight':(l1+l2)/10}),
        (NF1_2, NF3_3,{'filter':'r2','weight':(l1+l2)/10}),
        (NF2_1, dest1,{'filter':'r3','weight':(l1+l2)/5} ),
        (NF3_1, dest2,{'filter':'r3','weight':(l1+l2)/5} ),
        (NF3_2, dest2,{'filter':'r3','weight':(l1+l2)/5} ),
        (NF3_3, dest2,{'filter':'r3','weight':(l1+l2)/5} ),
        (NF2_2, dest1,{'filter':'r3','weight':(l1+l2)/5} ),
        (source2, NF1_1,{'filter':'r4','weight':l2/2}),
        (source2, NF1_2,{'filter':'r4','weight':l2/2})])

    return fifa

placed_graph = placement_output([fifa1,fifa2],[source1,source2],[l1,l2])

