#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re
import math
from difflib import SequenceMatcher as fuzzyCompare #use this as fuzzyCompare(None, string_one, string_two).ratio()
from tabulate import tabulate
import os
import support
import subprocess
from support import platform_supports_color
from support import bcolors

class error_checking:
     #"PARSED_INSTRUCTION_LIST" : this includes the line the instruction was on, the opcode, the parameters, and the location
     #                            of the instruction in the instruction memory
     PARSED_INSTRUCTION_LIST = []
     #"LABEL_LIST" : this includes the label name, the line label was on, the instruction number it represents, and whether it
     #was used atleast once (by name, or by the address it represents) with the JMP command
     LABEL_LIST = []
     
     @staticmethod
     #"PARSE_TEXT" : receives the entire file as a string, and parses it
     def parse_text(file_string):
          #we convert string to a list of lines
          file_string = file_string.split()
          
          #