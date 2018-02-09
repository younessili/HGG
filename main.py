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
            interfaces = config ["interfaces"]
            global_variables = config ["global_variables"]
            assignments = config["assignments"]
        except:
            print('There was an error in the config file!')
            sys.exit(1)
        return (global_variables,interfaces, module_name, width, height,assignments)


    ######################list of segment definitions#############################
    global_variables,interfaces,module_name, width, height,assignments = check_input(config_file_path)
    area = width * height     #Area of the module
    define_exp = "`define %s %d"
    mod_name= "module %s();" #module header defiinition
    IO_type_exp = " %s [%d:%d] %s ;" #Input and output type expression
    input_exp = "  wire %s;" #input expression
    output_exp = "  wire %s;" #output expression
    str_def = "  %s r%d (%s);"  #module definition here (%s) is %s [%d], %s[%d], %s[%d], %s[%d]
    assignment_exp = "%s[%d]<=%s[%d];"
    interface_keys = interfaces.keys()



    def global_variable_def(var):
        for key,val in var.iteritems():
            if key == "MSB":
                return key,val
            else:
                print("No such global variable")
                sys.exit(1)


    def create_IO_def (interface):
        """Return the input and output port definitions """

        IO = interfaces[interface]["IO"]
        val_exp_in = "%s %d"
        val_exp_out = "%s"

        for key, val in IO.iteritems(): #iteritems gets the key and value for each pair of entry in the IO of each interface.
            if key == "input":
                val_exp_in= ", ".join(val)
                return val_exp_in

            elif key == "output":
                val_exp_out= ", ".join(val)
                return val_exp_out


        #return of value out of scope why?


        valid_keys = ["input", "output"]
        valids = [key in valid_keys for key in IO.keys()]
        if not all(valids):
            print("error with config file's IO declaration, look for spelling mistakes")
            sys.exit(1)


    def create_port_def(mod_index, port_name, port_width):
        """return the argument for the module instances based on the number of data lines for each interface. """

        start_bit = port_width * mod_index
        end_bit = (port_width * (mod_index+1) )- 1

       ####need to get the start bit of the first itteration and the last bit of the last itteration for each different interface


        if port_width == 0:
            return port_name
        elif start_bit == end_bit:
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


    def create_module_assigmnet():
        """create module assignments based on the user prefered assignments."""
        print "//neighbours connections \n"

        assignments_keys = " ".join(assignments.keys())
        assignments_values = " ".join(assignments.values())

        for i in range (width-1):
            print "// Connector block (index = %d):" %i
            print assignment_exp % (assignments_values, i, assignments_keys, i+1)



    def create_block_code():

        #########################define global variables########################

        global_var_name,global_var_value= global_variable_def(global_variables)
        print define_exp % (global_var_name,global_var_value)

        ###################prints the module header definition ####################

        IO_values= [create_IO_def(x) for x in interface_keys]
        IO_string= ", ".join(IO_values)
        print mod_name % module_name  # substitute module name

        ###################prints the IO defiinitions#############

        print "//  --------------------input/output ports----------------------"
        print "// %s" % IO_values  #how to remove the u preciding each term so i can extract indicidual ports.

        # get_vec_signals = lambda interface: [item for item in interface["signals"].iteritems() if item[1]>0]

        def get_vec_signals(interface):
            """Given an inteface dictionary, return a list of (signal, bits)
            where bits>0."""

            results = []

            for signal, bits in interface["signals"].iteritems():
                if bits:
                    results.append((signal, bits))

            return results

        # Create list of (list of (signal, bit) tups).

        vec_signal_tups = [get_vec_signals(interface) for interface
                           in interfaces.values()]

        # Flatten vec_signal_tups

        vec_signals = sum(vec_signal_tups, [])

        # Print wire definition statements for array signals.

        wire_exp = "wire %s [%d:0];"

        for signal, bits in vec_signals:
            total_bits = bits * area
            print wire_exp % (signal, total_bits-1)


        ###################prints the port_data_type definitions###########
        print "//  --------------------input/output data types------------------"
        print "\n"

        ################### prints all the instansiations of the modules given the area ##############
        print "//  --------------------module instancces-----------------"

        for n in range(area):
            port_parts = [create_interface_def(n, x) for x in interface_keys]
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
