#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re
import math
from difflib import SequenceMatcher as fuzzyCompare #use this as fuzzyCompare(None, string_one, string_two).ratio()
from texttable import Texttable

#TO-DO:
#complete flags processor
#complete the function that fethces data from the flags processor, and other relevant things

class parser:
     #this is the list of all commands
     #NOTE: no labels have been included here; they concept of 'labels' has been hardcoded into the program
     #        COMMAND            FORMAT                        PSEDUO-REGEX
     SYNTAX =  [     
                    [["LD"]   , ["<nnnn>, Ri", "Ri, Rj"]     , ["nnnn, Ri", "Ri, Ri"]     ],
                    [["LDi"]  , ["nnnn, Ri", "nnnn, Ri"]     , ["nnnn, Ri", "nnnn, Ri"]   ],
                    [["SD"]   , ["Ri, <nnnn>", "Ri, Rj"]     , ["Ri, nnnn", "Ri, Ri"]     ],
                    [["SDi"]  , ["mmmm, <nnnn>", "mmmm, Ri"] , ["nnnn, nnnn", "nnnn, Ri"] ],
                    [["ADD"]  , ["Ri, Rj, Rk"]               , ["Ri, Ri, Ri"]             ],
                    [["ADDi"] , ["Ri, nnnn, Rj"]             , ["Ri, nnnn, Ri"]           ],
                    [["SUB"]  , ["Ri, Rj, Rk"]               , ["Ri, Ri, Ri"]             ],
                    [["SUBi"] , ["Ri, nnnn, Rj"]             , ["Ri, nnnn, Ri"]           ],
                    [["MUL"]  , ["Ri, Rj, Rk"]               , ["Ri, Ri, Ri"]             ],
                    [["MULi"] , ["Ri, nnnn, Rj"]             , ["Ri, nnnn, Ri"]           ],
                    [["DIV"]  , ["Ri, Rj, Rk"]               , ["Ri, Ri, Ri"]             ],
                    [["JMP"]  , ["<nnnn>"]                   , ["nnnn"]                   ],
                    [["JZ"]   , ["Ri, <nnnn>"]               , ["Ri, nnnn"]               ],
                    [["JNZ"]  , ["Ri, <nnnn>"]               , ["Ri, nnnn"]               ],
                    [["JGZ"]  , ["Ri, <nnnn>"]               , ["Ri, nnnn"]               ],
                    [["JGEZ"] , ["Ri, <nnnn>"]               , ["Ri, nnnn"]               ],
                    [["JLZ"]  , ["Ri, <nnnn>"]               , ["Ri, nnnn"]               ],
                    [["JLEZ"] , ["Ri, <nnnn>"]               , ["Ri, nnnn"]               ]
               ]
     #Program State Registers
     #NOTE: these registers are ADDITIONAL to the registers that the user specified
     PROGRAM_COUNTER = 0 #this keeps track of the line number
     STACK_POINTER = 0 #this keeps track of the stack top
     INSTRUCTION_POINTER = 0 #this keeps track of the address where the current instruction being executed is stored
     
     CONSOLE_VIEW = "" #this
     REGISTER_VIEW = [] #this includes the contents of all registers
     MEMORY_VIEW = [] #this includes the stack, and the instructions
     DATA_MEMORY = [] #this separate from the RAM; special area for storing instructions
     LABEL_LIST = [] #this includes names of all labels, and line numbers they occur on
     
     #Processor configurations; these are just the default values that will be changed
     #based on the data provided by the flags processor
     REGISTER_COUNT                = 8
     RAM_COUNT                     = 256
     STACK_COUNT                   = 8
     CONSOLE_COUNT                 = 8
     PROCESSOR_SPEED               = 1

#this class receives the appropriate processor configuration, and other settings from
#the flags processor
class receive_data:
     @staticmethod
     def fetch_flags():
          #do something
          print("TEST")
     
#this class is responsible for displaying the state of the program on the screen     
class display_state:
     #this function prints the data stored in all registers that the program has
     @staticmethod
     def print_registers():
          print("REGISTERS")
          
     #this function prints the entire ram of the program (this INCLUDES the instructions)
     @staticmethod
     def print_memory():
          print("MEMORY")
          
     #this function displays the contents of the console on the screen
     @staticmethod
     def print_console():
          print("CONSOLE")