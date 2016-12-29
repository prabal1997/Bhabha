#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re
import math
import os
from tabulate import tabulate

#we use this function to check if our platform supports color output or not
def platform_supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True
    
class bcolors:
     HEADER = "\033[95m"
     OKBLUE = "\033[94m"
     OKGREEN = "\033[92m"
     WARNING = "\033[93m"
     FAIL = "\033[91m"
     ENDC = "\033[0m"
     BOLD = "\033[1m"
     UNDERLINE = "\033[4m"

    #"make_discolored" : This function checks if the platform supports color, and if not, then it changes the color codes to the 'null' character 
     @staticmethod
     def make_discolored():
         HEADER = OKBLUE = OKGREEN = WARNING = FAIL = ENDC = BOLD = UNDERLINE = ""
     
     #this converts the input text to yellow color
     @staticmethod
     def give_yellow_text(input_string):
          return bcolors.WARNING + str(input_string) + bcolors.ENDC
          
     #this converts the input text to red color
     @staticmethod
     def give_red_text(input_string):
          return bcolors.FAIL + str(input_string) + bcolors.ENDC
          
     #this converts the input text to green color
     @staticmethod
     def give_green_text(input_string):
          return bcolors.OKGREEN + str(input_string) + bcolors.ENDC
          
     #this converts the input text to blue color
     @staticmethod
     def give_blue_text(input_string):
          return bcolors.OKBLUE + str(input_string) + bcolors.ENDC
          
#"decode_file" : opens a file, reads it, decodes it, and returns the equivalent string
class other_support:
    @staticmethod
    def decode_file(file_name):
        open_file = open(file_name, "r")
        file = open_file.read()
        file = file.split(os.linesep)
        open_file.close()
        
        final_string = ""
        rows = len(file)
        for row_var in range(0, rows):
           line_len = len(file[row_var])
           curr_line = ""
           for col_var in range(0, line_len):
                CEASER_CIPER_OFFSET = 100
                new_character = ord(file[row_var][col_var])-CEASER_CIPER_OFFSET
                number_of_characters = 256
                new_character = new_character % number_of_characters
                curr_line += chr(new_character)
           if (row_var!=rows-1):
               curr_line += "\n"
           final_string += curr_line
        
        return (final_string)
    
    #"code_file" : reads a string, codes it, and saves it into a file
    @staticmethod
    def code_file(string_to_write, file_name):
        string_to_write = string_to_write.split("\n")
        
        final_string = ""
        rows = len(string_to_write)
        for row_var in range(0, rows):
           line_len = len(string_to_write[row_var])
           curr_line = ""
           for col_var in range(0, line_len):
               CEASER_CIPER_OFFSET= 100
               new_character = ord(string_to_write[row_var][col_var])+CEASER_CIPER_OFFSET
               number_of_characters = 256
               new_character = new_character % number_of_characters
               curr_line += str(chr(new_character))
           if (row_var!=rows-1):
               curr_line += "\n"
           final_string += curr_line
        
        open_file = open(file_name, "w")
        open_file.write(final_string)
        open_file.close()
        
        return(final_string)
        
    @staticmethod
    def give_flag_info(flag_list, flag_defs):
        list_of_flags = other_support.decode_file(flag_list)
        list_of_defs = other_support.decode_file(flag_defs)
        
        #making parameter list
        list_of_flags = list_of_flags.split("\n")
        list_length = len(list_of_flags)
        for index in range(0, list_length):
            list_of_flags[index] = bcolors.give_green_text(list_of_flags[index])
        
        #making definition list
        list_of_defs = list_of_defs.replace("<red>", bcolors.FAIL)
        list_of_defs = list_of_defs.replace("<green>", bcolors.OKGREEN)
        list_of_defs = list_of_defs.replace("<blue>", bcolors.OKBLUE)
        list_of_defs = list_of_defs.replace("<yellow>", bcolors.WARNING)
        list_of_defs = list_of_defs.replace("<bold>", bcolors.BOLD)
        list_of_defs = list_of_defs.replace("<end>", bcolors.ENDC)
        list_of_defs = list_of_defs.split("\n<split>\n")
        def_length = len(list_of_defs)
        
        #we merge the lists
        small_int = def_length if (def_length<list_length) else list_length
        
        new_list = []
        for index in range(0, small_int):
            new_element = [list_of_flags[index], list_of_defs[index]]
            new_list.append(new_element)
        
        #making a new table
        final_table = ""
        for element in new_list:
            final_table += tabulate([[element[0]]], tablefmt="grid") + "\n"
            final_table += element[1] + "\n"
        
        return final_table
