#!/bin/bash

# Parse the ppm-power output into a CSV of the format
# Socket0,RAM0,Socket1,RAM1
#
# where Socket is the power consumption of the CPU on the socket 0 or 1 and RAM the power cosumption of the RAM blocks for both sockets.
# All values are in Watts (W).

cat pcm-power.dat | grep "Watts:" | gsed -r 's/.*: ([0-9]+)\.([0-9]+).*/\1.\2/g' | gsed -r ':a;N;$!ba;s/\n/,/g' | gsed -r 's/([^,]*,[^,]*,[^,]*,[^,]*),/\1\n/g' | tee parsed_watts.csv 