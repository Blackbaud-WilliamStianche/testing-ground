__author__ = 'William Stianche'

#!/usr/bin/python

import datetime
import json
import os
import subprocess

process_name = "Xorg"
ps_output = subprocess.check_output(["ps","-C",process_name])
header_line = true
for line in ps_output.splitlines():
    lines = line.split()

print lines