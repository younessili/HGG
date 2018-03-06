#!/usr/bin/env python

import sys
import json
import jinja2

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
    str_def = "  %s r%d (%s);"  #module definition here (%s) is %s [%d], %s[%d], %s[%d], %s[%d]
    assignment_exp = "%s[%d]<=%s[%d];"
    interface_keys = interfaces.keys()
    wire_exp = "wire %s [%d:0];"

    def get_vec_signals(interface):
        """Given an inteface dictionary, return a list of (signal, bits)
        where bits>0."""

        results = []
        for signal, bits in interface["signals"].iteritems():
            if bits:
                results.append((signal, bits))
        return results


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
        #print "//neighbours connections \n"

        assignments_keys = " ".join(assignments.keys())
        assignments_values = " ".join(assignments.values())

        for i in range (width-1):
            #print "// Connector block (index = %d):" %i
            return assignment_exp % (assignments_values, i, assignments_keys, i+1)


    def create_block_code():


               
        ###################prints the IO defiinitions#############

        # Create list of (list of (signal, bit) tups).
        vec_signal_tups = [get_vec_signals(interface) for interface in interfaces.values()]

        # Flatten vec_signal_tups
        vec_signals = sum(vec_signal_tups, [])

        # Print wire definition statements for array signals.
        for signal, bits in vec_signals:
            total_bits = bits * area
            wire_expression_list = wire_exp % (signal, total_bits-1)



        ################### prints all the instansiations of the modules given the area ##############
        print "//  --------------------module instancces-----------------"

        for n in range(area):
            port_parts = [create_interface_def(n, x) for x in interface_keys]
            port_def = ", ".join(port_parts)
            module_instances_list= str_def % (module_name, n, port_def)


        templateLoader = jinja2.FileSystemLoader( searchpath="/" )
        templateEnv = jinja2.Environment( loader=templateLoader )
        TEMPLATE_FILE = "/cygdrive/c/project/test_python/template.v"
        template = templateEnv.get_template( TEMPLATE_FILE )
        templateVars = {
        "module_name" : module_name,
        "wire_defs" : wire_expression_list, 
        "instances" : str_def % (module_name, n, port_def),
        "assignments":create_module_assigmnet()
        }
        outputText = template.render( templateVars )
        print outputText
    

    create_block_code()
##############################################################################
def main():
    """main function"""
    config_file_path = sys.argv[1]      #takes the input from the user and stores it in a variable.
    generate_code(config_file_path) #feed the "module name" entry in the json file to the generate code function
##############################################################################

if __name__ == '__main__':
    main()
