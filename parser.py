#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re
import math

#we define general properties and settings of the project in this section
     #this class takes care of general properties like names, extensons etc.
class properties:
     PROJECT_NAME = "Bhabha"
     FILE_EXTENSION=".asm"
     #NOTE: this is to be preceded by the name of the file that is being compiled
     FILE_WRITE_CONSOLE_EXTENSION="console_view.txt"

     #this class take manages how the input is parsed
#class syntax:
     

     #store list of required parameters
class data_type:
     #the INT, STRING, and BOOL parameters are expected to be received as "-parameter_name=data"
     INT = 0
     STRING = 1
     BOOL = 2
     #the ONLY_INFO parameters are expected to be received as "-parameter_name"
     ONLY_INFO = 3

     #each parameter has name, a data-type it expects, a given value OR default value, a minimum value, and a maximum value
     #"maxErrors" : this asks the user how many errors they want to see before the compilation terminates
     #"maxWarnings" : this asks the user how many warnings do they want to see before the compilation terminates
     #"showWarnings" : this asks the user if they want to see warnings
     #"displayConsole" : this asks the user if they want to see the registers, the ram, and the output when the program runs
     #"writeConsole" : writes the output of every screen to a text file
     #"executionSpeed" : asks the user the speed at which the instructions should be executed
     #"help" : displays user the list of commands required to properly use the compiler
     #"version" : displays the version of compiler to the user
global_parameter_list =  [   
                              ["maxErrors", data_type.INT, float('inf'), 1, float('inf')],
                              ["maxWarnings", data_type.INT, float('inf'), 1, float('inf')],
                              ["showWarnings", data_type.BOOL, True, True, False],
                              ["displayConsole", data_type.BOOL, True, True, False],
                              ["writeConsole", data_type.BOOL, True, True, False],
                              ["executionSpeed", data_type.INT, 1, 1, float('inf')],
                              ["version", data_type.ONLY_INFO, None, None, None],
                              ["help", data_type.ONLY_INFO, None, None, None]
                         ]

#defining an error and warning streams
     #this allows us to colour our outputs
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    #this allows us to throw errors, while keeping track of their count
def eprint(is_error, *args, **kwargs):
     #we check what kind of message we are supposed to print, and we identify relevant characteristics
     counter = eprint.warning_counter
     message_type = ["Warning", "warnings"]
     max_value = global_parameter_list[1][2]
     display_message = global_parameter_list[2][2]
     
     if (is_error):
          counter = eprint.error_counter
          message_type = ["Error", "errors"]
          max_value = global_parameter_list[0][2]
          display_message = True
          
     if (display_message):
          if (counter <= max_value):
               print(*args, file=sys.stderr, **kwargs)
          if (counter == max_value):
               print(bcolors.WARNING + message_type[0] + " limit reached. No more " + message_type[1] + " will be printed." + bcolors.ENDC)
               if (is_error):
                    #we quit the compilation when we reach the upper limit of errors
                    print(bcolors.FAIL + "Compilation Terminated." + bcolors.ENDC)
                    quit()
          #these variables keep track of how many times this function was called
          if (counter <= max_value):
               if (is_error):
                    eprint.error_counter += 1
               else:
                    eprint.warning_counter +=1 
eprint.warning_counter = 1
eprint.error_counter = 1

#extract the filename to be compiled
if (len(sys.argv)<2):
     error_message = bcolors.FAIL + "Error: no filename found. Compilation terminated." + bcolors.ENDC
     error_message_extra  = "\nExpected " + bcolors.WARNING + "<file_name-1> <file_name-2> <file_name-3> ... <parameter-1> <parameter-2> <parameter-3> ... " + bcolors.ENDC
     eprint(True, error_message, error_message_extra)

#SEQUENTIAL CODE