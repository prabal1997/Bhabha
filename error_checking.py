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
     
     @staticmethod
     #all the three functions below return:
     #*a value
     #*a list containing errors
     def give_ram_value(address, system_settings):
          
     @staticmethod
     def give_register_value(register_input, system_settings):
     
     @staticmethod     
     def give_integer(integer_input, system_settings):
          
     #"PARSED_INSTRUCTION_LIST" : this includes the line the instruction was on, the opcode, the parameters, 
     #                            the actual instruction string from the file, and the location
     #                            of the instruction in the instruction memory.

     #"LABEL_LIST" : this includes the label name, the line label was on, the instruction number it represents, and whether it
     #was used atleast once (by name, or by the address it represents) with the JMP command
     
     #POSSIBLE WARNINGS:
     #Accessing RAM beyond the given index
     #Labels that exist, but are never used
     #Integer Overflow
     
     @staticmethod
     #"PARSE_TEXT" : receives the entire file as a string, and parses it
     def parse_text(file_string, source_list, system_settings):
          #error_list
          error_or_warning_list = []
          label_list = []
          instruction_list = []
          
          #we give shorter names to colouring functions
          yellow = bcolors.give_yellow_text
          green = bcolors.give_green_text
          red = bcolors.give_red_text
          blue = bcolors.give_blue_text
          
          #we convert string to a list of lines
          file_string_list = file_string.split("\n")
          for line_no, element in enumerate(file_string_list):
               #we remove unrequired spaces from the instruction
               element = element.strip()
               comment_start = element.find("#")
               
               #we remove the comments from the instruction
               if (comment_start>=0):
                    element = element[0:comment_start]
               
               #at this point, if the string is empty, then we skip over it
               if (len(element)==0):
                    continue
               
               #if the program control reaches here, then we must be receiving a
               #valid or invalid instruction or a label name
               regex_match_row = -1
               regex_match_col = -1
               match_object = "" #NOTE: this WILL NOT be a string eventually; it will become a match object
               
               for index, ins_element in enumerate(source_list):
                    found_match = False
                    
                    for reg_index, reg_element in enumerate(source_list[index][3]):
                         match_object = re.match(reg_element, element)
                         if (match_object):
                              regex_match_row = index
                              regex_match_col = reg_index
                              
                              found_match = True
                              break
                    
                    if (found_match):
                         break
                    
               #now we only have two possibilities: either a match, or not a match
               #in case of 'not a match', we give an error and give the closest possible instruction they can use
               if (regex_match_row<0 or regex_match_col<0):
                    
                    stripped_element = element.strip()
                    identical_instruction_invalid_use = False
                    identical_index = -1
                    for ind, obj in enumerate(source_list):
                         if (source_list[ind][0]==stripped_element):
                              identical_instruction_invalid_use = True
                              identical_index = ind
                              break
                         
                    error_message = red("Error on line ") + yellow(str(line_no+1)) + red(": ")
                    if (not identical_instruction_invalid_use):     
                         error_message += red("invalid instruction ")
                         error_message += yellow("'"+element.strip()+"'") + red(" could not be processed.") + "\n"
                    else:
                         error_message += red("invalid use of instruction ") + green("'"+source_list[identical_index][0]+"'") + red(".") + "\n"
                         error_message += red("The syntax for using ") + green("'"+source_list[identical_index][0]+"'") + red(" is ")
                         error_message += green(("'"+source_list[identical_index][0]+" "+source_list[identical_index][1][0]+"'")) + ((red(" or ")+green("'"+source_list[identical_index][0]+" "+source_list[identical_index][1][1]+"'")) if (len(source_list[identical_index][1])>1) else "") + red(".") + "\n" 
                    
                    if (not identical_instruction_invalid_use):     
                         space_index = element.find(" ")
                         find_similar_string = ""
                         if (space_index>0):
                              find_similar_string = element[0:space_index]
                         else:
                              find_similar_string = element
                         if (len(find_similar_string)==0):
                              find_similar_string=" "
                         
                         highest_ratio = 0
                         highest_index = 0
                         for index, instruction in enumerate(source_list): 
                              if (not source_list[index][0]==""):
                                   new_ratio = fuzzyCompare(None, find_similar_string, source_list[index][0]).ratio()
                                   if (new_ratio>highest_ratio):
                                        highest_ratio = new_ratio
                                        highest_index = index
                             
                         lower_bound = 0.70      
                         if (highest_ratio>=lower_bound):
                              error_message += red("Did you mean to use the ") + green("'"+source_list[highest_index][0]+"'") + red(" instruction?") + "\n"
                              error_message += red("The syntax for using ") + green("'"+source_list[highest_index][0]+"'") + red(" is ")
                              error_message += green(("'"+source_list[highest_index][0]+" "+source_list[highest_index][1][0]+"'")) + ((red(" or ")+green("'"+source_list[highest_index][0]+" "+source_list[highest_index][1][1]+"'")) if (len(source_list[highest_index][1])>1) else "") + red(".") + "\n" 
                    
                    error_or_warning_list.append(["error", error_message])
               else:
                    #if the program control reaches here, then we know that everything was syntactically correct,
                    #but we need to catch logical errors via static analysis
                    
                    #LIST OF ERRORS:
                    '''
                    <nnnn>          : Check for integer overflow, invalid RAM access (Runtime AND Static) (Warning)
                    Ri              : Check for invalid register access (Static) (Error)
                    <label-name>    : Check if the label name exists (Static) (Error) (NOTE: DO NOT do this check if the instruction line is trying to declare a label)
                    
                    Division by 0   : Check for division by 0 in 'DIVi' and 'DIV' (Runtime) (Error)
                    "<label-name>:" : Label not used Warning (this can only be done AFTER the initial staic analysis
                                      to see if none of the instructions contain the label name at all)
                    '''
                    #we check for static errors
                    #<nnnn>   :    integer overflow, invalid RAM access
                    if (not source_list[regex_match_row][0]=="<label-name>:"):
                         pseduo_regex = source_list[regex_match_row][2][regex_match_col]
                         
                         #we count instances of occurance of different type of values
                         address_count = pseduo_regex.count("<nnnn>")
                         number_count = pseduo_regex.count("nnnn") - address_count
                         register_count = pseduo_regex.count("Ri")
                         label_count = pseduo_regex.count("<label-name>")
                         
                    
                    
          return [error_or_warning_list, label_list, instruction_list]