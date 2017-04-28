#!/usr/bin/env python
#
# Small script for extracting the geometry from a TeraChem frame
# and return it as a xyz-file suitable for FEFF, with specific index 0.
#
# Peng Liu
#
import math
import re
import sys
#
# Search patterns
#
ReStart = re.compile(r"""
    frame
    \s+
    (\d+)\s+
    xyz \s file \s generated \s by \s terachem
    \s*$
    """, re.X)
ReEnd = re.compile(r"""
    \s+
    Distance \s matrix \s \(angstroms\):
    \s*$
    """, re.X)
RePosition = re.compile(r"""
    \s*				# Leading spaces
    (\w+)\s+			# Atomic name
    ([+-]*\d+\.\d{6,10})\s+	# X
    ([+-]*\d+\.\d{6,10})\s+	# Y
    ([+-]*\d+\.\d{6,10})	# Z
    \s*$			# End of line
    """, re.X)
#
# Global variables
#
my_coords = []
my_elements = {}
#
# Which frame are we interested in?
#
try:
    my_idx = int(sys.argv[1])
except IndexError:
    print >> sys.stderr, 'A frame number is needed!'
    exit(1)
#
# Read the list of absorber and back scatterers.
#
try:
    for (idx, element) in enumerate(sys.argv[2:]):
        tmp_idx = my_elements.get(element, [])
        tmp_idx.append(idx)
        my_elements[element] = tmp_idx
except IndexError:
    print >> sys.stderr, 'A list of absorber and back scatterers is needed!'
    exit(2)

#
# Read in all coordinates
#
found = False
f = sys.stdin
for line in f:
    if found:
        foo = RePosition.match(line)
        if foo:
            try:
                tmp = [ float(foo.group(2)),
                        float(foo.group(3)),
                        float(foo.group(4)),
                        my_elements[foo.group(1)][0] ]
            except KeyError:
                print >> sys.stderr, 'Unknown element %s' % foo.group(1)
                exit(4)
            if (len(my_elements[foo.group(1)]) > 1):
                my_cur_list = my_elements[foo.group(1)]
                my_elements[foo.group(1)] = my_cur_list[1:]
            my_coords.append(tmp)
    foo = ReStart.match(line)
    if foo:
        if (int(foo.group(1)) == my_idx):
            found = True
        elif found:
            break
if (len(my_coords) > 0):
    #
    # Print the found frame.
    #
    for (idx, coord) in enumerate(my_coords):
        print ' %11.6f' % coord[0],
        print '%11.6f' % coord[1],
        print '%11.6f' % coord[2],
        print coord[3]
