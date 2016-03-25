##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

"""E2 implementation using pyreric and mininet"""
from pyretic.lib.corelib import *
from pyretic.lib.std import *

class e2():
    def __init__(self, net, pipelets, helper):
        self.net = net
        self.piplets = pipelets
        self.helper = helper

    def start(self):
        return flood()

# # for edge in fifa.edges(data=True):
# #     if edge[0].name not in nodedict:
# #         nodedict[edge[0].name] = []

# #     nodedict[edge[0].name].append(edge)

# interfaces={}
# port={}
# for s in net.switches:
#     port[s.name] = s.listenPort

# for link in net.links:
#     if link.intf1.name.split("-")[0] not in interfaces:
#         interfaces[link.intf1.name.split("-")[0]] = {}
#     pos = link.intf1.name.split("-")[1].rindex("h")+1
#     interfaces[link.intf1.name.split("-")[0]][link.intf2.name.split("-")[0]] = link.intf1.name.split("-")[1][pos:]

# for edge in fifa.edges(data=True):
#      if edge[0].name not in nodedict:
#         nodedict[edge[0].name] = []
#      nodedict[edge[0].name].append(edge)

# allroutes = None
# for sw in port.keys():
#     route  =None
#     #print "Rule for ", sw
#     if sw in nodedict:
#         for rule in nodedict[sw]:
#             if route is None:
#                 route = rule[2]['filter'] >> fwd(interfaces[sw][rule[1].name])
#             else:
#                 route = route + rule[2]['filter'] >> fwd(interfaces[sw][rule[1].name])
#         if allroutes is None:
#             allroutes = (match(srcport = port[sw]) >> route)
#         else:
#             allroutes += (match(srcport = port[sw]) >> route)
#     #print route
# print allroutes
# net.stop()
