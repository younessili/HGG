#!/usr/bin/env python

import sys
import json

# TODO:

# 1. print an error message if configuration file does not exist ............DONE!
# 2. print error messages if necessary fields don't exist in config file

#############################################################################
def load_json(file):
    with open(file, "r") as fid:
        return json.load(fid)   #load the json file in read mode.
#############################################################################

def print_json(obj):
     print(json.dumps(obj, indent=4))

#############################################################################
def generate_code(mod_name, width, height):
    # mod_name = "myblock"
    # mod_name = sys.argv[1]
    
    str_def = "%s r%d (north[%d], east[%d], south[%d], west[%d]);"  #module definition
    str_con = "assign north[%d] = south[%d];"   #module connections

    total = width * height     #Area of the module

    for n in range(total):
        print str_def % (mod_name, n, n, n, n, n)
        #prints all the block deffinitions accourding to the json file 
        #1 string for name of block and 4 integers for the block increment

    print "\n//Connections:\n"

    shifts = [width*x for x in range(height-1)] #?????????

    for row_shift in shifts:
        print "// Connector block (shift = %d):" % row_shift
        for m in range(width):
            n = row_shift + m
            print str_con % (n, n+width)
        print "\n"
##############################################################################
def main():

    config_file_path = sys.argv[1]      #takes the input from the user and stores it in a variable.

    #USE it is Easier to Ask for Forgiveness than for Permission" (in short: EAFP)

    try: 
        config = load_json(config_file_path)
    except IOError:
        print('There was No such file to open!') 
        sys.exit(1)      #try loading the file if there is an IO error stop and print error message

    try:
        block_name = config["module_name"]  #set the block name to the "module name" entry in the json files
        width, height = map(int, config["dimensions"]) #in the config file set width and height to the 1st and 2nd index of the array "dimensions"
    except:
        print('There was an error in the config file!')
        sys.exit(1)    

    generate_code(block_name, width, height) #feed the "module name" entry in the json file to the generate code function
    

##############################################################################

if __name__ == '__main__':
    main()
