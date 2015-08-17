__author__ = 'William Stianche'

#!/usr/bin/python

import datetime
import json
import os
import subprocess

process_name = "Xorg"
ps_output = subprocess.check_output(["ps","-fC",process_name])
for line in iter(ps_output):
    print line
