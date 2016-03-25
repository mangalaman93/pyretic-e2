##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

"""E2 implementation using pyreric and mininet"""
from pyretic.lib.corelib import *
from pyretic.lib.std import *
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.link import Link, TCLink

my_helper=None
class e2():
    def __init__(self, net, pipelets, helper):
        global my_helper
	self.net = net
        self.pipelets = pipelets[0]
        my_helper = helper

    def start(self):
	global my_helper
        nodedict = {}
        interfaces={}
        port={}
        for s in self.net.switches:
            #print s.name, s.dpid, s.listenPort, s.defaultDpid()
            port[s.name] = s.dpid

        for link in self.net.links:
            if link.intf1.name.split("-")[0] not in interfaces:
                interfaces[link.intf1.name.split("-")[0]] = {}
            pos = link.intf1.name.split("-")[1].rindex("h")+1
            interfaces[link.intf1.name.split("-")[0]][link.intf2.name.split("-")[0]] = link.intf1.name.split("-")[1][pos:]

        for edge in self.pipelets.edges(data=True):
             if edge[0].name not in nodedict:
                nodedict[edge[0].name] = []
             nodedict[edge[0].name].append(edge)

        allroutes = None
        for sw in port.keys():
            route  =None
            #print "Rule for ", sw
            if sw in nodedict:
                for rule in nodedict[sw]:
                    if route is None:
                        route = rule[2]['filter'] >> fwd(interfaces[sw][rule[1].name])
                    else:
                        route = route + rule[2]['filter'] >> fwd(interfaces[sw][rule[1].name])
                if allroutes is None:
                    allroutes = (match(switch = port[sw]) >> route)
                else:
                    allroutes += (match(switch = port[sw]) >> route)
            #print route
        #print allroutes
        my_helper()
	return allroutes
	#self.net.stop()
        #return flood()
