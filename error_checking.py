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
import math

class error_checking:
     RAM_COUNT = -1
     HIGH_BIT_MODE = -1
     REGISTER_COUNT = -1
     DISCOLOR = False
     setup_complete = False
     
     @staticmethod
     def give_colored_string(input_string, color):
          ending_tag = bcolors.ENDC
          if (not (isinstance(input_string, str) or isinstance(input_string, unicode))):
               input_string = str(input_string)
          if (error_checking.DISCOLOR):
               ending_tag = ""
               color = ""
          
          return (color + input_string + ending_tag)

     @staticmethod               
     def YELLOW(input_string):
          return error_checking.give_colored_string(input_string, bcolors.WARNING)

     @staticmethod
     def GREEN(input_string):
          return error_checking.give_colored_string(input_string, bcolors.OKGREEN)
     
     @staticmethod
     def RED(input_string):
          return error_checking.give_colored_string(input_string, bcolors.FAIL)
     
     @staticmethod
     def BLUE(input_string):
          return error_checking.give_colored_string(input_string, bcolors.OKBLUE)
     
     @staticmethod
     #receives data from a hash map, and stores the data in local variables instead
     def set_parameters(system_settings):
          if (not error_checking.setup_complete):
               error_checking.DISCOLOR = system_settings["DISCOLOR"]
               error_checking.RAM_COUNT = system_settings["RAM_COUNT"]
               error_checking.HIGH_BIT_MODE = system_settings["HIGH_BIT_MODE"]
               error_checking.REGISTER_COUNT = system_settings["REGISTER_COUNT"]
               error_checking.setup_complete = True
               
     @staticmethod
     #all the three functions below return:
     #*a value
     #*a list containing errors
     
     #Only possible three errors during runtime (in decreasing order of importance)
     #*Division by Zero (FATAL ERROR)
     #*Invalid RAM Access (NON-FATAL ERROR)
     #*Integer Overflow (NON-FATAL ERROR)
     def give_ram_address(address, system_settings, line_number):
          error_checking.set_parameters(system_settings)
          
          #we find any potential errors that might have occurerror_checking.RED
          message_list = []
          output_list = error_checking.give_integer(address, system_settings, line_number)
          message_list = output_list[1]
          
          #we find the 'int' equivalent of the input value
          address_value = output_list[0]
          new_address_value = address_value%error_checking.RAM_COUNT
          
          #we give an appropriate warning if requierror_checking.RED
          error_message = ""
          if (new_address_value!=address_value):
               error_message += error_checking.YELLOW("Warning ") + error_checking.RED("on line ") + error_checking.YELLOW(str(line_number)) + error_checking.RED(": invalid RAM access caused by an index of ") + error_checking.YELLOW(str(address)) + error_checking.RED(" as the range of indices available for use is ") + error_checking.YELLOW("0 - "+str(error_checking.RAM_COUNT-1)) + error_checking.RED(".")+"\n"
          if (len(error_message)>0):
               message_list.append(["warning", error_message])
          
          #we return the address and other relevant messages
          return [new_address_value, message_list]
               
     @staticmethod
     def give_register_index(register_input, system_settings, line_number):
          error_checking.set_parameters(system_settings)
          
          #we make a list of all messages we want to send
          message_list = []
          
          #we separate the index from the register
          reg_index = int(register_input[1:])
          
          error_message = ""
          if (reg_index>error_checking.REGISTER_COUNT or reg_index<=0):
               error_message += error_checking.RED("Error ") + error_checking.RED("on line ") + error_checking.YELLOW(str(line_number)) + error_checking.RED(": invalid register access caused due to ") + error_checking.YELLOW("'"+register_input+"'") + error_checking.RED(" as no such register exists.") + "\n"
          if (len(error_message)>0):
               message_list.append(["error", error_message])
               
          return [reg_index, message_list]
          
     @staticmethod     
     def give_integer(integer_input, system_settings, line_number):
          error_checking.set_parameters(system_settings)
          
          #we make a list to collect all possible errors and warnings
          original_input = integer_input
          message_list = []
          
          #we separate the sign from the number
          sign = 1
          if (integer_input[0]=="-"):
               sign=-1
          if (not integer_input[0].isdigit()):
               integer_input=integer_input[1:]
                    
          if (integer_input.find("0b")>=0):
               integer_input = integer_input[2:]
               integer_input = int(integer_input, 2)
          #hexa-decimal number
          elif (integer_input.find("0x")>=0):
               integer_input = integer_input[2:]
               integer_input = int(integer_input, 16)
          #normal number
          else:
               integer_input = int(integer_input)
          
          #we fix the sign now
          integer_input = sign*integer_input
          
          #we make the number 'unsigned' by taking modulo the 2^bits
          bits = 16 if (error_checking.HIGH_BIT_MODE) else 8
          FLOAT_POINT_ERROR_THRESHOLD = 0.001
          unique_ints = int(math.pow(2, bits) + FLOAT_POINT_ERROR_THRESHOLD)
          new_integer_input = int((integer_input % unique_ints) + FLOAT_POINT_ERROR_THRESHOLD)
          
          #we find errors
          error_message = ""
          if (new_integer_input!=integer_input or sign<0):
               error_message += error_checking.YELLOW("Warning ") + error_checking.RED("on line ") + error_checking.YELLOW(str(line_number)) + error_checking.RED(": integer overflow occurred because a literal of value ") + error_checking.YELLOW(str(original_input)) + error_checking.RED(" is not within the range ") + error_checking.GREEN("0 - " + str(unique_ints-1)) + error_checking.RED(".") + "\n"
          if (len(error_message)>0):
               message_list.append(["warning", error_message])
               
          return [new_integer_input, message_list]
          
     #"PARSED_INSTRUCTION_LIST" : this includes the line the instruction was on, the opcode, the parameters, 
     #                            the actual instruction string from the file, and the location
     #                            of the instruction in the instruction memory.

     #"LABEL_LIST" : this includes the line label was on, the label name, whether it was called atleast once
     
     #POSSIBLE WARNINGS:
     #Accessing RAM beyond the given index
     #Labels that exist, but are never used
     #Integer Overflow
     
     @staticmethod
     #"PARSE_TEXT" : receives the entire file as a string, and parses it
     def parse_text(file_string, source_list, system_settings):
          error_checking.set_parameters(system_settings)
          
          #error_list
          error_or_warning_list = []
          label_list = []
          instruction_list = []
          
          #we convert string to a list of lines
          file_string_list = file_string.split("\n")
          
          #we make a label list here
          for index, element in enumerate(file_string_list):
               LABEL_DEFINITION_REGEX_ROW_INDEX = 21
               label_def_regex = source_list[LABEL_DEFINITION_REGEX_ROW_INDEX][3][0] 
               
               match_object = re.match(label_def_regex, element)
               label_name = ""
               if (match_object):
                    label_name = match_object.group(1+0)
                    
               line_no = index+1
               
               for idx, obj in enumerate(label_list):
                    if (obj[1]==label_name):
                         error_message = error_checking.RED("Error on line ") + error_checking.YELLOW(str(line_no)) + error_checking.RED(": another instance of label ") + error_checking.YELLOW("'"+label_name+"'") + error_checking.RED(" already exists.") + "\n"
                         error_or_warning_list.append(["error" ,error_message])
                         break
               
               if (len(label_name)>0):
                    label_list.append([line_no, label_name, 0])
          
          for line_index, element in enumerate(file_string_list):
               #we remove unrequierror_checking.RED spaces from the instruction
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
                         
                    error_message = error_checking.RED("Error on line ") + error_checking.YELLOW(str(line_index+1)) + error_checking.RED(": ")
                    if (not identical_instruction_invalid_use):     
                         error_message += error_checking.RED("invalid instruction ")
                         error_message += error_checking.YELLOW("'"+element.strip()+"'") + error_checking.RED(" could not be processed.") + "\n"
                    else:
                         error_message += error_checking.RED("invalid use of instruction ") + error_checking.GREEN("'"+source_list[identical_index][0]+"'") + error_checking.RED(".") + "\n"
                         error_message += error_checking.RED("The syntax for using ") + error_checking.GREEN("'"+source_list[identical_index][0]+"'") + error_checking.RED(" is ")
                         error_message += error_checking.GREEN(("'"+source_list[identical_index][0]+" "+source_list[identical_index][1][0]+"'")) + ((error_checking.RED(" or ")+error_checking.GREEN("'"+source_list[identical_index][0]+" "+source_list[identical_index][1][1]+"'")) if (len(source_list[identical_index][1])>1) else "") + error_checking.RED(".") + "\n" 
                    
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
                              error_message += error_checking.RED("Did you mean to use the ") + error_checking.GREEN("'"+source_list[highest_index][0]+"'") + error_checking.RED(" instruction?") + "\n"
                              error_message += error_checking.RED("The syntax for using ") + error_checking.GREEN("'"+source_list[highest_index][0]+"'") + error_checking.RED(" is ")
                              error_message += error_checking.GREEN(("'"+source_list[highest_index][0]+" "+source_list[highest_index][1][0]+"'")) + ((error_checking.RED(" or ")+error_checking.GREEN("'"+source_list[highest_index][0]+" "+source_list[highest_index][1][1]+"'")) if (len(source_list[highest_index][1])>1) else "") + error_checking.RED(".") + "\n" 
                    
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
                    #we use the list of labels for static error checking
                    
                    #we check for static errors
                    #<nnnn>   :    integer overflow, invalid RAM access
                    if (not source_list[regex_match_row][1][0] == "<label-name>:"):
                         register_label = "Ri"
                         address_label = "<nnnn>"
                         number_label = "nnnn"
                         label_label = "<label-name>"
                         
                         pseduo_regex = source_list[regex_match_row][2][regex_match_col]
                         
                         #we count instances of occurance of different type of values
                         address_count = pseduo_regex.count(address_label)
                         number_count = pseduo_regex.count(number_label) - address_count
                         register_count = pseduo_regex.count(register_label)
                         label_count = pseduo_regex.count(label_label)
                         
                         #we make lists of all available inputs
                         address_list = []
                         number_list = []
                         register_list = []
                         local_label_list = []
                         
                         #we now fill-up the lists with their values                
                         element_count = pseduo_regex.count(",")+1
                         
                         type_list = pseduo_regex.replace(",", "").split()
                         element_list = []
                         for idx in range(0, element_count):
                              element_list.append(match_object.group(1+idx))
                              
                         for idx in range(0, len(type_list)):
                              if (type_list[idx]==address_label):
                                   address_list.append(element_list[idx])
                              elif (type_list[idx]==number_label):
                                   number_list.append(element_list[idx])
                              elif (type_list[idx]==register_label):
                                   register_list.append(element_list[idx])
                              elif (type_list[idx]==label_label):
                                   local_label_list.append(element_list[idx])
                         
                         #we count all the calls to labels in our label_list
                         label_list_len = len(label_list)
                         for idx_1 in range(0, label_count):
                              for idx_2 in range(0, label_list_len):
                                   if (local_label_list[idx_1].strip()==label_list[idx_2][1]):
                                        label_list[idx][2] += 1
                                   
                         #We now process all the elements in each list to give errors
                         for idx_1 in range(0, label_count):
                              label_found = False
                              closest_label_index = -1
                              similarity_ratio = 0
                              for idx_2 in range(0, label_list_len):
                                   comparison = fuzzyCompare(None, local_label_list[idx_1], label_list[idx_2][1]).ratio()
                                   if(comparison>similarity_ratio):
                                        closest_label_index = idx_2
                                        similarity_ratio = comparison
                                   if (local_label_list[idx_1] == label_list[idx_2][1]):
                                        label_found = True
                              if (not label_found):
                                   error_message = error_checking.RED("Error on line ") + error_checking.YELLOW(str(line_index+1)) + error_checking.RED(": could not find label ") + error_checking.YELLOW("'"+local_label_list[idx_1]+"'") + error_checking.RED(".") + "\n"
                                   FLOAT_COMPARISON_THRESHOLD = 0.70
                                   if (similarity_ratio>=FLOAT_COMPARISON_THRESHOLD):
                                        error_message += error_checking.RED("Did you mean to use the ") + error_checking.YELLOW("'"+label_list[closest_label_index][1]+"'") + error_checking.RED(" label?") + "\n"
                                   error_or_warning_list.append(["error", error_message])
                                   
                        
                         for element in address_list:
                              output_list = error_checking.give_ram_address(element, system_settings, line_index+1)
                              error_or_warning_list = error_or_warning_list + output_list[1]
                              
                         for element in number_list:
                              output_list = error_checking.give_integer(element, system_settings, line_index+1)
                              error_or_warning_list = error_or_warning_list + output_list[1]
                         
                         for element in register_list:
                              output_list = error_checking.give_register_index(element, system_settings, line_index+1)
                              error_or_warning_list = error_or_warning_list + output_list[1]

                         
          return [error_or_warning_list, label_list, instruction_list]