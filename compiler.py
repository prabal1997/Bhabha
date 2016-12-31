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
     CURRENT_STACK_SIZE            = 1      
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
          computer.STACK_COUNT = int(sys.argv[1+8])
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
          register_headers = ["PC", "IP", "SP"]
          for index, element in enumerate(register_headers):
               register_headers[index] = bcolors.give_red_text(element)
          
          register_values = [computer.PROGRAM_COUNTER, computer.STACK_POINTER, computer.INSTRUCTION_POINTER]
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
                         ,bcolors.give_red_text("IP") + " : " + bcolors.BOLD+"INSTRUCTION POINTER"+bcolors.ENDC
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
          
          length_of_instructions = len(computer.INSTRUCTION_LIST)
          length_of_instructions = 1 if (length_of_instructions==0) else length_of_instructions 
          final_return_output += "\n" + bcolors.give_yellow_text("INSTRUCTION MEMORY (ADDRESS " + str(computer.RAM_COUNT) + "-" + str(computer.RAM_COUNT + length_of_instructions-1) + ")" + "\n")
          
          MAX_ELEMENTS_PER_ROW = 8
          final_return_output += display_state.give_formatted_table(computer.INSTRUCTION_LIST, computer.INSTRUCTION_LIST, bcolors.give_blue_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW, True)
          
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
          print("\n<split>")
          
     
     @staticmethod
     def update_computer(new_instruction):
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
          
          print(new_instruction)
          
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
               print(bcolors.give_red_text("Compilation Terminated."), file=sys.stderr)
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
                   "MAX_STACK_COUNT" : computer.STACK_COUNT,
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
     for element in instruction_list[index][PARAMETER_LIST_INDEX]:
          MAX_WIDTH_ALLOWED = 12 #(in characters)
          if (len(element)>MAX_WIDTH_ALLOWED):
               ELLIPSES = "..."
               element = element[0:MAX_WIDTH_ALLOWED-len(ELLIPSES)] + ELLIPSES
          computer.INSTRUCTION_LIST.append(element)
     
     INSTRUCTION_TYPE_INDEX = 1
     if (instruction_list[index][INSTRUCTION_TYPE_INDEX]!=""):
          beginning_cell_no += 1

#we now start processing each instruction
for index in range(0, instruction_count):     
     display_state.update_computer(instruction_list[index])
     display_state.print_screen()


#END OF PROGRAM
read_file.close()