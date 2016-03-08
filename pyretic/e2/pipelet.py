##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

import networkx as nx

class E2NF(object):
    """Network Function for E2"""
    def __init__(self, name, num_instance):
        super(E2NF, self).__init__()
        self.name = name
        self.num_instance = num_instance

    def __hash__(self):
        return self.name.__hash__()

class E2Pipelet(nx.DiGraph):
    """E2 Pipelet defining end to end flow"""
    def __init__(self, name):
        super(E2Pipelet, self).__init__()
        self.name = name
