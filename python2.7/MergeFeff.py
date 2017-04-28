#!/usr/bin/env python
#
# Small script for merging feff-files from FEFF calculations.
#
# Jan Rosdahl
#
import math
import re
import sys
#
# Search patterns
#
ReFeff = re.compile(r"""
    \s+					# Leading spaces
    (\d+\.\d{3})\s+			# k
    ([+-]*\d\.\d{4}E[+-]+\d{2})\s+	# real[2*phc]
    ([+-]*\d\.\d{4}E[+-]+\d{2})\s+	# mag[feff]
    ([+-]*\d\.\d{4}E[+-]+\d{2})\s+	# phase[feff]
    ([+-]*\d\.\d{3}E[+-]+\d{2})\s+	# red factor
    ([+-]*\d\.\d{4}E[+-]+\d{2})\s+	# lambda
    ([+-]*\d\.\d{4}E[+-]+\d{2})		# real[p]
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
    foo = ReFeff.match(line)
    if foo:
        key = int(1000 * float(foo.group(1)))
        tmp = [ float(foo.group(2)),
                float(foo.group(3)),
                float(foo.group(4)),
                float(foo.group(5)),
                float(foo.group(6)),
                float(foo.group(7)) ]
        cur_data = my_data.get(key, [])
        cur_data.append(tmp)
        my_data[key] = cur_data
#
# Calculate the average and print it :-)
#
for my_key in sorted(my_data.keys()):
    my_list = my_data.get(my_key)
    my_real = []
    my_mag = []
    my_phase = []
    my_red = []
    my_lambda = []
    my_realp = []
    for element in my_list:
        my_real.append(element[0])
        my_mag.append(element[1])
        my_phase.append(element[2])
        my_red.append(element[3])
        my_lambda.append(element[4])
        my_realp.append(element[5])
    print ' %6.3f' % (my_key / 1000.0),
    print '%11.4E' % (sum(my_real) / len(my_real)),
    print '%11.4E' % (sum(my_mag) / len(my_mag)),
    print '%10.4E' % (sum(my_phase) / len(my_phase)),
    print '%10.3E' % (sum(my_red) / len(my_red)),
    print '%11.4E' % (sum(my_lambda) / len(my_lambda)),
    print '%11.4E' % (sum(my_realp) / len(my_realp))
