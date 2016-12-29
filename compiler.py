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

#TO-DO:
#complete flags processor
#complete the function that fethces data from the flags processor, and other relevant things
#remove the sample file name from the 'FILE_NAME' filed

class computer:
     #this is the list of all commands
     #NOTE: no labels or comments have been included here; the concept of 'labels' has been hardcoded into the program
     #NOTE: comments are lines that start with the '#' symbol
     #        COMMAND            FORMAT                        PSEDUO-REGEX
     SYNTAX =  [     
                    [["LD"]   , ["<nnnn>, Ri", "Ri, Rj"]     , ["nnnn , Ri", "Ri , Ri"]     ],
                    [["LDi"]  , ["nnnn, Ri", "nnnn, Ri"]     , ["nnnn , Ri", "nnnn , Ri"]   ],
                    [["SD"]   , ["Ri, <nnnn>", "Ri, Rj"]     , ["Ri , nnnn", "Ri , Ri"]     ],
                    [["SDi"]  , ["mmmm, <nnnn>", "mmmm, Ri"] , ["nnnn , nnnn", "nnnn , Ri"] ],
                    [["ADD"]  , ["Ri, Rj, Rk"]               , ["Ri , Ri , Ri"]             ],
                    [["ADDi"] , ["Ri, nnnn, Rj"]             , ["Ri , nnnn , Ri"]           ],
                    [["SUB"]  , ["Ri, Rj, Rk"]               , ["Ri , Ri , Ri"]             ],
                    [["SUBi"] , ["Ri, nnnn, Rj"]             , ["Ri , nnnn , Ri"]           ],
                    [["MUL"]  , ["Ri, Rj, Rk"]               , ["Ri , Ri , Ri"]             ],
                    [["MULi"] , ["Ri, nnnn, Rj"]             , ["Ri , nnnn , Ri"]           ],
                    [["DIV"]  , ["Ri, Rj, Rk"]               , ["Ri , Ri , Ri"]             ],
                    [["JMP"]  , ["<nnnn>"]                   , ["nnnn"]                   ],
                    [["JZ"]   , ["Ri, <nnnn>"]               , ["Ri , nnnn"]               ],
                    [["JNZ"]  , ["Ri, <nnnn>"]               , ["Ri , nnnn"]               ],
                    [["JGZ"]  , ["Ri, <nnnn>"]               , ["Ri , nnnn"]               ],
                    [["JGEZ"] , ["Ri, <nnnn>"]               , ["Ri , nnnn"]               ],
                    [["JLZ"]  , ["Ri, <nnnn>"]               , ["Ri , nnnn"]               ],
                    [["JLEZ"] , ["Ri, <nnnn>"]               , ["Ri , nnnn"]               ]
               ]
     #Program State Registers
     #NOTE: these registers are ADDITIONAL to the registers that the user specified
     PROGRAM_COUNTER = 0 #this keeps track of the line number
     STACK_POINTER = 0 #this keeps track of the stack top
     INSTRUCTION_POINTER = 0 #this keeps track of the address where the current instruction being executed is stored
     
     CONSOLE_VIEW = [] #this includes the text that will be displayed on the screen
     COMMENT_SYMBOL = "#" #this is the symbol that indicates the beginning of a comment
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
     
#||------------------------------------------------||
#PARSING FUNCTIONS
#||------------------------------------------------||
     
#this class receives the appropriate processor configuration, and other settings from
#the flags processor
class receive_data:
     @staticmethod
     def fetch_flags():
          #do something
          
          print("FETCH_FLAGS CALLED")
     
     #this function, based on the processor configuration, sets up a computer with the required settings
     @staticmethod
     def setup_processor():
          for index in range(0, computer.CONSOLE_COUNT):
               computer.CONSOLE_VIEW.append("")
          for index in range(0, computer.REGISTER_COUNT):
               computer.REGISTER_VIEW.append(0)
          for index in range(0, computer.RAM_COUNT):
               computer.MEMORY_VIEW.append(0)
     
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
               register_values[index] = bcolors.give_blue_text(element)
          
          register_table = tabulate([register_values], register_headers, tablefmt="grid")
          
          final_return_output += bcolors.give_yellow_text("PROGRAM STATE") + "\n"
          
          current_instruction = computer.INSTRUCTION
          current_instruction = current_instruction.strip()
          MAXIMUM_INSTRUCTION_WIDTH_ALLOWED = 43
          if (len(current_instruction) > MAXIMUM_INSTRUCTION_WIDTH_ALLOWED):
               current_instruction = current_instruction[0:MAXIMUM_INSTRUCTION_WIDTH_ALLOWED-2]+"..."
               
          final_return_output += tabulate([[bcolors.give_blue_text(computer.LINE_NUMBER), bcolors.give_blue_text(current_instruction)]], [bcolors.give_red_text("Current Line"), bcolors.give_red_text("Instruction")], tablefmt="grid")
          
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
                    COLORED_HEADERS.append(header_color(element))
               
               COLORED_DATA = []
               for index, element in enumerate(data_list):
                    COLORED_DATA.append(data_color(element))
               
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
          
          MAX_ELEMENTS_PER_ROW = 16
          final_return_output += display_state.give_formatted_table(computer.INSTRUCTION_LIST, computer.INSTRUCTION_LIST, bcolors.give_blue_text, bcolors.give_green_text, MAX_ELEMENTS_PER_ROW, True)
          
          return final_return_output
     
     @staticmethod
     def print_screen(is_compact=True):
          register_string = display_state.give_registers()
          memory_string = display_state.give_memory()
          console_string = display_state.give_console()
          stack_string = display_state.give_stack()
          
          output_string = ""
          if (is_compact):
               spaces = "    "
               line_list = console_string.split("\n") + register_string.split("\n") + stack_string.split("\n")
               list_len = len(line_list)
               for index in range(0, list_len):
                    line_list[index] = spaces + line_list[index] + "\t" 
               
               memory_string_row_width = memory_string[len("MEMORY")+2:].find("\n")
               memory_string_len = memory_string.count("\n")
               if (list_len > memory_string_len):
                    line_difference = list_len - memory_string_len
                    memory_string += (" "*(memory_string_row_width+2) + "\n") * line_difference
               
               for element in line_list:
                    memory_string = memory_string.replace("\n", element, 1)
               output_string = memory_string.replace("\t", "\n")
               
          else:
               output_string += register_string + memory_string + console_string + "\n" + stack_string
          
          output_string += display_state.give_instruction_view()
          
          print(output_string)
#||---------------------------------------------||
#START OF PROGRAM
#||---------------------------------------------||
if (not platform_supports_color()):
     bcolors.make_discolored()

receive_data.fetch_flags()
receive_data.setup_processor()