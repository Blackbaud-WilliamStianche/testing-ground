__author__ = 'William Stianche'

#!/usr/bin/python

import datetime
import json
import os
import subprocess
output = []
process_name = "Xorg"
ps_output = subprocess.check_output(["ps","-C",process_name])
for line in ps_output.splitlines():
    x = []
    for item in line.split():
        x.append(item)
    print "Printing X"
    print x
    output.append(x)

print "Printing output"
print output