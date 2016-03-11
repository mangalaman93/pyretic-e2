##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

"""E2 implementation using pyreric and mininet"""
from pyretic.lib.std import *
import importlib

class e2():
    def __init__(self, pol):
        super(ft, self).__init__()

    def create_mininet_network(path_to_file,class_name):
	#get mininet class from file
        module = importlib.import_module(path_to_file)
	mininet_class = getattr(module, class_name)
	net = mininet_class()
	#create the  topology
        net.start()
        CLI(net)
        net.stop()
        return mininet_class
