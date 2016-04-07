##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

"""E2 implementation using pyreric and mininet"""
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
