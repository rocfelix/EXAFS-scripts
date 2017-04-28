#!/usr/bin/env python
#
# Small script for generating random numbers and return them
# as a list of numbers.
#
# Tested with Python 2.7.5
#
# Jan Rosdahl
#
import random
import sys
#
# Main routine
#
try:
    my_low = int(sys.argv[1])
    my_high = int(sys.argv[2])
    my_count = int(sys.argv[3])
except IndexError:
    print >> sys.stderr, 'Three integers are required: lower, upper and count'
    exit(1)
for elm in random.sample(range(my_low, my_high + 1), my_count):
    print elm,
print
