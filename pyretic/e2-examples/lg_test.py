##########################################################
# Computer Networks course project, CS6250, Georgia Tech #
##########################################################

from pyretic.e2.lg import *

#
# +--------+                      +---------+
# |        +--------------------->+         |
# | src I  |                      | dest II |
# |        |         +----------->+         |
# +--------+         |            +---------+
#                    |
#                    |
#                    |
# +--------+         |            +---------+
# |        +---------+            |         |
# | src II |                      | dest I  |
# |        +--------------------->+         |
# +--------+                      +---------+
#

# destinations
dest1_l1 = LoadGenerator.dest(7000)
dest2_l1 = LoadGenerator.dest(8000)
dest2_l2 = LoadGenerator.dest(9000)

# src
src1_s1 = LoadGenerator.src("dest2_ip", 8000, 10)
src2_s1 = LoadGenerator.src("dest2_ip", 9000, 10)
src2_s2 = LoadGenerator.src("dest1_ip", 7000, 10)

print '''dest1_l1: {}
dest2_l1: {}
dest2_l2: {}
src1_s1: {}
src2_s1: {}
src2_s2: {}
'''.format(dest1_l1, dest2_l1, dest2_l2, src1_s1, src2_s1, src2_s2)

def main():
    return flood()
