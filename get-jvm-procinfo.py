__author__ = 'William Stianche'

#!/usr/bin/python

import datetime
import json
import os
import subprocess

process_name = "Xorg"
psj = subprocess.call(["ps","-fC",process_name])
for process in iter(psj.stdout.readline, ''):
    print process,
