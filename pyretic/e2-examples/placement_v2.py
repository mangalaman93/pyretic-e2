import  math
import networkx as nx
class E2NF(object):
    """Network Function for E2"""
    def __init__(self, name, num_instance,node_id,nf_capacity=None,switch_placed=None,inp_load_estimate=None):
        super(E2NF, self).__init__()
        self.name = name
        self.num_instance = num_instance
        self.node_id = node_id
        self.nf_capacity=nf_capacity
        self.inp_load_estimate= inp_load_estimate
        self.switch_placed = switch_placed

    def __hash__(self):
        return self.name.__hash__()

class E2Pipelet(nx.DiGraph):
    """E2 Pipelet defining end to end flow"""
    def __init__(self, name):
        super(E2Pipelet, self).__init__()
        self.name = name

##loads generated
l1 = 4
l2 = 4
l3 = 4
l4 = 4
l5 = 4
nfc1 = 5
nfc2 = 10
nfc3 = 4

# creating NFs
source1 = E2NF("s1", 1,'src1',inp_load_estimate=l1)
source2 = E2NF("s2", 1,'src2',inp_load_estimate=l2)
source3 = E2NF("s3", 1,'src3',inp_load_estimate=l3)
source4 = E2NF("s4", 1,'src4',inp_load_estimate=l4)
source5 = E2NF("s5", 1,'src5',inp_load_estimate=l5)

NF1 = E2NF("s6", 1,'1_1',nf_capacity=nfc1)
NF2 = E2NF("s7", 1, '2_1',nf_capacity=nfc2)
NF3 = E2NF("s8", 1, '3_1',nf_capacity=nfc3)
dest1 = E2NF("s9", 1, 'dst1(')
dest2 = E2NF("s10", 1,'dst2')

# adding filters
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

def merge_pipelets(pipelets_list):
    for i in range(len(pipelets_list)):
        if i==0:
            pgraph = pipelets_list[i]
        else:
            pgraph= nx.compose(nx.DiGraph(pgraph),nx.DiGraph(pipelets_list[i]))

    return pgraph

def create_igraph(pgraph,pipelets_sources):
    igraph = E2Pipelet('igraph')
    igraph.add_nodes_from(pgraph.nodes())
    NF1_2 = E2NF("s11", 1,'1_2',nf_capacity=nfc1)
    NF2_2 = E2NF("s12", 1, '2_2',nf_capacity=nfc2)
    NF3_2 = E2NF("s13", 1, '3_2',nf_capacity=nfc3)
    NF3_3 = E2NF("s14", 1, '3_3',nf_capacity=nfc3)
    NF3_4 = E2NF("s15", 1, '3_4',nf_capacity=nfc3)
    NF3_5 = E2NF("s16", 1, '3_5',nf_capacity=nfc3)

    igraph.add_nodes_from([NF1_2,NF2_2,NF3_2,NF3_3,NF3_4,NF3_5])
    igraph.add_edge(source1,NF1_2,{'filter':'r1'})
    igraph.add_edge(source2,NF1,{'filter':'r4'})
    igraph.add_edge(source3,NF2,{'filter':'r4'})

    igraph.add_edge(source4,NF2,{'filter':'r4'})
    igraph.add_edge(source5,NF2_2,{'filter':'r4'})
    igraph.add_edge(NF1_2,NF3,{'filter':'r2'})
    igraph.add_edge(NF1,NF3_2,{'filter':'r5'})
    igraph.add_edge(NF2,NF3_3,{'filter':'r5'})
    igraph.add_edge(NF2,NF3_4,{'filter':'r5'})
    igraph.add_edge(NF2_2,NF3_5,{'filter':'r5'})
    return igraph

def bin_pack(igraph,pipelets_sources,bin_capacity):
    list_of_srcs= list(pipelets_sources)
    node_list=[]
    for src in list_of_srcs:
        for edge in nx.dfs_edges(igraph,src):
            if edge[1] in node_list:
                pass
            else:
                node_list.append(edge[1])
    bin_full = 0
    bin_num = 0 
    cap_sum = 0         
    for node in node_list:
        cap_sum = cap_sum + node.nf_capacity
        if cap_sum <= bin_capacity:
            node.switch_placed = "s"+str(bin_num)
            print node.switch_placed,node.node_id,node.nf_capacity
        else:     
            cap_sum = node.nf_capacity
            bin_num =bin_num + 1
            node.switch_placed = "s"+str(bin_num)
            print node.switch_placed,node.node_id,node.nf_capacity
 


"""    cap_sum=0
    bin_num=0
    for node in node_list:
        #bin_num = cap_sum/bin_capacity
        cap_sum = cap_sum + node.nf_capacity
        if cap_sum<(bin_num+1)*bin_capacity:
            node.switch_placed = "s"+str(bin_num)
            print "ifless",node.switch_placed,node.node_id,node.nf_capacity
        else:
            bin_num =bin_num + 1
            node.switch_placed = "s"+str(bin_num)
            print "else",node.switch_placed,node.node_id,node.nf_capacity
    #for n in igraph.nodes():
    #    print n.node_id,n.switch_placed,n.nf_capacity
"""

def calc_instances(pgraph,pipelets_sources):
    number_of_instances= dict()
    first_level=[]
    for src in pipelets_sources:
        first_level.append(pgraph.successors(src)[0])

    for node in set(first_level):
        pred_list = pgraph.predecessors(node)
        load_sum = 0

        for p in pred_list:
            load_sum = load_sum + p.inp_load_estimate
            #print p.node_id,load_sum
        #print "nfc",node.nf_capacity

        node.inp_load_estimate=load_sum

        num_inst =math.ceil(float(load_sum)/node.nf_capacity)
        key_nf = node.node_id
        number_of_instances[key_nf]=num_inst

    second_level=[]
    for s in first_level:
        second_level.append(pgraph.successors(s)[0])

    for node in set(second_level):
        pred_list = pgraph.predecessors(node)
        num_inst = 0
        for p in pred_list:

            num_inst += math.ceil(float(p.inp_load_estimate)/node.nf_capacity)
        key_nf = node.node_id
        number_of_instances[key_nf]=num_inst
        #print number_of_instances

    igraph = E2Pipelet("igraph")
    #igraph.add_nodes_from(pgraph.nodes())
    for node in set(first_level):
        num_inst_new=0
        pred_list = pgraph.predecessors(node)
        s = 0
        flag =0
        for p in pred_list:
            #print p.node_id
            s += p.inp_load_estimate
            if s>node.nf_capacity:
                num_inst_new +=1
                nid = node.node_id[0]+"_"+str(num_inst_new)
                name = "s"+str(nx.number_of_nodes(pgraph))
                nfc = node.nf_capacity
                ld_est = p.inp_load_estimate
                new_node = E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=ld_est)
                igraph.add_node(new_node)
                filter_val = pgraph[p][node]['filter']
                igraph.add_edge(p,new_node,{'filter':filter_val})
                #print "ifedge",p.node_id,new_node.node_id,filter_val
                #print "if",s,ld_est,nid,name,num_inst_new
            else:
                if flag!=1:
                    num_inst_new +=1
                    nid = node.node_id[0]+"_"+str(num_inst_new)
                    name = "s"+str(nx.number_of_nodes(pgraph))
                    nfc = node.nf_capacity
                    ld_est = p.inp_load_estimate
                    new_node = E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=ld_est)
                    igraph.add_node(new_node)
                    filter_val = pgraph[p][node]['filter']
                    igraph.add_edge(p,new_node,{'filter':filter_val})
                    ##print "else_edge",p.node_id,new_node.node_id,filter_val
                    #print "else",s,ld_est,nid,name,num_inst_new
                    flag = 1
                else:
                    nid = node.node_id[0]+"_"+str(num_inst_new)
                    name = "s"+str(nx.number_of_nodes(pgraph))
                    nfc = node.nf_capacity
                    ld_est = p.inp_load_estimate
                    #new_node = E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=ld_est)
                    #igraph.add_node(new_node)
                    filter_val = pgraph[p][node]['filter']
                    igraph.add_edge(p,new_node,{'filter':filter_val})
                    #print "else_edge",p.node_id,new_node.node_id,filter_val
                    #print "else",s,ld_est,nid,name,num_inst_new
    first_level_ig=[]
    for src in pipelets_sources:
        first_level_ig.append(pgraph.successors(src)[0])

    second_level_ig=[]
    for s in first_level_ig:
        second_level_ig.append(pgraph.successors(s)[0])

    #for node in set(second_level):
    for node in set(second_level_ig):
        print "node",node.node_id
        num_inst_new=0
        pred_list = pgraph.predecessors(node)
        #pred_list = first_level
        s = 0
        flag =0
        for p in pred_list:
            print p.node_id
            s += p.inp_load_estimate
            if s>node.nf_capacity:
                num = p.inp_load_estimate/node.nf_capacity
                for i in range(num):
                    num_inst_new +=1
                    nid = node.node_id[0]+"_"+str(num_inst_new)
                    name = "s"+str(nx.number_of_nodes(pgraph))
                    nfc = node.nf_capacity
                    ld_est = p.inp_load_estimate
                    new_node = E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=ld_est)
                    igraph.add_node(new_node)
                    filter_val = pgraph[p][node]['filter']
                    igraph.add_edge(p,new_node,{'filter':filter_val})
                    print "ifedge",p.node_id,new_node.node_id,filter_val
                    #print "if",s,ld_est,nid,name,num_inst_new
            else:
                if flag!=1:
                    num_inst_new +=1
                    nid = node.node_id[0]+"_"+str(num_inst_new)
                    name = "s"+str(nx.number_of_nodes(pgraph))
                    nfc = node.nf_capacity
                    ld_est = p.inp_load_estimate
                    new_node = E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=ld_est)
                    igraph.add_node(new_node)
                    filter_val = pgraph[p][node]['filter']
                    igraph.add_edge(p,new_node,{'filter':filter_val})
                    print "else_edge",p_node_id,new_node.node_id,filter_val
                    #print "else",s,ld_est,nid,name,num_inst_new
                    flag = 1
                else:
                    nid = node.node_id[0]+"_"+str(num_inst_new)
                    name = "s"+str(nx.number_of_nodes(pgraph))
                    nfc = node.nf_capacity
                    ld_est = p.inp_load_estimate
                    #new_node = E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=ld_est)
                    #igraph.add_node(new_node)
                    filter_val = pgraph[p][node]['filter']
                    igraph.add_edge(p,new_node,{'filter':filter_val})
                    print "else_edg2",p.node_id,new_node.node_id,filter_val

    for e in igraph.edges():
        print e[0].node_id,e[1].node_id,igraph[e[0]][e[1]]['filter']
    """
        for i in range(int(number_of_instances[node.node_id]-1)):
            nid = node.node_id[0]+"_"+str(i+1+1)
            name = "s"+str(nx.number_of_nodes(pgraph))
            nfc = node.nf_capacity
            pred_list = pgraph.predecessors(node)
            #load_est = float(node.inp_load_estimate)/number_of_instances[node.node_id]
            print node.node_id,node.inp_load_estimate
            igraph.add_node(E2NF(name,1,nid,nf_capacity=nfc))
            print node.node_id,load_est,nid
    for node in set(second_level):
        for i in range(int(number_of_instances[node.node_id]-1)):
            print node.inp_load_estimate
            nid = node.node_id[0]+"_"+str(i+1+1)
            name = "s"+str(nx.number_of_nodes(pgraph))
            nfc = node.nf_capacity
            load_est = float(node.inp_load_estimate)/number_of_instances[node.node_id]
            igraph.add_node(E2NF(name,1,nid,nf_capacity=nfc,inp_load_estimate=load_est))
            print node.node_id,nid
    """
g1 = merge_pipelets([pipe1,pipe2,pipe3,pipe4,pipe5])
g2 = create_igraph(g1,[source1,source2,source3,source4,source5])
#g2 = calc_instances(g1,[source1,source2,source3,source4,source5])
bin_pack(g2,[source1,source2,source3,source4,source5],10)





