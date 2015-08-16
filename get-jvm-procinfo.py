__author__ = 'William Stianche'

#!/usr/bin/python

import datetime
import json
import os
import subprocess

psj = subprocess.call("ps", "-fC", "java")
for process in iter(psj.stdout.readline, ''):
    print process,
