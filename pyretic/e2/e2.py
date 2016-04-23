##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

"""E2 implementation using pyreric and mininet"""
from pyretic.e2.pipelet import *
from pyretic.e2.e2 import *
from pyretic.lib.corelib import *
from pyretic.lib.std import *

class e2():
    def __init__(self, net, pipelets):
        self.net = net
        self.pipelets = pipelets[0]

    def policy(self):
        nodedict = {}
        interfaces = {}
        port = {}
        policy = None
        ipmap = {}

        for s in self.net.switches:
            port[s.name] = s.dpid

        for host in self.net.hosts:
            ipmap[host.name] = host.IP()

        print self.net.links
        
        for link in self.net.links:
            pos = link.intf1.name.split("-")[1].rindex("h") + 1
            # if it is a host link
            if link.intf1.name.split("-")[0][0] == 'h':
                host = link.intf1.name.split("-")[0]
                rule = (match(switch = int(port[link.intf2.name.split("-")[0]]), dstip=ipmap[host]) >> fwd(int(link.intf2.name.split("-")[1][pos:])))
                if policy is None:
                    policy = rule
                else:
                    policy += rule

            if link.intf2.name.split("-")[0][0] == 'h':
                host = link.intf2.name.split("-")[0]
                rule = (match(switch = int(port[link.intf1.name.split("-")[0]]), dstip=ipmap[host]) >> fwd(int(link.intf1.name.split("-")[1][pos:])))
                if policy is None:
                    policy = rule
                else:
                    policy += rule

            if link.intf1.name.split("-")[0] not in interfaces:
                interfaces[link.intf1.name.split("-")[0]] = {}
            if link.intf2.name.split("-")[0] not in interfaces:
                interfaces[link.intf2.name.split("-")[0]] = {}
            interfaces[link.intf1.name.split("-")[0]][link.intf2.name.split("-")[0]] = link.intf1.name.split("-")[1][pos:]
            interfaces[link.intf2.name.split("-")[0]][link.intf1.name.split("-")[0]] = link.intf2.name.split("-")[1][pos:]

        for edge in self.pipelets.edges(data=True):
             if edge[0].name not in nodedict:
                nodedict[edge[0].name] = []
             nodedict[edge[0].name].append(edge)

        for sw in port.keys():
            route  = None
            if sw in nodedict:
                for rule in nodedict[sw]:
                    if route is None:
                        route = (rule[2]['filter'] >> fwd(int(interfaces[sw][rule[1].name])))
                    else:
                        route = route + (rule[2]['filter'] >> fwd(int(interfaces[sw][rule[1].name])))
                if policy is None:
                    policy = (match(switch = int(port[sw])) >> route)
                else:
                    policy += (match(switch = int(port[sw])) >> route)
        return policy

    def merge_pipelets(self, pipelets_list, graph_name):
        """
        function to get pgraph
        """
        for i in range(len(pipelets_list)):
            if i==0:
                pgraph = pipelets_list[i]
            else:
                pgraph = nx.compose(nx.DiGraph(pgraph),nx.DiGraph(pipelets_list[i]))
        
        pgraph.name = graph_name
        
        return pgraph
    
    def create_igraph(self, pgraph,pipelets_sources):
        """
        function to get igraph
        """
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
        
        igraph.add_edge(NF3,dest1,{'filter':'r4'})
        igraph.add_edge(NF3_2, dest1, {'filter':'r4'})
        igraph.add_edge(NF3_3, dest2,{'filter':'r2'})
        igraph.add_edge(NF3_4, dest2,{'filter':'r5'})
        igraph.add_edge(NF3_5,dest1,{'filter':'r5'})
        
        return igraph
    
    def bin_pack(self, igraph, pipelets_sources, bin_capacity):
        """
        function to bin pack the NF instances
        """
        print "Enter binpack"
        switches_places = {}
        list_of_srcs= list(pipelets_sources)
        node_list=[]
        print "Sources", list_of_srcs
        print "Nodes", igraph.nodes()
        for src in list_of_srcs:
            print "DFS EDGES", list(nx.dfs_edges(igraph,src))
            for edge in list(nx.dfs_edges(igraph,src)):
                print  "Edge", edge
                if edge[1] in node_list:
                    pass
                else:
                    node_list.append(edge[1])
        bin_full = 0
        bin_num = 0 
        cap_sum = 0  
        print "Node list", node_list
        for node in node_list:
            print node
            cap_sum = cap_sum + node.nf_capacity
            if cap_sum <= bin_capacity:
                node.switch_placed = "s"+str(bin_num)
                print node.switch_placed,node.node_id,node.nf_capacity
            else:     
                cap_sum = node.nf_capacity
                bin_num =bin_num + 1
                node.switch_placed = "s"+str(bin_num)
                print node.switch_placed,node.node_id,node.nf_capacity
