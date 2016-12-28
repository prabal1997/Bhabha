#!/usr/bin/env python
from __future__ import print_function
import commands
import sys
import random
import re
import math
from difflib import SequenceMatcher as fuzzyCompare
#use this as fuzzyCompare(None, string_one, string_two).ratio()

#we define general properties and settings of the project in this section
     #this class takes care of general properties like names, extensons, processor configuration etc.
class properties:
     
     #"PROJECT_NAME" : this holds the name of the project
     #"FILE_EXTENSION" : this holds the extension of the files that it expects to compile
     #"FILE_WRITE_CONSOLE_EXTENSION" : this holds the partial name of the console output saved into a text file
     PROJECT_NAME                  = "Bhabha"
     FILE_EXTENSION                = ".asm"
     FILE_WRITE_CONSOLE_EXTENSION  = "_console_view.txt"      #NOTE: this is to be preceded by the name of the file that is being compiled
     
     #"REGISTER COUNT" : This holds the count of number of registers that exist in the processor
     #"RAM COUNT" : This holds the count of number of ram cells (each 1 byte) that exist in the processor
     #"STACK_COUNT" : This holds the count of number of stack cells (each 1 byte) that exist in the processor
     #"PROCESSOR_SPEED" : This holds the processor frequency in hertz
     REGISTER_COUNT                = int()
     RAM_COUNT                     = int()
     STACK_COUNT                   = int()
     CONSOLE_COUNT                 = int()
     PROCESSOR_SPEED               = int()
     
     #"check_processor_settings" : This receives process values and checks them to see if they are valid
     
     #this converts the input text to yellow color
     @staticmethod
     def give_yellow_text(input_string):
          return bcolors.WARNING + input_string + bcolors.ENDC
          
     #this converts the input text to red color
     @staticmethod
     def give_red_text(input_string):
          return bcolors.FAIL + input_string + bcolors.ENDC
          
     #this converts the input text to green color
     @staticmethod
     def give_green_text(input_string):
          return bcolors.OKGREEN + input_string + bcolors.ENDC
     
     #"parse_parameters" : this function receives a list of command line arguments, and it processes them to convert user input to stored data
     #                     and returns a list of errors as strings
     #NOTE : this DOES NOT work for a parameter of type data_type.ONLY_INFO 
     @staticmethod
     def parse_parameters(input_list):
          #this receives a data type, and a string, and checks if the string holds that type of data
          def give_data(data_type, received_data):
               regex_string = ""
               if (data_type == data_type.INT):
                    regex_string = "^([-+]{0,1}[1-9]+)$"
               elif (data_type == data_type.STRING):
                    regex_string = "(.+)"
               elif (data_type == data_type.BOOL):
                    regex.string = "^(true|false)$"
                    
               match_object = re.findall(regex_string, received_data, re.DOTALL | re.IGNORECASE)
               if (len(match_object)<0):
                    return None
               else:
                    if (len(match_object[0])<=0):
                        return None
                    else:
                         if (data_type==data_type.INT):
                              return int(match_object[0])
                         elif (data_type==data_type.BOOL):
                              if (match_object[0].lower()=="false"):
                                   return False
                              else:
                                   return True
                         elif (data_type==data_type.STRING):
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
                    formatted_element = element[element.find('-'):]
               
               found_parameter = False
               #we extract the values from the given parameters
               for index in range(0, len(global_parameter_list)):
                    if (global_parameter_list[index][0] is formatted_element):
                         found_parameter = True
                         if (global_parameter_list[index][1]==data_type.ONLY_INFO):
                              global_parameter_list[index][2] = True
                         else:
                              global_parameter_list[index][2] = give_data(global_parameter_list[index][1], element[element.find('='):])
                              
                         #we increment the call counter to indicate how many times this element was encountered, and we record an appropriate error
                         global_parameter_list[6] += 1
                         if (global_prameter_list[6]==2):   #we use '2' so that this error only occurs once
                              error_message = properties.give_red_text("Error: parameter ") + properties.give_yellow_text("'" + global_parameter_list[index] + "'") + properties.give_red_text(" was used multiple times.\n") 
                              error_list.append(error_message)
                              
               if (not found_parameter):
                    error_message = properties.give_red_text("Error: parameter ") + properties.give_yellow_text("'"+element+"'") + properties.give_red_text(" could not be found.")
                    
                    #we look through the entire list of parameters to find the closest match
                    highest_index = 0.00
                    highest_ratio = 0.00
                    lower_bound = 0.75 #if the ratio is below this, the error won't be displayed on the screen
                    for index in range(0, len(global_parameter_list)):
                         new_ratio = fuzzyCompare(None, formatted_element, global_parameter_list[index][0]).ratio()
                         if (new_ratio>highest_ratio):
                              highest_index = index
                              highest_ratio = new_ratio 
                    if (highest_ratio>lower_bound):
                         error_message = error_message + "\n" + properties.give_red_text("Did you mean to use the ") + properties.give_green_text("'" + global_parameter_list[highest_index][0]+"'") + properties.give_red_text(" parameter?")
                    
                    if (element[0]!='-'):
                         error_message = properties.give_red_text("Error: command-line parameter ") + properties.give_yellow_text("'"+element+"'") + properties.give_red_text(" was used with incorrect syntax.")
                    error_message = error_message + "\n" + properties.give_red_text("Proper syntax for command-line parameters is ") + properties.give_green_text('-parameter_name=value') + properties.give_red_text(" or ") + properties.give_green_text("-parameter_name") + properties.give_red_text(".\n")
                    error_list.append(error_message)
                    
          return error_list
               
     @staticmethod
     def check_parameters():
               
          #'check_bounds' : this function checks if a given value is within the proper bounds
          def check_bounds(lower_bound, input_val, upper_bound):
               if (input_val is None):
                    return False
                    
               if (lower_bound <= input_val):
                    return True
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
                              error_message = properties.give_red_text("Error: ") + properties.give_yellow_text(input_parameter_name) + properties.give_red_text(" is out of bounds.")
                              
                              formatted_condition = element[5].replace("<place-holder-name>", input_parameter_name)
                              formatted_condition = formatted_condition.replace("<place-holder-min>", str(element[3]))
                              formatted_condition = formatted_condition.replace("<place-holder-max>", str(element[4]))
                              
                              parameter_value = element[2]
                              if (parameter_value is None):
                                   parameter_vale = "invalid"
                                   
                              error_message_extra = properties.give_red_text("The condition ") + properties.give_yellow_text(formatted_condition) + properties.give_red_text(" was not satisfied because ") + properties.give_yellow_text(input_parameter_name) + properties.give_red_text(" has a value of ") + properties.give_yellow_text(element[2]) + properties.give_red_text(".\n")
                              
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
global_parameter_list =  [   # PARAMETER NAME      ,      DATA TYPE     ,   DEFAULT   , MIN.,     MAX     ,                            CONDITION                                         CALLS 
                              ["maxErrors"         , data_type.INT      , float('inf'), 1   , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["maxWarnings"       , data_type.INT      , float('inf'), 1   , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["showWarnings"      , data_type.BOOL     , True        , True, False       , "<place-holder-name> can only be <place-holder-max> or <place-holder-min>",  0],
                              ["displayConsoleOnly", data_type.BOOL     , True        , True, False       , "<place-holder-name> can only be <place-holder-max> or <place-holder-min>",  0],
                              ["writeConsole"      , data_type.BOOL     , True        , True, False       , "<place-holder-name> can only be <place-holder-max> or <place-holder-min>",  0],
                              ["executionSpeed"    , data_type.INT      , 1           , 1   , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["version"           , data_type.ONLY_INFO, False       , None, None        , None                                                                      ,  0],
                              ["help"              , data_type.ONLY_INFO, False       , None, None        , None                                                                      ,  0],
                              ["registerCount"     , data_type.INT      , 8           , 4   , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["ramSize"           , data_type.INT      , 256         , 128 , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["stackCount"        , data_type.INT      , 8           , 8   , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["consoleSize"       , data_type.INT      , 8           , 0   , float('inf'), "<place-holder-min> <= <place-holder-name> <= <place-holder-max>"         ,  0],
                              ["defaultProcessor"  , data_type.ONLY_INFO, False       , None, None        , None                                                                      ,  0]
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
          
     if (display_message):
          if (counter <= max_value):
               print(*args, file=sys.stderr, **kwargs)
          if (counter == max_value):
               print(bcolors.WARNING + message_type[0] + " limit reached. No more " + message_type[1] + " will be printed." + bcolors.ENDC)
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
          print(bcolors.FAIL + "Compilation Terminated." + bcolors.ENDC)
          quit()
eprint.warning_counter = 1
eprint.error_counter = 1

#extract the filename to be compiled
file_name = ""
if (len(sys.argv)<2):
     error_message = properties.give_red_text("Error: no filename found.")
     error_message  = error_message + properties.give_red_text("\nExpected ") + properties.give_yellow_text("<file_name> <parameter-1> <parameter-2> <parameter-3> ... \n")
     eprint(True, True, error_message)

file_name = sys.argv[1]
if (not ((file_name[::-1])[0:4]==".asm"[::-1])):
     error_message = properties.give_red_text("Error: invalid filename found.")
     error_message = error_message + properties.give_red_text("\nExpected ") + properties.give_green_text(".asm") + properties.give_red_text(" at the end of the input filename ") + properties.give_yellow_text("'"+sys.argv[1]+"'") + properties.give_red_text(".\n")
     eprint(True, True, error_message)

#we parse the command line arguments to find the appropriate errors
errors_occurred = False
command_line_arguments = sys.argv[2:] #we separate the file-name of the compilable file from the rest of the list
errors = []
parse_errors = properties.parse_parameters(command_line_arguments)
bounds_errors = properties.check_parameters()

for element in parse_errors:
     errors.append(element)
for element in bounds_errors:
     errors.append(element)

if (len(errors)>0):
     errors_occurred = True
for index in range(0, len(errors)):
     terminate_program = False
     if (index==len(errors)-1):
          terminate_program = True
     eprint(True, terminate_program, errors[index])