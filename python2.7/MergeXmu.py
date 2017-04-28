#!/usr/bin/env python
#
# Small script for merging xmu-files from FEFF calculations.
#
# Jan Rosdahl
#
import math
import re
import sys
#
# Search patterns
#
ReChi = re.compile(r"""
    \s+					# Leading spaces
    (\d+\.\d{3})\s+			# e
    (-*\d+\.\d{3})\s+			# e(wrt edge)
    (\d+\.\d{3})\s+			# k
    ([+-]*\d\.\d{5}E[+-]+\d{2})\s+	# mu=(1+chi)*mu0
    ([+-]*\d\.\d{5}E[+-]+\d{2})\s+	# mu0
    ([+-]*\d\.\d{5}E[+-]+\d{2})		# chi
    \s*$				# End of line
    """, re.X)
#
# Global variables
#
my_data = {}
#
# Read the data
#
f = sys.stdin
for line in f:
    foo = ReChi.match(line)
    if foo:
        key = int(1000 * float(foo.group(3)))
        tmp = [ float(foo.group(1)),
                float(foo.group(2)),
                float(foo.group(3)),
                float(foo.group(4)),
                float(foo.group(5)),
                float(foo.group(6))]
        cur_data = my_data.get(key, [])
        cur_data.append(tmp)
        my_data[key] = cur_data
#
# Calculate the average and print it :-)
#
for my_key in sorted(my_data.keys()):
    my_list = my_data.get(my_key)
    my_e = []
    my_e_wrt = []
    my_k = []
    my_mu = []
    my_mu0 = []
    my_chi = []
    for element in my_list:
        my_e.append(element[0])
        my_e_wrt.append(element[1])
        my_k.append(element[2])
        my_mu.append(element[3])
        my_mu0.append(element[4])
        my_chi.append(element[5])
    print ' %11.3f' % (sum(my_e) / len(my_e)),
    print ' %9.3f' % (sum(my_e_wrt) / len(my_e_wrt)),
    print ' %6.3f' % (sum(my_k) / len(my_k)),
    print '%12.5E' % (sum(my_mu) / len(my_mu)),
    print '%12.5E' % (sum(my_mu0) / len(my_mu0)),
    print '%12.5E' % (sum(my_chi) / len(my_chi))
