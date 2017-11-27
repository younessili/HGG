#!/usr/bin/env python

import sys
import json

#TODO add reading from config file for  port types and the data types for inputs outputs

#############################################################################
def load_json(file):
    with open(file, "r") as json_data:
        return json.load(json_data)   #load the json file in read mode.
#############################################################################
def check_input(config_file_path):
     #USE: it is Easier to Ask for Forgiveness than for Permission" (in short: EAFP)
    try:
        config = load_json(config_file_path)
    except IOError:
        print('There was No such file to open!')
        sys.exit(1)      #try loading the file if there is an IO error stop and print error message
    try:
        block_name = config["module_name"]  #set the block name to the "module name" entry in the json files
        width, height = map(int, config["dimensions"]) #in the config file set width and height to the 1st and 2nd index of the array "dimensions"
        port_names = config["port_names"]
        port_types= config["port_types"]
        interfaces = config ["interfaces"]


        #add line to read the interfaces code from the config file.

        return (port_names, port_types,interfaces, block_name, width, height)
    except:
        print('There was an error in the config file!')
        sys.exit(1)
#############################################################################
def generate_code(module_name, width, height, port_names,port_types,interfaces):

    total = width * height     #Area of the module

    port_names = port_names.values()
    port_type =  port_types.values()    #list comprehension
    # interface = interfaces.items()


    ######################list of segment definitions#############################

    mod_name= "module %s();" #module header defiinition
    input_exp = "input %s;"
    str_def = "  %s r%d (%s);"  #module definition here (%s) is %s [%d], %s[%d], %s[%d], %s[%d]
    str_con = "     assign %s[%d] = %s[%d];"   #module connections

    ############### prints the module header definition ####################

    print mod_name % (module_name) #feed module name to the mod_name string as an argument to fill %s

    ############## prints the port_type defiinitions#############
    print "//  --------------------input ports----------------------"


    print "// %s" % port_names;
    print "// %s" % port_type;
    # print interface;
    print "\n"


    port_type = ", ".join(port_type)
    print  input_exp % (port_type);
       # print input_exp % (port_names[0],port_names[1],port_names[2]);

    print "//  --------------------output ports----------------------"
    print "  output my_out;"

    #############prints the port_data_type definitions###########
    print "//  --------------------input data types------------------"
    print "  wire up;"
    print "  wire data[99:0];" ## TODO
    print "//  --------------------output data types-----------------"
    print "  reg [3:0] my_out; \n"


    ################### prints all the instansiations of the modules given the are ##############
    print "//  --------------------module instancces-----------------"

    def create_port_def(mod_index, port_name, port_width):
        # example call:
        # create_port_def(0, "data", 8)
        # returns:
        # "data[7:0]"
        # "data[15:8]"
        # "data[23:16]"

        start_bit = port_width * mod_index
        end_bit = port_width * (mod_index+1) - 1

        if start_bit == end_bit:
            return "%s [%d]" % (port_name, start_bit)
        else:
            return "%s[%d:%d]" % (port_name, end_bit, start_bit)


    def create_interface_def(mod_index, interface):
        """Return a Verilog port declaration string representing the interface."""

        if interface in interfaces:

            signals = interfaces[interface]["signals"]

            # indexed_keys = ["%s [%d]" % (key, mod_index) for key in keys]  # e.g. ["req[0]", "ack[0]", "data[0]"]
            indexed_keys = []
            for key, val in signals.iteritems():
                indexed_key = create_port_def(mod_index, key, val)
                indexed_keys.append(indexed_key)

            return ", ".join(indexed_keys)

        else:
            return "%s [%d]" % (interface, mod_index)


    for n in range(total):

        port_parts = [create_interface_def(n, x) for x in port_names]
        # port_parts = ["%s [%d]" % (x, n) for x in port_names] # "up [0]", "down[0]", "right[0]"
        port_def = ", ".join(port_parts)


        print str_def % (module_name, n, port_def)
        #prints all the block deffinitions accourding to the json file
        #1 string for name of block and 4 integers for the block increment


    ########### prints the connections (Assignments) between the module instances #########


    print " \n //north to south"
    port_north = port_names [2]
    port_south = port_names [3]

    shifts = [width*x for x in range(height-1)]

    for row_shift in shifts:
        print "\n    // Connector block (shift = %d):" % row_shift
        for m in range(width):
            n = row_shift + m
            print str_con % (port_north, n, port_south, n+width)

#####################################################################################
    print " \n //east to west"

    port_west = port_names [0]
    port_east = port_names [1]

    column = [width*x for x in range(height)]

    for row_shift in column:
        print "\n    // Connector block (shift = %d):" % row_shift
        for m in range(width-1):
            n = row_shift + m
            print str_con % (port_west, n, port_east, n+1)
#####################################################################################


    ## module footer ##
    print "endmodule \n"



##############################################################################
def main():

    config_file_path = sys.argv[1]      #takes the input from the user and stores it in a variable.
    port_names, port_types, interfaces,block_name, width, height = check_input(config_file_path)
    generate_code(block_name, width, height, port_names, port_types,interfaces) #feed the "module name" entry in the json file to the generate code function

##############################################################################

if __name__ == '__main__':
    main()
