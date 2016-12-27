#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re

#defining an error stream, output color
def eprint(*args, **kwargs):
     print(*args, file=sys.stderr, **kwargs)
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
#store list of required parameters
global_parameter_list = []
     
#extract the filename to be compiled
if (len(sys.argv)<2):
     eprint(bcolors.FAIL + "Error: no file-name found. Compilation terminated." + bcolors.ENDC)
     eprint("Expected " + bcolors.WARNING + "<file-name> <parameter-1> <parameter-2> <parameter-3> ... <parameter-n>" + bcolors.ENDC)


