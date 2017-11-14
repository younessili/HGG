#!/usr/bin/env python

import sys
import json

#how to make the number of ports independent of the code generator. i.e if a new module is
#introduced with 6 ports how not to define them all over again in the code ??????


#why do we need the print_json function?

#how to move all the checking for the inputs to a different function? tried this but it gives and error in the return type

#TODO add reading from config file for  port types and the data types for inputs outputs 



#############################################################################
def load_json(file):
    with open(file, "r") as fid:
        return json.load(fid)   #load the json file in read mode.
#############################################################################

def print_json(obj):
     print(json.dumps(obj, indent=4))
#############################################################################
#def check_input(file):



#############################################################################
def generate_code(module_name, width, height,port_north,port_south,port_east,port_west):
    mod_name= "module %s(%s,%s,%s,%s);" #module header defiinition
    port_type = "%s = %s ;"
    str_def = "  %s r%d (%s [%d], %s[%d], %s[%d], %s[%d]);"  #module definition
    str_con = "     assign %s[%d] = %s[%d];"   #module connections


   
    ############### prints the module header definition ####################
    print mod_name % (module_name,port_north,port_south,port_east,port_west)
    

    ############## prints the port_type defiinitions#############
    print "  --------------------input ports----------------------"
    print "  input up;"
    print "  input down;"
    print "  input right;"
    print "  input left;"
    print "  --------------------output ports----------------------"
    print "  output my_out;"

    #############prints the port_data_type definitions###########
    print "  --------------------input data types------------------" 
    print "  wire up;"
    print "  wire down;"
    print "  wire right;"
    print "  wire left;"
    print "  --------------------output data types-----------------" 
    print "  reg [3,0] my_out; \n"

    
    ################### prints all the instansiations of the modules given the are ##############
    print "  --------------------module instancces-----------------" 
    total = width * height     #Area of the module
    for n in range(total):
        print str_def % (module_name, n, port_north, n, port_south ,n, port_east, n,port_west, n)
        #prints all the block deffinitions accourding to the json file 
        #1 string for name of block and 4 integers for the block increment
       
    
    ########### prints the connections between the module instances #########
    print "\n  initial begin \n"
    print "    //Connections:\n"
    
    shifts = [width*x for x in range(height-1)] 

    for row_shift in shifts:
        print "    // Connector block (shift = %d):" % row_shift
        for m in range(width):
            n = row_shift + m
            print str_con % (port_north, n, port_south, n+width)

    print "\n  end\n"

    ## module footer ##
    print "endmodule \n"

##############################################################################
def main():

    config_file_path = sys.argv[1]      #takes the input from the user and stores it in a variable.

    #USE: it is Easier to Ask for Forgiveness than for Permission" (in short: EAFP)

    try: 
        config = load_json(config_file_path)
    except IOError:
        print('There was No such file to open!') 
        sys.exit(1)      #try loading the file if there is an IO error stop and print error message

    try:
        port_north =config ["port_names"]["north"]
        port_south = config ["port_names"]["south"]
        port_east = config ["port_names"]["east"]
        port_west = config ["port_names"]["west"]
        block_name = config["module_name"]  #set the block name to the "module name" entry in the json files
        width, height = map(int, config["dimensions"]) #in the config file set width and height to the 1st and 2nd index of the array "dimensions"
    except:
        print('There was an error in the config file!')
        sys.exit(1)    

    generate_code(block_name, width, height,port_north,port_south,port_east,port_west) #feed the "module name" entry in the json file to the generate code function
    

##############################################################################

if __name__ == '__main__':
    main()
