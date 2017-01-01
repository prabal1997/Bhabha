#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re
import math
from difflib import SequenceMatcher as fuzzyCompare #use this as fuzzyCompare(None, string_one, string_two).ratio()
import os
from support import platform_supports_color
from support import bcolors
from support import other_support
from subprocess import Popen, PIPE
from tabulate import tabulate
import os.path
import time

#we define general properties and settings of the project in this section
     #this class takes care of general properties like names, extensons, processor configuration etc.
class properties:
     
     #"PROJECT_NAME" : this holds the name of the project
     #"FILE_EXTENSION" : this holds the extension of the files that it expects to compile
     #"FILE_WRITE_CONSOLE_EXTENSION" : this holds the partial name of the console output saved into a text file
     #"FLAG_INFO_FILE_NAME" : holds the names of the files that hold information about the flag names and flag definitions
     #NOTE: modifying the flags in any external file DOES NOT affect the flags stored internally
     PROJECT_NAME                  = "Bhabha"
     FILE_EXTENSION                = ".asm"
     FILE_WRITE_CONSOLE_EXTENSION  = "_console_view.txt"      #NOTE: this is to be preceded by the name of the file that is being compiled
     FLAG_INFO_FILE_NAME           = ["flag_list","flag_defs"] 
     
     #"REGISTER COUNT" : This holds the count of number of registers that exist in the processor
     #"RAM COUNT" : This holds the count of number of ram cells (each 1 byte) that exist in the processor
     #"STACK_COUNT" : This holds the count of number of stack cells (each 1 byte) that exist in the processor
     #"PROCESSOR_SPEED" : This holds the processor frequency in hertz
     REGISTER_COUNT                = 8
     RAM_COUNT                     = 256
     STACK_COUNT                   = 8
     CONSOLE_COUNT                 = 8
     PROCESSOR_SPEED               = 1
     
     #"help" : this prints the help contents for the user
     @staticmethod
     def help():
          
          print("\n"+bcolors.give_yellow_text("HELP"))
          print("Bhabha is an assembly simulator, and runs a dialect of RISC instructions developed at the University of Waterloo.")
          print("The following table shows the default configuration of the processor Bhabha simulates:\n")
          
          properties.getDefaultSettings(False)
          
          print("\nRefer to the following table to understand the notation used on this page:\n")
          
          #the key to understanding syntax
          print(tabulate([[bcolors.give_green_text("nnnn"),bcolors.give_blue_text(" : an integer (prefix with '0b', '0x', or nothing for binary, hex, or decimal input respectively.")],[bcolors.give_green_text("<nnnn>"),bcolors.give_blue_text(" : an integer interpreted as a RAM address.")], [bcolors.give_green_text("Ri"), bcolors.give_blue_text(" : a register (replace 'i' with the register number).")]], tablefmt="grid"))
          
          print("\nThe following list displays all the parameters(flags) that Bhabha uses alongside their descriptions:\n")
          
          #we read from the file the required data, and 'decode' it using a caesar-cypher-like technique
          final_table = other_support.give_flag_info(properties.FLAG_INFO_FILE_NAME[0], properties.FLAG_INFO_FILE_NAME[1])
          final_table = final_table[0:-1]
          print(final_table)

     #"version" : this prints information about the program to the user
     @staticmethod
     def version():
          headings =  [
                         bcolors.give_green_text("Project Name"),
                         bcolors.give_green_text("Version"),
                         bcolors.give_green_text("Author")
                      ]
                      
          values =    [
                         bcolors.give_blue_text("Bhabha"),
                         bcolors.give_blue_text("1.0.0"),
                         bcolors.give_blue_text("Prabal Gupta")
                      ]
          
          print("\n"+bcolors.give_yellow_text("VERSION INFORMATION"))            
          print(tabulate([values], headings, tablefmt="grid"))
          
     #"getDefaultSettings" : this prints information abour the default values of the processor
     @staticmethod
     def getDefaultSettings(printHeader=True):
          
          headings =  [
                         bcolors.give_green_text("RAM Size"),
                         bcolors.give_green_text("Registers"),
                         bcolors.give_green_text("Stack Size"),
                         bcolors.give_green_text("Console Size"),
                         bcolors.give_green_text("Processor Frequency"),
                         bcolors.give_green_text("Memory Cell/Register Size")
                      ]
                      
          values =    [
                         bcolors.give_blue_text(str(properties.RAM_COUNT) + " bytes"),
                         bcolors.give_blue_text(str(properties.REGISTER_COUNT) + " bytes"),
                         bcolors.give_blue_text(str(properties.STACK_COUNT) + " bytes"),
                         bcolors.give_blue_text(str(properties.CONSOLE_COUNT) + " characters"),
                         bcolors.give_blue_text(str(properties.PROCESSOR_SPEED) + " Hertz"),
                         bcolors.give_blue_text("16 Bytes")
                      ]
          if (printHeader):
               print("\n"+bcolors.give_yellow_text("DEFAULT PROCESSOR CONFIGURATION"))            
          print(tabulate([values], headings, tablefmt="grid"))
          
          
     #"check_processor_settings" : This receives process values and checks them to see if they are valid
     @staticmethod
     def check_processor_settings():
          red = bcolors.give_red_text
          blue = bcolors.give_blue_text
          green = bcolors.give_green_text
          yellow = bcolors.give_yellow_text
          
          RATIO_OF_RAM_TO_MAX_STACK = 0.25
          error_list = []
          for index in [10, 11]:
               if (global_parameter_list[index][2]>global_parameter_list[9][2]*RATIO_OF_RAM_TO_MAX_STACK):
                    message_condition = green("\""+str(global_parameter_list[index][3]) + " <= ") + green("'"+global_parameter_list[index][0] + "'") + green(" <= 0.25 "+ u"\u00D7" +" " + "'"+global_parameter_list[9][0]+"'\"") 
                    error_message = red("Error: ") + yellow("'"+global_parameter_list[index][0]+"'") + red(" is incorrect.\n")
                    error_message += red("The condition ") + message_condition + red(" was not satisfied because ") + yellow("'"+global_parameter_list[9][0]+"'") + red(" and ") + yellow("'"+global_parameter_list[index][0]+"'" + red(" are ") + yellow(str(global_parameter_list[9][2])) + red(" and ") + yellow(str(global_parameter_list[index][2])) + red(" respectively.")) + "\n"
                    
                    error_list.append(error_message)
               
          return error_list
     #"parse_parameters" : this function receives a list of command line arguments, and it processes them to convert user input to stored data
     #                     and returns a list of errors as strings
     #NOTE : this DOES NOT work for a parameter of type data_type.ONLY_INFO 
     @staticmethod
     def parse_parameters(input_list):
          #this receives a data type, and a string, and checks if the string holds that type of data
          def give_data(input_data_type, received_data):
               regex_string = ""
               if (input_data_type == data_type.INT):
                    regex_string = "^([-+]{0,1}[0-9]+)$"
               elif (input_data_type == data_type.STRING):
                    regex_string = "(.+)"
               elif (input_data_type == data_type.BOOL):
                    regex_string = "^(true|false)$"
                    
               match_object = re.findall(regex_string, received_data, re.DOTALL | re.IGNORECASE)
               if (len(match_object)<=0):
                    return None
               else:
                    if (len(match_object[0])<=0):
                        return None
                    else:
                         if (input_data_type==data_type.INT):
                              return int(match_object[0])
                         elif (input_data_type==data_type.BOOL):
                              if (match_object[0].lower()=="false"):
                                   return False
                              else:
                                   return True
                         elif (input_data_type==data_type.STRING):
                              if (match_object[0]==""):
                                   return None
                              else:
                                   return match_object[0]
               return None
          
          #this list contains all the errors that would be found during flag processing
          error_list = []
          for element in input_list:
               #we divide data into parameters and values
               formatted_element = ""
               if (element.find('=')!=-1):
                    formatted_element = element[element.find('-')+1:element.find('=')]
               else:
                    formatted_element = element[element.find('-')+1:]
               
               found_parameter = False
               #we extract the values from the given parameters
               for index in range(0, len(global_parameter_list)):
                    if (global_parameter_list[index][0] == formatted_element):
                         found_parameter = True
                         if (global_parameter_list[index][1]==data_type.ONLY_INFO):
                              global_parameter_list[index][2] = True
                         else:
                              global_parameter_list[index][2] = give_data(global_parameter_list[index][1], element[element.find('=')+1:])
                              
                         #we increment the call counter to indicate how many times this element was encountered, and we record an appropriate error
                         global_parameter_list[index][6] += 1
                         if (global_parameter_list[index][6]==2):   #we use '2' so that this error only occurs once
                              error_message = bcolors.give_red_text("Error: parameter ") + bcolors.give_yellow_text("'" + global_parameter_list[index][0] + "'") + bcolors.give_red_text(" was used multiple times.\n") 
                              error_list.append(error_message)
                              
               if (not found_parameter):
                    error_message = bcolors.give_red_text("Error: parameter ") + bcolors.give_yellow_text("'"+element+"'") + bcolors.give_red_text(" could not be found.")
                    
                    #we look through the entire list of parameters to find the closest match
                    highest_index = 0.00
                    highest_ratio = 0.00
                    lower_bound = 0.70 #if the ratio is below this, the error won't be displayed on the screen
                    for index in range(0, len(global_parameter_list)):
                         new_ratio = fuzzyCompare(None, formatted_element, global_parameter_list[index][0]).ratio()
                         if (new_ratio>=highest_ratio):
                              highest_index = index
                              highest_ratio = new_ratio 
                              
                    if (element[0]!='-'):
                         error_message = bcolors.give_red_text("Error: command-line parameter ") + bcolors.give_yellow_text("'"+element+"'") + bcolors.give_red_text(" was used with incorrect syntax.")
                    
                    found_fuzzy_match = False
                    if (highest_ratio>lower_bound):
                         error_message = error_message + "\n" + bcolors.give_red_text("Did you mean to use the ") + bcolors.give_green_text("'" + global_parameter_list[highest_index][0]+"'") + bcolors.give_red_text(" parameter?")
                         found_fuzzy_match = True
                    
                    error_message = error_message + "\n" + bcolors.give_red_text("Proper syntax for") + bcolors.give_red_text(" this " if (found_fuzzy_match) else " every ") + bcolors.give_red_text("command-line parameter is ")
                    if (found_fuzzy_match):
                         if (global_parameter_list[highest_index][1]==data_type.ONLY_INFO):
                              error_message = error_message + bcolors.give_green_text("-parameter_name")
                         else:
                              error_message = error_message + bcolors.give_green_text('-parameter_name=value')
                    else:
                         error_message = error_message + bcolors.give_green_text('-parameter_name=value') + bcolors.give_red_text(" or ") + bcolors.give_green_text("-parameter_name")
                    error_list.append(error_message + bcolors.give_red_text(".\n"))
                    
          return error_list
               
     @staticmethod
     def check_parameters():
               
          #'check_bounds' : this function checks if a given value is within the proper bounds
          def check_bounds(lower_bound, input_val, upper_bound):
               if (input_val is None):
                    return False
                    
               if (lower_bound > input_val):
                    return False
               if (input_val==float('inf')):
                    if (upper_bound==float('inf')):
                         return True
               else:
                    if (upper_bound>=input_val):
                         return True
               
               return False
          
          #this reads through the parameter list, and checks if the properties are within the required bound
          def give_appropriate_errors(argument_list):
               error_list = []
               for element in argument_list:
                    if (element[1]!=data_type.ONLY_INFO):
                         if (not check_bounds(element[3], element[2], element[4])):
                              input_parameter_name = "'" + element[0] + "'"
                              error_message = bcolors.give_red_text("Error: ") + bcolors.give_yellow_text(input_parameter_name) + bcolors.give_red_text(" is incorrect.")
                              
                              formatted_condition = element[5].replace("<place-holder-name>", input_parameter_name)
                              lower_bound_string = str(element[3])
                              lower_bound_string = lower_bound_string.replace("inf", 	u"\u221E")
                              formatted_condition = formatted_condition.replace("<place-holder-min>", lower_bound_string)
                              
                              upper_bound_string = str(element[4])
                              upper_bound_string = upper_bound_string.replace("inf", 	u"\u221E")
                              formatted_condition = formatted_condition.replace("<place-holder-max>", upper_bound_string)
                              
                              parameter_value = element[2]
                              if (parameter_value is None):
                                   parameter_value = "invalid"
                              
                              if (not bcolors.is_string(parameter_value)):
                                   parameter_value = str(parameter_value)
                                   
                              error_message_extra = bcolors.give_red_text("The condition ") + bcolors.give_green_text(formatted_condition) + bcolors.give_red_text(" was not satisfied because ") + bcolors.give_yellow_text(input_parameter_name) + bcolors.give_red_text(" has a value that is ") + bcolors.give_yellow_text(parameter_value) + bcolors.give_red_text(".\n")
                              error_message = error_message + "\n" + error_message_extra
                              
                              error_list.append(error_message)
                              
               return error_list
               
          return give_appropriate_errors(global_parameter_list)
                         
    
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
     #"displayConsoleOnly" : this asks the user if they want to see the registers, the ram, and the output or only the output when the program runs
     #"writeConsole" : writes the output of every screen to a text file
     #"executionSpeed" : asks the user the speed at which the instructions should be executed
     #"help" : displays user the list of commands required to properly use the compiler
     #"version" : displays the version of compiler to the user
     #"defaultProcessor" : displays on screen the default configuration of the processor
     
     #NOTE: it is NOT possible to add another instruction to this list
global_parameter_list =  [   # PARAMETER NAME      ,      DATA TYPE     ,            VALUES            , MIN.,     MAX     ,                            CONDITION                                         CALLS     DEFAULT 
                              ["maxErrors"         , data_type.INT      , float('inf')               , 1    , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    float('inf')],
                              ["maxWarnings"       , data_type.INT      , float('inf')               , 1    , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    float('inf')],
                              ["showWarnings"      , data_type.BOOL     , True                       , False, True        , "'<place-holder-name> can only be <place-holder-max> or <place-holder-min>'" ,  0,    True],
                              ["displayConsoleOnly", data_type.BOOL     , False                      , False, True        , "'<place-holder-name> can only be <place-holder-max> or <place-holder-min>'" ,  0,    False],
                              ["writeConsole"      , data_type.BOOL     , False                      , False, True        , "'<place-holder-name> can only be <place-holder-max> or <place-holder-min>'" ,  0,    False],
                              ["executionSpeed"    , data_type.INT      , properties.PROCESSOR_SPEED , 0    , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    properties.PROCESSOR_SPEED],
                              ["version"           , data_type.ONLY_INFO, False                      , None , None        , None                                                                         ,  0,    False],
                              ["help"              , data_type.ONLY_INFO, False                      , None , None        , None                                                                         ,  0,    False],
                              ["registerCount"     , data_type.INT      , properties.REGISTER_COUNT  , 4    , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    properties.REGISTER_COUNT],
                              ["ramSize"           , data_type.INT      , properties.RAM_COUNT       , 128  , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    properties.RAM_COUNT],
                              ["stackCount"        , data_type.INT      , properties.STACK_COUNT     , 8    , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    properties.STACK_COUNT],
                              ["consoleSize"       , data_type.INT      , properties.CONSOLE_COUNT   , 1    , float('inf'), "'<place-holder-min> <= <place-holder-name> <= <place-holder-max>'"          ,  0,    properties.CONSOLE_COUNT],
                              ["defaultProcessor"  , data_type.ONLY_INFO, False , None , None        , None                                                                                              ,  0,    False],
                              ["16BitMode"         , data_type.BOOL     , True                       , False, True        , "'<place-holder-name> can only be <place-holder-max> or <place-holder-min>"  ,  0,   False]
                         ]

    #this allows us to throw errors, while keeping track of their count
def eprint(is_error, terminate_compilation, *args, **kwargs):
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
     
     #we check if the values that the WARNING and ERROR flags have in 'global_parameter_list' are valid
     min_max_range_index = 0 if (is_error) else 1
     if (max_value<global_parameter_list[min_max_range_index][3] or max_value>global_parameter_list[min_max_range_index][2]):
          max_value = None
     
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
                    eprint.error_counter += 1
               else:
                    eprint.warning_counter +=1 
                    
     #we terminate compilation after printing an appropriate error message on the screen.          
     if (terminate_compilation):
          print(bcolors.FAIL + "Parsing Terminated." + bcolors.ENDC, file=sys.stderr)
          quit()
eprint.warning_counter = 1
eprint.error_counter = 1

#||---------------------------------------------||
#START OF PROGRAM
#||---------------------------------------------||
#we check if the console supports color output
if (not platform_supports_color()):
     bcolors.make_discolored()

if (len(sys.argv)==2 and sys.argv[1].lower()=="-help"):
     properties.help()
     quit()

#we print an empty line to resolve minor formatting issue
print("")

#extract the filename to be compiled
file_name = ""
if (len(sys.argv)<2):
     error_message = bcolors.give_red_text("Error: no filename found.")
     error_message  = error_message + bcolors.give_red_text("\nExpected ") + bcolors.give_yellow_text("<file_name> <parameter-1> <parameter-2> <parameter-3> ... \n")
     eprint(True, True, error_message)

file_name = sys.argv[1]
if (not ((file_name[::-1])[0:4]==".asm"[::-1])):
     error_message = bcolors.give_red_text("Error: invalid filename detected.")
     error_message = error_message + bcolors.give_red_text("\nExpected ") + bcolors.give_green_text(".asm") + bcolors.give_red_text(" at the end of the input filename ") + bcolors.give_yellow_text("'"+sys.argv[1]+"'") + bcolors.give_red_text(".\n")
     eprint(True, True, error_message)
     
if (len(file_name)<(len(".asm")+1)):
     error_message = bcolors.give_red_text("Error: filename ") + bcolors.give_yellow_text("'"+file_name+"'") + bcolors.give_red_text(" is too short.\n")
     eprint(True, True, error_message)

if (not os.path.isfile(sys.argv[1])):
     error_message = bcolors.give_red_text("Error: filename ") + bcolors.give_yellow_text("'"+sys.argv[1]+"'") + bcolors.give_red_text(" not found.") + "\n"
     eprint(True, True, error_message)

#we parse the command line arguments to find the appropriate errors
errors_occurred = False
command_line_arguments = sys.argv[2:] #we separate the file-name of the compilable file from the rest of the list
errors = []

parse_errors = properties.parse_parameters(command_line_arguments)
bounds_errors = properties.check_parameters()
#we replace any erroneous values with the default value
for index, element in enumerate(global_parameter_list):
     if (element[2] is None):
          global_parameter_list[index][2] = global_parameter_list[index][7]
     
processor_errors =  properties.check_processor_settings()

errors = parse_errors + bounds_errors + processor_errors

if (len(errors)>0):
     errors_occurred = True
     
if (errors_occurred):
     for index, element in enumerate(errors):
          terminate_program = False
          if (index==len(errors)-1):
               terminate_program = True
          eprint(True, terminate_program, element)
          
#we continue while assuming all the flags were correctly processed
     #these are the flags that do not require any values
if (global_parameter_list[12][2]):
     properties.getDefaultSettings()
if (global_parameter_list[6][2]):
     properties.version()
if (global_parameter_list[7][2]):
     properties.help()
     #these are the rest of the flags
     
#start parsing the file according to the given input
input_data = global_parameter_list[0:6] + global_parameter_list[8:12]
for index, element in enumerate(input_data):
     input_data[index] = str(element[2]) if (not bcolors.is_string(element[2])) else element[2]
input_data = [sys.executable, "compiler.py"] + input_data + [str(platform_supports_color()), sys.argv[1], str(global_parameter_list[13][2])]

cproc = Popen(input_data, stdin=PIPE, stdout=PIPE, stderr=PIPE) #sys.executable is the address where the current script is being ran
out, err = cproc.communicate()

#we write the output to file, OR we print it to screen
output_string = err

#we see if 'stderr' has atleast one error
has_errors = False
if (re.match("Error", output_string, re.IGNORECASE)):
     has_errors = True

computer_state_screen_list = out.split("<split>")
computer_state_screen = ""
for element in computer_state_screen_list:
     computer_state_screen += element

WRITE_CONSOLE_INDEX = 4
if (global_parameter_list[WRITE_CONSOLE_INDEX][2]):
     
     #we only add the output screen if there were no errors
     if (not has_errors):
          output_string += computer_state_screen

     #we write the entire output to file, including errors
     write_file_name = sys.argv[1]
     write_file_name = write_file_name[::-1]
     write_file_name = write_file_name.replace(properties.FILE_EXTENSION[::-1], properties.FILE_WRITE_CONSOLE_EXTENSION[::-1], 1)
     write_file_name = write_file_name[::-1]
     open_file = open(write_file_name, "w")
     open_file.write(output_string)
     
     #we end the script here
     quit()
else:
          
     if (has_errors):
          quit()
     else:
          #we include errors in the screen to be displayed first
          print(output_string.strip()+"\n")
          
          #we wait for user key press
          raw_input(bcolors.give_yellow_text("Press any key to continue...\n"))
          
          #we now print the output screen at a pace user wants us to
          SCREEN_DISPLAY_PACE_INDEX = 5
          FREQ = global_parameter_list[SCREEN_DISPLAY_PACE_INDEX][2]
          CYCLE_LEN = (1.0/FREQ) if (FREQ>0) else (-1)
          
          
          #we print the console on the screen at an appropriate pace               
          if (CYCLE_LEN>0):
               for index, element in enumerate(computer_state_screen_list):
                    if ("CONSOLE" in element):
                         print(element)
                         if(index!=len(computer_state_screen_list)-1):
                              time.sleep(CYCLE_LEN)
                              os.system('cls' if os.name=='nt' else 'clear')
                              
          else:
               for index, element in enumerate(computer_state_screen_list):
                    if ("CONSOLE" in element):
                         if(index!=0):
                              raw_input(bcolors.give_yellow_text("Press any key to continue...\n"))
                              os.system('cls' if os.name=='nt' else 'clear')
                         print(element)
               

quit()