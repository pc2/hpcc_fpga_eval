#!/bin/bash

LOGFILE=powermeasure.csv

echo "" > $LOGFILE


# Start the benchmark

$@ &

bm_pid=$!
# Start power measurements

#
# Output will contain the occurences of "voltage" and "current" in "xbutil dump" in order.
# A row in the csv represents a call of xbutil dump.
# The first four values in a row represent the 12v_pex and 12v_aux volatage and current in millivolt and milliampere = reported power
# What about vccint? --> I2C interface
#


while $(kill -0 $bm_pid); do
    echo $(xbutil dump | grep "voltage\|current" | sed -r "s/.+: \"([0-9]+)\".*/\1/g" | sed -r ':a;N;$!ba;s/\n/,/g' ) >> $LOGFILE
    sleep 0.1
done
