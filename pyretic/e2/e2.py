##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

"""E2 implementation using pyreric and mininet"""
from pyretic.e2.pipelet import *
from pyretic.e2.e2 import *
from pyretic.lib.corelib import *
from pyretic.lib.std import *

# helper function for creating igraph
# either finds an existing instance for the given amount of load
#     or creates a new instance of the given network function
#     it used E2NF.other variable to keep track of instances that it creates
def find_or_create_instance(load, nf):
    if nf.other:
        for instance in nf.other:
            if instance.nf_capacity >= (load + instance.inp_load_estimate):
                instance.inp_load_estimate += load
                return instance
    else:
        nf.other = []
    num = len(nf.other) + 1
    instance = E2NF(nf.name, num, nf.node_id+"_"+str(num),
        nf_capacity=nf.nf_capacity, inp_load_estimate=load)
    nf.other.append(instance)
    return instance

# helper function for creating igraph
# annotates the edge with correct filters and adds the edge (and hence nodes)
#  to the given igraph
def update_igraph(igraph, node1_instance, node2_instance, filter_dict, source):
    # add filter
    if 'source' in filter_dict:
        filter_dict['source'].append(source)
    else:
        filter_dict['source'] = [source]
    igraph.add_edge(node1_instance, node2_instance, filter_dict)

class e2():
    def __init__(self, net, pipelets):
        self.net = net
        self.pipelets = pipelets

    def switch_dict(self):
        switches = {}
        for s in self.net.switches:
            switches[s.name] = s
        return switches
        
    def dpid_dict(self):
        dpid = {}
        for s in self.net.switches:
            dpid[s.name] = s.dpid
        return dpid

    def host_dict(self):
        ipmap = {}
        for host in self.net.hosts:
            ipmap[host.name] = host.IP()
        return ipmap

    def policy(self, igraph, pipelets_sources, hws):
        nodedict = {}
        interfaces = {}
        policy = None
        dpid = self.dpid_dict()
        ipmap = self.host_dict()
        switches = self.switch_dict()
        
        #print "DPID", dpid
        
        #print "IPMAP", ipmap
        
        #print "SWITCH", switches
        
        for link in self.net.links:
            pos = link.intf1.name.split("-")[1].rindex("h") + 1
            print link.intf1.name, "   ", link.intf2.name
            # if it is a host link
            if link.intf1.name.split("-")[0][0] == 'h':
                host = link.intf1.name.split("-")[0]
                rule = (match(switch = int(dpid[link.intf2.name.split("-")[0]]), dstip=ipmap[host]) >> fwd(int(link.intf2.name.split("-")[1][pos:])))
                if policy is None:
                    policy = rule
                else:
                    policy += rule

            if link.intf2.name.split("-")[0][0] == 'h':
                host = link.intf2.name.split("-")[0]
                rule = (match(switch = int(dpid[link.intf1.name.split("-")[0]]), dstip=ipmap[host]) >> fwd(int(link.intf1.name.split("-")[1][pos:])))
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
        
        #print "INTERFACES", interfaces
        
        for source in pipelets_sources:
            for edge in list(nx.dfs_edges(igraph, source)):
                node1 = edge[0]
                node2 = edge[1]
                
                #print "NODE1-> ", node1.name, " NODE2-> ", node2.name
                
                src_sw = node1.switch_placed
                dst_sw = node2.switch_placed
                
                print "SOURCE SW-> ", src_sw, " DEST SW-> ", dst_sw
                
                data = igraph.get_edge_data(node1, node2)
                filters = data['filter']
                sources = data['source']
                ip = ipmap[source.name]
                
                hws_inport = int(interfaces[hws][src_sw])
                src_inport = int(interfaces[src_sw][hws])
                
                if node1.node_id[:3] == 'src':
                    assert (node1 in sources)
                    # rule from source switch to hardware switch
                    policy += ((match(switch=int(dpid[src_sw]), srcip=ip) >> filters) >> fwd(int(interfaces[src_sw][hws])))
                    # rule from hardware switch to a switch connected to node2
                    policy += ((match(switch=int(dpid[hws]), srcip=ip, inport=hws_inport) >> filters) >> fwd(int(interfaces[hws][dst_sw])))
                elif node2.node_id[:3] == 'dst':
                    assert (source in sources)
                    # rule from source switch to hardware switch
                    policy += ((match(switch=int(dpid[src_sw]), srcip=ip, inport=src_inport) >> filters) >> fwd(int(interfaces[src_sw][hws])))
                    # rule from hardware switch to a switch connected to node2
                    policy += ((match(switch=int(dpid[hws]), srcip=ip, inport=hws_inport) >> filters) >> fwd(int(interfaces[hws][dst_sw])))
                else:
                    if src_sw == dst_sw:
                        continue
                    if not source in sources:
                        continue
                    # rule from source switch to hardware switch
                    policy += ((match(switch=int(dpid[src_sw]), srcip=ip, inport=src_inport) >> filters) >> fwd(int(interfaces[src_sw][hws])))
                    # rule from hardware switch to a switch connected to node2
                    policy += ((match(switch=int(dpid[hws]), srcip=ip, inport=hws_inport) >> filters) >> fwd(int(interfaces[hws][dst_sw])))
        print policy
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
    
    def bin_pack(self, igraph, sources, bin_capacity):
        """
        function to bin pack the NF instances
        """
        #print "Enter binpack"
        switches_places = {}
        
        node_list=[]
        #print "Nodes", igraph.nodes()
        #print "Edges", igraph.edges()

        for src in sources:
            #print "DFS EDGES", src, list(nx.dfs_edges(igraph,src))
            for edge in list(nx.dfs_edges(igraph,src)):
                #print  "Edge", edge
                if edge[1] in node_list:
                    pass
                else:
                    node_list.append(edge[1])
        bin_full = 0
        bin_num = 1 
        cap_sum = 0  
        #print "Node list", node_list
        for node in node_list:
            if node.node_id[0]=='d' or node.node_id[0]=='s':
                continue
            cap_sum = cap_sum + node.nf_capacity
            if cap_sum <= bin_capacity:
                node.switch_placed = "s"+str(bin_num)
                print node.switch_placed,node.node_id,node.nf_capacity
            else:     
                cap_sum = node.nf_capacity
                bin_num =bin_num + 1
                node.switch_placed = "s"+str(bin_num)
                print node.switch_placed,node.node_id,node.nf_capacity
        return igraph

    def should_I_add_an_edge_to_dest_from_src(self, src, dest):
        for pipelet in self.pipelets:
            count = 0
            for (n1, n2) in pipelet.edges():
                if n1 == src:
                    count += 1
                elif n2 == dest:
                    count += 1
            if count == 2:
                return True
        return False
    
    # Assumptions - one instance can handle all the load from one source
    # - source and destination are never connected directly
    # - source nodes are named with prefix "src" without quotes
    def create_igraph(self, pgraph, pipelets_sources):
        igraph = E2Pipelet('igraph')
        for src in pipelets_sources:
            # nf -> nf instance, keeps track of the assigned instance for this source
            current_instance = {}
            
            #print "DFS Edges:", list(nx.dfs_edges(pgraph, src))
            
            for edge in list(nx.dfs_edges(pgraph, src)):
                node1 = edge[0]
                node2 = edge[1]
                #print "Nodes:", node1, node2
                
                if node1.node_id[:3] == 'src':
                    node2_instance = find_or_create_instance(node1.inp_load_estimate, node2)
                    update_igraph(igraph, node1, node2_instance, pgraph.get_edge_data(node1, node2), src)
                    assert not (node2 in current_instance)
                    current_instance[node2] = node2_instance
                elif node2.node_id[:3] == 'dst':
                    if self.should_I_add_an_edge_to_dest_from_src(src, node2):
                        node1_instance = current_instance[node1]
                        update_igraph(igraph, node1_instance, node2, pgraph.get_edge_data(node1, node2), src)
                else:
                    node1_instance = current_instance[node1]
                    load = node1_instance.inp_load_estimate
                    node2_instance = find_or_create_instance(load, node2)
                    update_igraph(igraph, node1_instance, node2_instance, pgraph.get_edge_data(node1, node2), src)
                    assert not (node2 in current_instance)
                    current_instance[node2] = node2_instance
        # print list(igraph.edges())
        return igraph
