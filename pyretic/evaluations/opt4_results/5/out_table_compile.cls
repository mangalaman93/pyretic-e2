classifier size: 16
print : match: ('switch', 5) ('vlan_pcp', 0) ('vlan_id', 10)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 11)])
 match: ('vlan_pcp', 0) ('vlan_id', 10)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('switch', 2) ('vlan_pcp', 0) ('vlan_id', 4)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 5)])
 match: ('vlan_pcp', 0) ('vlan_id', 4)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('switch', 3) ('vlan_pcp', 0) ('vlan_id', 6)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 7)])
 match: ('vlan_pcp', 0) ('vlan_id', 6)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('srcip', IPv4Network('10.0.0.1/32')) ('switch', 1) ('dstip', IPv4Network('10.0.0.2/32')) ('vlan_pcp', 0) ('vlan_id', 0)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 2)])
 match: ('vlan_pcp', 0) ('vlan_id', 0)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('switch', 4) ('vlan_pcp', 0) ('vlan_id', 8)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 9)])
 match: ('vlan_pcp', 0) ('vlan_id', 8)
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('vlan_pcp', 0) ('vlan_id', 7)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('vlan_pcp', 0) ('vlan_id', 9)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('vlan_pcp', 0) ('vlan_id', 2)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('vlan_pcp', 0) ('vlan_id', 5)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 match: ('vlan_pcp', 0) ('vlan_id', 11)
  -> set([Controller, modify: ('vlan_pcp', 0) ('vlan_id', 3)])
 identity
  -> set([modify: ('vlan_pcp', 0) ('vlan_id', 3)]) 
---------------------------------