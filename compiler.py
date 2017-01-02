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
from error_checking import error_checking
from random import randint
import ctypes
 
#TO-DO:
#complete flags processor
#complete the function that fethces data from the flags processor, and other relevant things
#remove the sample file name from the 'FILE_NAME' filed

class computer:
     #this is the list of all commands
     #NOTE: no labels or comments have been included here; the concept of 'labels' has been hardcoded into the program
     #NOTE: comments are lines that start with the '#' symbol
     #        COMMAND            FORMAT                        PSEUDO-REGEX                    REGEX
     SYNTAX =  [     
                    ["LD"   , ["<nnnn>, Ri", "Ri, Rj"]       , ["<nnnn> , Ri", "Ri , Ri"]        ,[]],
                    ["LDi"  , ["nnnn, Ri"]                   , ["nnnn , Ri"]                     ,[]],
                    ["SD"   , ["Ri, <nnnn>", "Ri, Rj"]       , ["Ri , <nnnn>", "Ri , Ri"]        ,[]],
                    ["SDi"  , ["mmmm, <nnnn>", "mmmm, Ri"]   , ["nnnn , <nnnn>", "nnnn , Ri"]    ,[]],
                    ["ADD"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["SUB"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["MUL"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["DIV"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["JMP"  , ["<label-name>"]               , ["<label-name>"]                  ,[]],
                    ["JZ"   , ["Ri, <label-name>"]           , ["Ri , <label-name>"]             ,[]],
                    ["JNZ"  , ["Ri, <label-name>"]           , ["Ri , <label-name>"]             ,[]],
                    ["MORE" , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["LESS" , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["SAME" , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["AND"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["OR"   , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],
                    ["XOR"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"] , ["Ri , Ri , Ri", "Ri , nnnn , Ri"],[]],                    
                    ["NOT"  , ["Ri, Rj", "nnnn, Ri"]         , ["Ri , Ri", "nnnn , Ri"]          ,[]],                         
                    ["PUSH" , ["Ri", "nnnn"]                 , ["Ri", "nnnn"]                    ,[]],
                    ["POP"  , ["Ri", "<nnnn>"]               , ["Ri", "<nnnn>"]                  ,[]],
                    [""     , ["<label-name>:"]              , ["<label-name>:"]                 ,[]]
               ]
     #Program State Registers
     #NOTE: these registers are ADDITIONAL to the registers that the user specified
     PROGRAM_COUNTER = 0 #this keeps track of the line number
     STACK_POINTER = 0 #this keeps track of the stack top
     INSTRUCTION_POINTER = 0 #this keeps track of the address where the current instruction being executed is stored
     
     CONSOLE_VIEW = [] #this includes the text that will be displayed on the screen
     REGISTER_VIEW = [] #this includes the contents of all registers
     MEMORY_VIEW = [] #this includes the stack, and the instructions
     DATA_MEMORY = [] #this separate from the RAM; special area for storing instructions
     LABEL_LIST = [] #this includes names of all labels, and line numbers they occur on
     INSTRUCTION_LIST = [] #this contains the list of instructions as it would look like in the memory
     
     #Processor configurations; these are just the default values that will be changed
     #based on the data provided by the flags processor
     REGISTER_COUNT                = 8
     RAM_COUNT                     = 256
     MAX_STACK_COUNT               = 8
     CURRENT_STACK_SIZE            = 0      
     CONSOLE_COUNT                 = 8
     PROCESSOR_SPEED               = 1
     
     #Code Properties
     FILE_NAME = "sample.asm" #this is the name of the file that is to be compiled
     LINE_NUMBER = 0
     INSTRUCTION = ""
     LAST_ERROR = "" #this string holds the last warning/error that occured during the program execution (stack overflow, division by zero, found a negative number etc...)
     
     #OTHER FLAGS
     MAX_ERRORS = float('inf')
     MAX_WARNINGS = float('inf')
     SHOW_WARNINGS = True
     DISPLAY_CONSOLE_ONLY = False
     WRITE_CONSOLE = False
     COLOR_SUPPORTED = False
     HIGH_BIT_MODE = True
     
#||------------------------------------------------||
#PARSING FUNCTIONS
#||------------------------------------------------||
     
#this class receives the appropriate processor configuration, and other settings from
#the flags processor
class receive_data:
     @staticmethod
     def fetch_flags():
          #convert from string to appropriate data-types, storing data in appropriate fields
          computer.MAX_ERRORS = float('inf') if (sys.argv[1+0]=="inf") else int(sys.argv[1+0])
          computer.MAX_WARNINGS = float('inf') if (sys.argv[1+1]=="inf") else int(sys.argv[1+1])
          computer.SHOW_WARNINGS = True if (sys.argv[1+2]=="True") else False
          computer.DISPLAY_CONSOLE_ONLY = True if (sys.argv[1+3]=="True") else False
          computer.WRITE_CONSOLE = True if (sys.argv[1+4]=="True") else False
          computer.PROCESSOR_SPEED = int(sys.argv[1+5])
          computer.REGISTER_COUNT = int(sys.argv[1+6])
          computer.RAM_COUNT = int(sys.argv[1+7])
          computer.MAX_STACK_COUNT = int(sys.argv[1+8])
          computer.CONSOLE_COUNT = int(sys.argv[1+9])
          computer.COLOR_SUPPORTED = True if (sys.argv[1+10]=="True") else False
          computer.FILE_NAME = sys.argv[1+11]
          computer.HIGH_BIT_MODE = True if (sys.argv[1+12]=="True") else False
          
          display_state.eprint.warning_counter = 1
          display_state.eprint.error_counter = 1
     
     #this function, based on the processor configuration, sets up a computer with the required settings
     @staticmethod
     def setup_processor():
          for index in range(0, computer.CONSOLE_COUNT):
               computer.CONSOLE_VIEW.append("")
          for index in range(0, computer.REGISTER_COUNT):
               computer.REGISTER_VIEW.append(0)
          for index in range(0, computer.RAM_COUNT):
               computer.MEMORY_VIEW.append(0)
          computer.STACK_POINTER = computer.RAM_COUNT-computer.CONSOLE_COUNT-computer.CURRENT_STACK_SIZE
               
     #this function converts the 'pseduo-regex' to actual regex
     @staticmethod
     def make_regex():
          label_placeholder = "<label-name>"
          int_placeholder = "nnnn"
          address_placeholder = "<nnnn>"
          register_placeholder = "Ri"
          space_placeholder = " "
          
          label_regex = "([a-zA-Z_]+[0-9a-zA-Z_-]*)"
          int_regex = "([+-]{0,1}(?:0b[0-1]+|0x[0-9A-Fa-f]+|[0-9]+))"
          register_regex = "([rR]{1,1}[0-9]+)"
          space_regex = "\s*"
          beginning_regex = ""
          ending_regex = "\s*(?:\#.*|\s*)$"
          
          command_count = len(computer.SYNTAX)
          for row in range(0, command_count):
               
               beginning_regex = "^\s*" + computer.SYNTAX[row][0]+"\s" + ( "*" if (computer.SYNTAX[row][0] == "") else "+")
               for col in range(0, len(computer.SYNTAX[row][2])):
                    semi_regex = computer.SYNTAX[row][2][col]
                    
                    semi_regex = semi_regex.replace(":", "\s*\:")                    
                    semi_regex = semi_regex.replace(label_placeholder, label_regex)
                    semi_regex = semi_regex.replace(address_placeholder, int_regex)
                    semi_regex = semi_regex.replace(int_placeholder, int_regex)
                    semi_regex = semi_regex.replace(register_placeholder, register_regex)
                    semi_regex = semi_regex.replace(space_placeholder, "\s*")
                    
                    semi_regex = beginning_regex+semi_regex+ending_regex
                    computer.SYNTAX[row][3].append(semi_regex)
          
     
#this class is responsible for displaying the state of the program on the screen     
class display_state:
     #this returns the dimensions of the computer screen
     @staticmethod
     def give_dimensions():
          rows, columns = subprocess.check_output(['stty', 'size']).split()
          return [rows, columns]
          
     #this function prints the data stored in all registers that the program has
     @staticmethod
     def give_registers():
          final_return_output = ""
          #printing processor state registers
          register_headers = ["PC", "SP"]
          for index, element in enumerate(register_headers):
               register_headers[index] = bcolors.give_red_text(element)
          
          register_values = [computer.PROGRAM_COUNTER, computer.STACK_POINTER]
          for index, element in enumerate(register_values):
               register_values[index] = bcolors.give_blue_text(str(element))
          
          register_table = tabulate([register_values], register_headers, tablefmt="grid")
          
          final_return_output += bcolors.give_yellow_text("PROGRAM STATE") + "\n"
          
          current_instruction = computer.INSTRUCTION
          current_instruction = current_instruction.strip()
          MAXIMUM_INSTRUCTION_WIDTH_ALLOWED = 43
          if (len(current_instruction) > MAXIMUM_INSTRUCTION_WIDTH_ALLOWED):
               current_instruction = current_instruction[0:MAXIMUM_INSTRUCTION_WIDTH_ALLOWED-2]+"..."
               
          final_return_output += tabulate([[bcolors.give_blue_text(str(computer.LINE_NUMBER)), bcolors.give_blue_text(current_instruction)]], [bcolors.give_red_text("Current Line"), bcolors.give_red_text("Instruction")], tablefmt="grid")
          
          final_return_output += "\n\n" + bcolors.give_yellow_text("ERROR CONSOLE") + "\n"
          final_return_output += tabulate([[bcolors.give_blue_text(computer.LAST_ERROR)]], [bcolors.give_red_text("Error Message")], tablefmt="grid")
          final_return_output += "\n\n" + bcolors.give_yellow_text("REGISTERS")
          
          acronym_list = [
                         bcolors.give_red_text("PC") + " : " + bcolors.BOLD+"PROGRAM COUNTER"+bcolors.ENDC
                         ,bcolors.give_red_text("SP") + " : " + bcolors.BOLD+"STACK POINTER"+bcolors.ENDC
                         ]
          
          register_table = [register_table[0:register_table.find("\n")+1], register_table[register_table.find("\n")+1:]]
          for index in range(0, len(acronym_list)):
               spaces = "     "
               register_table[1] = register_table[1].replace("\n", spaces + acronym_list[index]+"\t", 1)
          register_table = register_table[0] + register_table[1]          
          register_table = register_table.replace("\t", "\n")
          
          final_return_output += "\n" + register_table + "\n"
          
          #printing numbered registers
          register_headers = []
          for index in range(0, computer.REGISTER_COUNT):
               reg_name = "R"+str(index+1)
               register_headers.append(reg_name)
          
          MAX_ELEMENTS_PER_ROW = 8
          output = display_state.give_formatted_table(computer.REGISTER_VIEW, register_headers, bcolors.give_blue_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW)
          final_return_output += output
          
          return final_return_output
     
     @staticmethod
     def give_formatted_table(data_list, header_list, data_color, header_color, max_elements_per_row, is_compact=False):
          if (len(header_list)>0):
               #NOTE: 'header_color', and 'data_color' are functions that colored version of the text they receive
               
               #length of the received lists
               width = len(header_list)
               
               #coloring the received lists
               COLORED_HEADERS = []
               for index, element in enumerate(header_list):
                    converter = []
                    if (bcolors.is_string(element)):
                         converter = element
                    else:
                         converter = str(element)
                         
                    COLORED_HEADERS.append(header_color(converter))
               
               COLORED_DATA = []
               for index, element in enumerate(data_list):
                    converter = []
                    if(bcolors.is_string(element)):
                         converter = element
                    else:
                         converter = str(element)
                         
                    COLORED_DATA.append(data_color(converter))
               
               data_width = len(COLORED_DATA)
               if (data_width<width):
                    number_of_extra_elements_required = width-data_width
                    while(number_of_extra_elements_required!=0):
                         COLORED_DATA.append(" ")
                         number_of_extra_elements_required-=1
               
               global_table = []
               compact_table_rows = []
               ceiling_value = width/(1.0*max_elements_per_row)
               if (ceiling_value<0):
                    ceiling_value *= -1
               FLOAT_COMPARISON_THRESHOLD = 0.0001
               if (ceiling_value - int(ceiling_value) > FLOAT_COMPARISON_THRESHOLD):
                    ceiling_value = int(ceiling_value) + 1
               
               counter = 0
               for index in xrange(0, int(max_elements_per_row*ceiling_value), max_elements_per_row):
                    final_index = index+max_elements_per_row
                    if (final_index > width):
                         final_index = width
                    
                    local_table = tabulate([COLORED_DATA[index:final_index]], COLORED_HEADERS[index:final_index], tablefmt="grid")
                    
                    global_table.append(local_table)
                    if (is_compact):
                         compact_table_rows.append(COLORED_DATA[index:final_index])
                    
                    counter+=1         
               
               if(is_compact):
                    output_string = tabulate(compact_table_rows, tablefmt="grid")
                    return output_string
               
               #finding the width of the widest table
               counter -= 1
               max_table_width = global_table[counter].find("\n")+1
               if (counter>0):
                    max_table_width = [max_table_width, global_table[counter-1].find("\n")+1]
                    if (max_table_width[0]>max_table_width[1]):
                         temp = max_table_width[0]
                         max_table_width[0] = max_table_width[1]
                         max_table_width[1] = temp
                         
                    max_table_width = max_table_width[1]
                    
               #changing width of all tables to match the highest width
               final_string = ""
               for index, element in enumerate(global_table):
                    if (index!=counter):
                         curr_width = element.find("\n")+1
                         spaces_count = max_table_width - curr_width
                         
                         global_table[index] = element.replace("\n", "\n"+" "*spaces_count)
                         global_table[index] = " "*spaces_count + global_table[index]
                    
                    final_string += global_table[index]+"\n"
               
               return final_string
          
          return ""
     
     #this function prints the entire ram of the program (this INCLUDES the instructions)
     @staticmethod
     def give_memory():
          header_text = "MEMORY"
          final_return_output = ""
          
          header_list = []
          for index in range(0, computer.RAM_COUNT):
               header_list.append(str(index))
          
          MAX_ELEMENTS_PER_ROW = 16
          final_return_output += display_state.give_formatted_table(computer.MEMORY_VIEW, header_list, bcolors.give_blue_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW, True) + "\n"
          
          table_width = final_return_output.find("\n")
          spacing_required = table_width - len(header_text)
          final_return_output = bcolors.give_yellow_text("\n" + header_text + spacing_required*" " + "\n") + final_return_output
          
          return final_return_output
          
     #this function displays the contents of the console on the screen
     @staticmethod
     def give_console():
          computer.CONSOLE_VIEW = []
          for index in range(computer.RAM_COUNT-computer.CONSOLE_COUNT, computer.RAM_COUNT):
               number_of_ASCII_characters = 256
               char_order = (computer.MEMORY_VIEW[index]%number_of_ASCII_characters)
               actual_char = ""+("" if (char_order==0) else chr(char_order))+""
               actual_char = unicode(actual_char, errors='ignore')
               computer.CONSOLE_VIEW.append(actual_char if computer.MEMORY_VIEW[index]!=0 else "")
          
          final_return_output = ""
          final_return_output += bcolors.give_yellow_text("\nTEXT CONSOLE\n")
          
          header_list = []
          for index in range(computer.RAM_COUNT-computer.CONSOLE_COUNT, computer.RAM_COUNT):
               header_list.append(str(index))
               
          MAX_ELEMENTS_PER_ROW = 8
          final_return_output += display_state.give_formatted_table(computer.CONSOLE_VIEW, header_list, bcolors.give_red_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW)
          
          return final_return_output
          
     @staticmethod
     def give_stack():
          final_return_output = ""
          final_return_output += bcolors.give_yellow_text("STACK") + "\n"
          
          header_list = []
          beginning_range = computer.RAM_COUNT-computer.CONSOLE_COUNT-computer.CURRENT_STACK_SIZE
          ending_range = computer.RAM_COUNT-computer.CONSOLE_COUNT
          for index in range(beginning_range, ending_range):
               header_list.append(str(index))               
          
          MAX_ELEMENTS_PER_ROW = 8
          final_return_output += display_state.give_formatted_table(computer.MEMORY_VIEW[beginning_range:ending_range], header_list, bcolors.give_blue_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW)

          return final_return_output
     
     @staticmethod
     def give_instruction_view():
          final_return_output = ""
          
          INSTRUCTION_LIST = computer.INSTRUCTION_LIST
          print_ellipses = False
          if (len(INSTRUCTION_LIST)>16):
               print_ellipses = True
               INSTRUCTION_LIST = INSTRUCTION_LIST[0:16]
               
          length_of_instructions = len(computer.INSTRUCTION_LIST)
          
          length_of_instructions = 1 if (length_of_instructions==0) else length_of_instructions 
          final_return_output += "\n" + bcolors.give_yellow_text("INSTRUCTION MEMORY (ADDRESS " + str(computer.RAM_COUNT) + "-" + str(computer.RAM_COUNT + length_of_instructions-1) + ")" + "\n")
          
          MAX_ELEMENTS_PER_ROW = 8
          final_return_output += display_state.give_formatted_table(INSTRUCTION_LIST, INSTRUCTION_LIST, bcolors.give_blue_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW, True)
          
          if (print_ellipses):
               final_return_output = final_return_output.strip() + "\n.\n.\n."  
               
          return final_return_output
     
     @staticmethod
     def print_screen(is_compact=True):
          
          console_string = display_state.give_console()
          output_string = ""
          if (not computer.DISPLAY_CONSOLE_ONLY):
               register_string = display_state.give_registers()
               memory_string = display_state.give_memory()
               stack_string = display_state.give_stack()
               
               if (is_compact):
                    spaces = "    "
                    line_list = console_string.split("\n") + register_string.split("\n") + stack_string.split("\n")
                    list_len = len(line_list)
                    for index in range(0, list_len):
                         line_list[index] = spaces + line_list[index] + "\n" 
                    
                    memory_string = memory_string.strip()
                    memory_string_list = memory_string.split("\n")
                    memory_string_len = len(memory_string_list) 
                    
                    if (list_len < memory_string_len):
                         for index in range(0, list_len):
                              memory_string_list[index] = memory_string_list[index] + line_list[index] 
                    else:
                         widest_row = len(memory_string_list[0])
                         #we look for the first instance where the line length is greater than the first line
                         for element in memory_string_list:
                              line_len = len(element)
                              if (line_len>widest_row):
                                   widest_row = line_len
                                   break
                         
                         line_difference = list_len - memory_string_len
                         for index in range(0, line_difference):
                              memory_string_list.append(" "*widest_row)

                         for index in range(0, list_len):
                              memory_string_list[index] = memory_string_list[index] + line_list[index] 
                         
                         for element in memory_string_list:
                              output_string += element
                    
               else:
                    output_string += register_string + memory_string + console_string + "\n" + stack_string
               output_string += display_state.give_instruction_view()
     
          else:
               output_string += "\n" + console_string
          
          print(output_string)
          
     
     @staticmethod
     def update_computer(new_instruction, label_list):
          #ERROR CODES in order of priority (smaller index means higher priority)
          FATAL_DIV_BY_ZERO = 0
          INVALID_ACCESS = 1
          STACK_OVERFLOW = 2
          STACK_UNDERFLOW = 3
          INT_OVERFLOW = 4
          INCORRECT_CHAR = 5
          NO_ERROR = 6
          
          '''
          STACK PUSH AND POP FUNCTIONS
          '''
          def push(input_data):
               #we setup the error message
               error_message = NO_ERROR
               
               #we find the equivalent data of the possible input string
               input_data = give_int(input_data)
               
               #we separate the error and the data
               error_message = input_data[1] if (input_data[1]<error_message) else error_message
               input_data = input_data[0]
               
               #we try to push the data, and if we can't, we give an error message
               if (computer.CURRENT_STACK_SIZE<computer.MAX_STACK_COUNT):
                    computer.CURRENT_STACK_SIZE += 1
                    
                    ram_index_to_modify = computer.RAM_COUNT-computer.CONSOLE_COUNT-computer.CURRENT_STACK_SIZE
                    computer.MEMORY_VIEW[ram_index_to_modify] = input_data
               else:
                    error_message = (STACK_OVERFLOW if (STACK_OVERFLOW<error_message) else error_message)
               
               #we fix the stack pointer
               computer.STACK_POINTER = computer.RAM_COUNT-computer.CONSOLE_COUNT-computer.CURRENT_STACK_SIZE
               
               #we return the value we inteded to add, alongside the highest priority error
               return [input_data, error_message]
          
          def pop():
               #we setup the error message
               error_message = NO_ERROR
               
               #we pop the stack if it has more than a single element, otherwise we only return the only value on the stack
               ram_index = computer.RAM_COUNT-computer.CONSOLE_COUNT-computer.CURRENT_STACK_SIZE
               popped_value = computer.MEMORY_VIEW[ram_index]
               
               if(computer.CURRENT_STACK_SIZE>=1):
                    computer.CURRENT_STACK_SIZE -= 1
               else:
                    error_message = STACK_UNDERFLOW if (STACK_UNDERFLOW<error_message) else error_message
                    
               #we fix the stack pointer
               computer.STACK_POINTER = computer.RAM_COUNT-computer.CONSOLE_COUNT-computer.CURRENT_STACK_SIZE
               
               #we return what we received as the value, along with the highest priority error message
               return [popped_value, error_message]
          
          '''
          >>> import ctypes
          >>> m = 0xFFFFFF00
          >>> ctypes.c_uint32(~m).value
          255L
          '''
          
          '''
          COMPUTER FUNCTIONS
          '''
          def give_int(input_data):
               #we check if the input is a string
               if (not (isinstance(input_data, str) or isinstance(input_data, unicode))):
                    input_data = str(input_data)
               
               #we setup the error code to be sent
               error_message = NO_ERROR
               
               #we separate the sign from the number
               sign = +1
               if(input_data[0]=='-'):
                    sign = -1
               if(not input_data[0].isdigit()):
                    input_data = input_data[1:]
               
               #we convert the number to integer base
               if (input_data[0:2]=="0b"):
                    input_data = input_data[2:]
                    input_data = int(input_data, 2)
               elif (input_data[0:2]=="0x"):
                    input_data = input_data[2:]
                    input_data = int(input_data, 16)
               else:
                    input_data = int(input_data)
               #we combine the sign with the number
               input_data = sign*input_data
               
               #we make the number unsigned
               FLOAT_COMPARISON_THRESHOLD = 0.0001
               unique_numbers = int(math.pow(2, 16 if (computer.HIGH_BIT_MODE) else 8) + FLOAT_COMPARISON_THRESHOLD)
               new_input_data = input_data%unique_numbers
               
               #we return the calculated value, and the highest priority error
               if (input_data!=new_input_data):
                    error_message = INT_OVERFLOW
                    
               return [new_input_data, error_message]
          
          def give_ram_data(ram_cell_index):
          
               #we set up our error message for any possible errors
               error_message = NO_ERROR
               
               #we simplify the received integer
               ram_cell_index = give_int(ram_cell_index)
               
               error_message = ram_cell_index[1] if (ram_cell_index[1]<error_message) else error_message
               ram_cell_index = ram_cell_index[0]
               
               #we see if the new index is within the acceptable ram indices
               new_ram_cell_index = (ram_cell_index%computer.RAM_COUNT)
               if (new_ram_cell_index!=ram_cell_index):
                    error_message = (INVALID_ACCESS if (INVALID_ACCESS<error_message) else error_message)
               
               #we return the value, along with the highest-priority error
               output_int = computer.MEMORY_VIEW[new_ram_cell_index]
               return [output_int, error_message]
               
          def set_ram_data(ram_cell_index, input_data):
               #we set up our error message for any possible errors
               error_message = NO_ERROR
               
               #we simplify the received integer
               ram_cell_index = give_int(ram_cell_index)
               
               error_message = ram_cell_index[1] if (ram_cell_index[1]<error_message) else error_message
               ram_cell_index = ram_cell_index[0]
               
               #we see if the new index is within the acceptable ram indices
               new_ram_cell_index = (ram_cell_index%computer.RAM_COUNT)
               if (new_ram_cell_index!=ram_cell_index):
                    error_message = (INVALID_ACCESS if (INVALID_ACCESS<error_message) else error_message)

               #we convert the received data into a bouded unsigned integer
               input_data = give_int(input_data)
          
               error_message = (input_data[1] if (input_data[1]<error_message) else error_message)
               input_data = input_data[0]
               
               #we set the ram cell to the value we calculated
               computer.MEMORY_VIEW[new_ram_cell_index] = input_data
               
               #we return the value that we set the ram cell equal to, along with the highest-priority error
               return [input_data, error_message]
               
          def give_register_data(register_name):
               register_index = register_name[1:]
               register_index = int(register_index)-1
               
               register_value = computer.REGISTER_VIEW[register_index]
               return [register_value, NO_ERROR]
          
          def set_register_data(register_name, input_int):
               register_index = register_name[1:]
               register_index = int(register_index)-1
               
               input_int = give_int(input_int)
               computer.REGISTER_VIEW[register_index] = input_int[0]
               
               error_message = NO_ERROR
               error_message = input_int[1] if (input_int[1]<error_message) else error_message

               return [input_int[0], error_message]
          
          def set_value(data_type, input_address, input_data):
               #we set up an error message
               error_message = NO_ERROR
               
               #different label styles for different possible data-types
               register_format = "Ri"
               pointer_format = "<nnnn>"

               #we identify the type of data
               output_list = []
               for element in [[register_format, set_register_data], [pointer_format, set_ram_data]]:
                    if(element[0]==data_type):
                         output_list = element[1](input_address, input_data) 
                         break
               
               #separating the error and the value that we set the register/ram cell equal to
               error_message = (output_list[1] if (output_list[1]<error_message) else error_message)
               output_list = output_list[1]
               
               #we return the value that we set the register equals to, and we also return the error with the highest priority
               return [output_list, error_message]
               
          def give_value(data_type, input_data):
               #different label styles for different possible data-types
               register_format = "Ri"
               pointer_format = "<nnnn>"
               integer_format = "nnnn"
               
               output = 0
               error_message = NO_ERROR
               
               #we identify the type of data, and we then find what its value is
               this_output_list = []
               for element in [[register_format, give_register_data], [pointer_format, give_ram_data], [integer_format, give_int]]:
                    if (data_type==element[0]):
                         this_output_list = element[1](input_data)
                         break
               
               #we separate the output and the error code
               output = this_output_list[0]
               error_message = (this_output_list[1] if (this_output_list[1]<error_message) else error_message)
               
               #we return the data
               return [output, error_message]
     
          #we clear the previous error that was shown by our computer
          computer.LAST_ERROR = ""
     
          #we update the program counter
          PROGRAM_COUNTER_INDEX = 5
          new_pc = new_instruction[5]
          computer.PROGRAM_COUNTER = new_pc
          
          #we update the line number and instruction
          LINE_NUMBER_AND_INSTRUCTION_INDEX = [0,2]
          
          new_line_no = new_instruction[LINE_NUMBER_AND_INSTRUCTION_INDEX[0]]
          computer.LINE_NUMBER = new_line_no
          
          new_instruction_name = new_instruction[LINE_NUMBER_AND_INSTRUCTION_INDEX[1]]
          computer.INSTRUCTION = new_instruction_name
          
          #we make a function that compares two integers, and returns the smaller one
          def return_smaller(input_one, input_two):
               return (input_one if (input_one<input_two) else input_two)
          
          line_increment_mode = 1 #1 means normal, 0 means to another specific line number
          new_line_number = 0
          error_message = NO_ERROR
          
          TYPE_LIST_INDEX = 3
          ELEMENT_LIST_INDEX = 4
          
          if (new_instruction[1]=="JMP"):
               line_increment_mode = 0
               
               LABEL_NAME_INDEX_IN_PARAMETER_LIST = 0
               label_name = new_instruction[ELEMENT_LIST_INDEX][LABEL_NAME_INDEX_IN_PARAMETER_LIST]
               
               for element in label_list:
                    if (element[1]==label_name):
                         new_line_number = element[0]
                         break
               
          elif(new_instruction[1]=="JZ"):
               LABEL_NAME_INDEX_IN_PARAMETER_LIST = 1
               label_name = new_instruction[ELEMENT_LIST_INDEX][LABEL_NAME_INDEX_IN_PARAMETER_LIST]
               
               register_value = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               register_value = register_value[0]
               
               if (register_value==0):
                    line_increment_mode = 0
                    for element in label_list:
                         if (element[1]==label_name):
                              new_line_number = element[0]
                              break
                                        
          elif(new_instruction[1]=="JNZ"):
               LABEL_NAME_INDEX_IN_PARAMETER_LIST = 1
               label_name = new_instruction[ELEMENT_LIST_INDEX][LABEL_NAME_INDEX_IN_PARAMETER_LIST]
               
               register_value = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               register_value = register_value[0]
               
               if (register_value!=0):
                    line_increment_mode = 0
                    for element in label_list:
                         if (element[1]==label_name):
                              new_line_number = element[0]
                              break
               
          elif(new_instruction[1]=="LD"):
               if (new_instruction[TYPE_LIST_INDEX][0]=="<nnnn>"):
                    data = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
                    error_message = return_smaller(data[1], error_message)
                    
                    data = set_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1], data[0])               
                    error_message = return_smaller(data[1], error_message)
               else:
                    
                    ram_add_from_reg = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
                    error_message = return_smaller(error_message, ram_add_from_reg[1])
                    
                    data = give_value("<nnnn>", ram_add_from_reg[0])
                    error_message = return_smaller(data[1], error_message)
                    data = data[0]

                    #data = computer.MEMORY_VIEW[give_int(ram_add_from_reg[0])[0]]
                    
                    new_data = set_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1], data)               
                    error_message = return_smaller(new_data[1], error_message)
               
          elif(new_instruction[1]=="SD"):
               if (new_instruction[TYPE_LIST_INDEX][1] == "<nnnn>"):
                    data = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
                    error_message = return_smaller(data[1], error_message)
                    
                    data = set_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1], data[0])               
                    error_message = return_smaller(data[1], error_message)
               else:
                    ram_add_from_reg = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
                    error_message = return_smaller(error_message, ram_add_from_reg[1])
                    
                    data = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
                    error_message = return_smaller(data[1], error_message)
                    
                    data = set_value("<nnnn>", ram_add_from_reg[0], data[0])               
                    error_message = return_smaller(data[1], error_message)
               
          elif(new_instruction[1]=="LDi" or new_instruction[1]=="SDi"):
               data = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data[1], error_message)
               
               data = set_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1], data[0])               
               error_message = return_smaller(data[1], error_message)
               
          elif(new_instruction[1]=="ADD"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = data_one[0] + data_two[0]
               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
               
          elif(new_instruction[1]=="SUB"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = data_one[0] - data_two[0]
               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
               
          elif(new_instruction[1]=="MUL"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = data_one[0] * data_two[0]
               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
               
          elif(new_instruction[1]=="DIV"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = 0
               if (data_two[0]==0):
                    error_message = return_smaller(error_message, FATAL_DIV_BY_ZERO)
                    A_FLOAT_ROUDNING_THRESHOLD = 0.0001
                    sum_var = int(math.pow(2, 16 if (computer.HIGH_BIT_MODE) else 8)+A_FLOAT_ROUDNING_THRESHOLD)-1
               else:
                    sum_var = data_one[0] / data_two[0]                    

               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
               
          elif(new_instruction[1]=="MORE"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = (1 if (data_one[0] > data_two[0]) else 0)
               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
          
          elif(new_instruction[1]=="LESS"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = (1 if (data_one[0] < data_two[0]) else 0)
               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
          
          elif(new_instruction[1]=="SAME"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(data_one[1], error_message)
               
               data_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(data_two[1], error_message)
               
               sum_var = (1 if (data_one[0] == data_two[0]) else 0)
               data_three = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], sum_var)
               error_message = return_smaller(error_message, data_three[1])
               
          elif(new_instruction[1]=="AND"):
               integer_input_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(integer_input_one[1], error_message)
               
               integer_input_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(integer_input_two[1], error_message)
               
               caster = ""
               if (computer.HIGH_BIT_MODE):
                    caster = ctypes.c_uint16
               else:
                    caster = ctypes.c_uint8
                    
               integer_input_one = caster(integer_input_one[0]).value
               integer_input_two = caster(integer_input_two[0]).value
               integer_output = caster(integer_input_one & integer_input_two).value
               
               integer_output_set = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], integer_output)
               error_message = return_smaller(error_message, integer_output_set[1])
               
          elif(new_instruction[1]=="OR"):
               integer_input_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(integer_input_one[1], error_message)
               
               integer_input_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(integer_input_two[1], error_message)
               
               caster = ""
               if (computer.HIGH_BIT_MODE):
                    caster = ctypes.c_uint16
               else:
                    caster = ctypes.c_uint8
                    
               integer_input_one = caster(integer_input_one[0]).value
               integer_input_two = caster(integer_input_two[0]).value
               integer_output = caster(integer_input_one | integer_input_two).value
               
               integer_output_set = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], integer_output)
               error_message = return_smaller(error_message, integer_output_set[1])

          elif(new_instruction[1]=="XOR"):
               integer_input_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(integer_input_one[1], error_message)
               
               integer_input_two = give_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1])
               error_message = return_smaller(integer_input_two[1], error_message)
               
               caster = ""
               if (computer.HIGH_BIT_MODE):
                    caster = ctypes.c_uint16
               else:
                    caster = ctypes.c_uint8
                    
               integer_input_one = caster(integer_input_one[0]).value
               integer_input_two = caster(integer_input_two[0]).value
               integer_output = caster(integer_input_one ^ integer_input_two).value
               
               integer_output_set = set_value(new_instruction[TYPE_LIST_INDEX][2], new_instruction[ELEMENT_LIST_INDEX][2], integer_output)
               error_message = return_smaller(error_message, integer_output_set[1])
               
          elif(new_instruction[1]=="NOT"):
               integer_input_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(integer_input_one[1], error_message)
               
               caster = ""
               if (computer.HIGH_BIT_MODE):
                    caster = ctypes.c_uint16
               else:
                    caster = ctypes.c_uint8
                    
               integer_input_one = caster(integer_input_one[0]).value
               integer_output = caster(~integer_input_one).value
               
               integer_output_set = set_value(new_instruction[TYPE_LIST_INDEX][1], new_instruction[ELEMENT_LIST_INDEX][1], integer_output)
               error_message = return_smaller(error_message, integer_output_set[1])
               
          elif(new_instruction[1]=="PUSH"):
               data_one = give_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0])
               error_message = return_smaller(error_message, data_one[1])
               
               push_data = push(data_one[0])
               error_message = return_smaller(error_message, push_data[1])
               
          elif(new_instruction[1]=="POP"):
               pop_var = pop()
               error_message = return_smaller(error_message, pop_var[1])
               
               stack_data = set_value(new_instruction[TYPE_LIST_INDEX][0], new_instruction[ELEMENT_LIST_INDEX][0], pop_var[0])
               error_message = return_smaller(error_message, stack_data[1])
          
          elif(new_instruction[1]==""):
               var_test = (1+1==2)
               
          #we check if any of the RAM cells that are sources to the text console have an invalid value stored in them
          beginning_index = computer.RAM_COUNT - computer.CONSOLE_COUNT
          ending_index = computer.RAM_COUNT
          NUMBER_OF_ASCII_CHARACTERS = 256
          for console_check_idx in range(beginning_index, ending_index):
               if (computer.MEMORY_VIEW[console_check_idx]>=256):
                    error_message = return_smaller(error_message, INCORRECT_CHAR)
                    break
               
          #we now set the latest error message after sorting errors by level of importance
          if (error_message==FATAL_DIV_BY_ZERO):
               computer.LAST_ERROR = "FATAL ERROR: Division by 0"
          elif(error_message==INVALID_ACCESS):
               computer.LAST_ERROR = "Invalid RAM Access Occurred"
          elif(error_message==STACK_OVERFLOW):
               computer.LAST_ERROR = "Stack Overflow"
          elif(error_message==STACK_UNDERFLOW):
               computer.LAST_ERROR = "Stack Underflow"
          elif(error_message==INT_OVERFLOW):
               computer.LAST_ERROR = "Integer Overflow"
          elif(error_message==INCORRECT_CHAR):
               computer.LAST_ERROR = "Invalid ASCII Value"
          elif(error_message==NO_ERROR):
               computer.LAST_ERROR = ""
     
          return [error_message, [line_increment_mode, new_line_number]]
          
          #in the end, we return the most important error, and the next line number the code should go to
          #which can then be parsed to see if the program needs to stop running
          
     #this allows us to throw errors, while keeping track of their count
     @staticmethod
     def eprint(is_error, terminate_compilation, *args, **kwargs):
          #we check what kind of message we are supposed to print, and we identify relevant characteristics
          counter = display_state.eprint.warning_counter
          message_type = ["Warning", "warnings"]
          max_value = computer.MAX_WARNINGS
          display_message = computer.SHOW_WARNINGS
          
          if (is_error):
               counter = display_state.eprint.error_counter
               message_type = ["Error", "errors"]
               max_value = computer.MAX_ERRORS
               display_message = True
          
          #this line keeps track of the fact that 'maxErrors' or 'maxWarnings' or 'display_message' could be 'None'
          if (max_value is None):
               max_value = float('inf')
          if (display_message is None):
               display_message = True
          
          if (display_message):
               if (counter <= max_value):
                    print(*args, file=sys.stderr, **kwargs)
               if (counter == max_value):
                    print(bcolors.WARNING + message_type[0] + " limit reached. No more " + message_type[1] + " will be printed." + bcolors.ENDC, file=sys.stderr)
                    if (is_error):
                         terminate_compilation = True
               #these variables keep track of how many times this function was called
               if (counter <= max_value):
                    if (is_error):
                         display_state.eprint.error_counter += 1
                    else:
                         display_state.eprint.warning_counter +=1 
                         
          #we terminate compilation after printing an appropriate error message on the screen.          
          if (terminate_compilation):
               print(bcolors.give_red_text("Parsing Terminated."), file=sys.stderr)
               quit()


#||---------------------------------------------||
#START OF PROGRAM
#||---------------------------------------------||
     
#we receive data from the previous script

receive_data.fetch_flags()
discolor = False
if (computer.WRITE_CONSOLE or (not computer.COLOR_SUPPORTED)):
     bcolors.make_discolored()
     discolor = True
     
receive_data.setup_processor()

#we convert pseduo-regex to regex
receive_data.make_regex()

#open the file we are supposed to read data from
read_file = open(computer.FILE_NAME, "r")
read_file_string = read_file.read()
read_file.close()

#error checking here
system_settings = {
                   "MAX_ERRORS" : computer.MAX_ERRORS,
                   "MAX_WARNINGS" : computer.MAX_WARNINGS,
                   "SHOW_WARNINGS" : computer.SHOW_WARNINGS,
                   "DISPLAY_CONSOLE_ONLY" : computer.DISPLAY_CONSOLE_ONLY,
                   "WRITE_CONSOLE" : computer.WRITE_CONSOLE,
                   "COLOR_SUPPORTED" : computer.COLOR_SUPPORTED,
                   "HIGH_BIT_MODE" : computer.HIGH_BIT_MODE,
                   
                   "REGISTER_COUNT" : computer.REGISTER_COUNT,
                   "RAM_COUNT" : computer.RAM_COUNT,
                   "MAX_STACK_COUNT" : computer.MAX_STACK_COUNT,
                   "CURRENT_STACK_SIZE" : computer.CURRENT_STACK_SIZE,
                   "CONSOLE_COUNT" : computer.CONSOLE_COUNT,
                   "PROCESSOR_SPEED" : computer.PROCESSOR_SPEED,
                   "DISCOLOR" : discolor
                  }
                   
all_lists = error_checking.parse_text(read_file_string, computer.SYNTAX, system_settings)
error_or_warning_list = all_lists[0]
error_or_warning_list_len = len(error_or_warning_list)

error_exists_index = -1
for index, element in enumerate(error_or_warning_list):
     if(element[0]=="error"):
          error_exists_index = index

for index in range(0, error_or_warning_list_len):
     if (error_or_warning_list[index][0]!=""):
          is_error = True if (error_or_warning_list[index][0]=="error") else False
          terminate_compilation = False
          if (index == error_exists_index):
               terminate_compilation = True
          display_state.eprint(is_error, terminate_compilation, error_or_warning_list[index][1])

#we now move on assuming no errors were found in the file being compiled
label_list = all_lists[1]
instruction_list = all_lists[2]

#we now go through each instruction, and we find where it is according to the program counter
beginning_cell_no = computer.RAM_COUNT
instruction_count = len(instruction_list)
for index in range(0, instruction_count):
     instruction_list[index].append(beginning_cell_no)
     
     CURR_INSTRUCTION_STRING = instruction_list[index][2]
     beginning_cell_no += (CURR_INSTRUCTION_STRING.count(",")+1)
     
     PARAMETER_LIST_INDEX = 4
     MAX_WIDTH_ALLOWED = 12 #(number of characters)
     complete_string = instruction_list[index][2]
     complete_string = complete_string.replace(":","")
     complete_string = complete_string.replace(","," ")
     complete_string = complete_string.split(" ")
     for element in complete_string:
          ELLIPSES = "..."
          MAX_WIDTH_ALLOWED = 12 #(in characters)
          if (len(element)>MAX_WIDTH_ALLOWED):
               element = element[0:MAX_WIDTH_ALLOWED-len(ELLIPSES)] + ELLIPSES
          if (len(element)>0):
               computer.INSTRUCTION_LIST.append(element)
     
     INSTRUCTION_TYPE_INDEX = 1
     if (instruction_list[index][INSTRUCTION_TYPE_INDEX]!=""):
          beginning_cell_no += 1

index = 0
has_started = False
while(index<instruction_count):
     #we assume that no jump statement will occur
     NEW_INDEX = index+1
     
     #we update our computer state
     line_order_state = display_state.update_computer(instruction_list[index], label_list)
     if (has_started):
          print("\n<split>")
     display_state.print_screen()

     #we see if a fatal error occurred during the last statement
     FATAL_DIV_BY_ZERO_KEY = 0
     if (line_order_state[0]==FATAL_DIV_BY_ZERO_KEY):
          quit()
     
     #we now see if a jump statement occurred
     CHECK_FOR_JUMP = (line_order_state[1][0]==0)
     if (CHECK_FOR_JUMP):
          for order, element in enumerate(instruction_list):
               LINE_NUMBER_HOLDING_INDEX = 1
               LABEL_LINE_NUMBER = line_order_state[1][LINE_NUMBER_HOLDING_INDEX]
               if (element[0]==LABEL_LINE_NUMBER):
                    NEW_INDEX = order  

     #we increment according to what the last instruction indicated
     index = NEW_INDEX
     has_started = True

#TEST:
#each runtime error case
#each command