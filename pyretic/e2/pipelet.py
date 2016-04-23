##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

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
        
    def __str__(self):
        return self.name + " " + self.node_id
        
    def __repr__(self):
        return self.__str__()

class E2Pipelet(nx.DiGraph):
    """E2 Pipelet defining end to end flow"""
    def __init__(self, name):
        super(E2Pipelet, self).__init__()
        self.name = name
