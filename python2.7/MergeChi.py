#!/usr/bin/env python
#
# Small script for merging chi-files from FEFF calculations.
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
    (\d+\.\d{4})\s+			# k
    ([+-]*\d\.\d{6}E[+-]+\d{2})\s+	# chi
    ([+-]*\d\.\d{6}E[+-]+\d{2})\s+	# mag
    ([+-]*\d\.\d{6}E[+-]+\d{2})		# phase
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
        key = int(10000 * float(foo.group(1)))
        tmp = [ float(foo.group(2)),
                float(foo.group(3)),
                float(foo.group(4)) ]
        cur_data = my_data.get(key, [])
        cur_data.append(tmp)
        my_data[key] = cur_data
#
# Calculate the average and print it :-)
#
for my_key in sorted(my_data.keys()):
    my_list = my_data.get(my_key)
    my_chi = []
    my_mag = []
    my_phase = []
    for element in my_list:
        my_chi.append(element[0])
        my_mag.append(element[1])
        my_phase.append(element[2])
    print ' %10.4f' % (my_key / 10000.0),
    print ' %14.6E' % (sum(my_chi) / len(my_chi)),
    print ' %12.6E' % (sum(my_mag) / len(my_mag)),
    print ' %12.6E' % (sum(my_phase) / len(my_phase))
