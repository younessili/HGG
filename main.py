#!/usr/bin/env python

import sys
import json

#############################################################################
def load_json(file):
    """Return the json data by opening the file in read mode  """
    with open(file, "r") as json_data:
        return json.load(json_data)   #load the json file in read mode.
#############################################################################
def generate_code(config_file_path):
    """generate the module instances and assignments"""

    def check_input(config_file_path):
        """Return the main file elements by loadding the congfig file. do this after data validation    """

        try:
             config = load_json(config_file_path)
        except IOError:
            print('There was No such file to open!')
            sys.exit(1)      #try loading the file if there is an IO error stop and print error message

        try:
            module_name = config["module_name"]  #set the block name to the "module name" entry in the json files
            width, height = map(int, config["dimensions"]) #in the config file set width and height to the 1st and 2nd index of the array "dimensions"
            port_names = config["port_names"]
            interfaces = config ["interfaces"]

        except:
            print('There was an error in the config file!')
            sys.exit(1)
        return (port_names,interfaces, module_name, width, height)


    ######################list of segment definitions#############################
    port_names, interfaces,module_name, width, height = check_input(config_file_path)
    area = width * height     #Area of the module
    mod_name= "module %s();" #module header defiinition
    IO_type_exp = " %s [%d:%d] %s ;" #Input and output type expression
    str_def = "  %s r%d (%s);"  #module definition here (%s) is %s [%d], %s[%d], %s[%d], %s[%d]
    str_con = "     assign %s[%d] = %s[%d];"   #module connections#
    port_names_values = port_names.values()


    ################## nested functions for module interface generation###########
    def create_port_def(mod_index, port_name, port_width):
        """return the argument for the module instances based on the number of data lines for each interface. """

        start_bit = port_width * mod_index
        end_bit = (port_width * (mod_index+1) )- 1

       ####need to get the start bit of the first itteration and the last bit of the last itteration for each different interface


        if start_bit == end_bit:
            one_bit_def = "%s [%d]" % (port_name, start_bit)
            return one_bit_def
        else:
            multi_bit_def ="%s[%d:%d]" % (port_name, end_bit, start_bit)
            return multi_bit_def


    def create_interface_def(mod_index, interface):
        """Return a Verilog port declaration string representing the interface."""

        if interface in interfaces:

            signals = interfaces[interface]["signals"]


            indexed_keys = []
            for key, val in signals.iteritems():
                indexed_key = create_port_def(mod_index, key, val)
                indexed_keys.append(indexed_key)
                indexed_keys_exp = ", ".join(indexed_keys)
            return indexed_keys_exp

        else:
            interface_exp = "%s" % (interface)
            return interface_exp


    def create_IO_def (interface):
        """Return the input and output port definitions """

        IO = interfaces[interface]["IO"]
        input_exp = "  input %s;" #input expression
        output_exp = "  output %s;" #output expression

        valid_keys = ["input", "output"]

        valids = [key in valid_keys for key in IO.keys()]

        if not all(valids):
            print("error with config fiel IO declaration look for spelling mistakes")
            sys.exit(1)


    def create_module_assigmnet():
        """create module assignments based on the user prefered assignments."""
        print " \n //north to south connections"

        port_north = port_names ["north"]
        port_south = port_names ["south"]

        shifts = [width*x for x in range(height-1)]
        for row_shift in shifts:
            print "\n    // Connector block (shift = %d):" % row_shift
            for m in range(width):
                n = row_shift + m
                print str_con % (port_north, n, port_south, n+width)

        print " \n //east to west connections"

        port_west = port_names ["west"]
        port_east = port_names ["east"]

        column = [width*x for x in range(height)]

        for row_shift in column:
            print "\n    // Connector block (shift = %d):" % row_shift
            for m in range(width-1):
                n = row_shift + m
                print str_con % (port_west, n, port_east, n+1)


    def create_block_code():
        ###################prints the module header definition ####################

        print mod_name % (module_name) #feed module name to the mod_name string as an argument to fill %s

        ###################prints the IO defiinitions#############

        print "//  --------------------input/output ports----------------------"
        IO_parts = [create_IO_def(x) for x in port_names_values]

        ###################prints the port_data_type definitions###########
        print "//  --------------------input/output data types------------------"

        print "\n"

        ################### prints all the instansiations of the modules given the area ##############
        print "//  --------------------module instancces-----------------"

        for n in range(area):
            port_parts = [create_interface_def(n, x) for x in port_names_values]
            port_def = ", ".join(port_parts)
            print str_def % (module_name, n, port_def)


        ################### prints all the module assignments ##############
        print "\n//  --------------------module assignments-----------------"
        create_module_assigmnet()

        ## module footer ##
        print "\n endmodule "


    create_block_code()
##############################################################################
def main():
    """main function"""
    config_file_path = sys.argv[1]      #takes the input from the user and stores it in a variable.
    generate_code(config_file_path) #feed the "module name" entry in the json file to the generate code function
##############################################################################

if __name__ == '__main__':
    main()
