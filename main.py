#!/usr/bin/env python

import sys
import json
import docopt
from jinja2 import Template

usage = """
HGG version 0.1

Usage:
  hgg [--quiet] <config> <template>

Options:
  --quiet -q  Suppress printing information messages.
  --version -v  Print version.

"""

##############################################################################
def load_json(file):
    """Return the json object by loading the json file  """
    with open(file, "r") as json_data:
        return json.load(json_data)   #load the json file in read mode.
##############################################################################
def load_file(file):
    """Return the file in read mode"""
    with open(file, "r") as fid:
        return fid.read()
##############################################################################
def check_input(config_file_path):
    """Return the main file elements by loadding the congfig file.
    do this after data validation    """

    #try loading the file if there is an IO error stop and print error message
    try:
         config = load_json(config_file_path)
    except IOError:
        print('There was No such file to open!')
        sys.exit(1)
    try:
        #set the block name to the "module name" entry in the json files
        module_name = config["module_name"]
        width, height = map(int, config["dimensions"])
        interfaces = config ["interfaces"]
        assignments = config["assignments"]
    except:
        print('There was an error in the config file!')
        sys.exit(1)
    return (interfaces, module_name, width, height,assignments)
##############################################################################
def generate_code(config_file_path, template_file):
    """generate the module instances and assignments"""

    ######################list of segment definitions#########################
    (interfaces,module_name,
    width, height,assignments) = check_input(config_file_path)

    area = width * height     #Area of the module
    str_def = "%s r%d (%s);"  #module definition here (%s) is %s[%d]
    assignment_exp = "%s[%d:%d] <= %s[%d:%d];"
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
        """return the argument for the module instances
         based on the number of data lines for each interface. """

        start_bit = port_width * mod_index
        end_bit = (port_width * (mod_index+1) )- 1

        if port_width == 0:
            return port_name
        elif start_bit == end_bit:
            one_bit_def = "%s [%d]" % (port_name, start_bit)
            return one_bit_def
        else:
            multi_bit_def ="%s[%d:%d]" % (port_name, end_bit, start_bit)
            return multi_bit_def

    def create_interface_def(mod_index, interface):
        """Return a Verilog port declaration string
        representing the interface."""

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
        """create module assignments based on the user assignments."""

        assignments_list =[]

        for key, val in assignments.iteritems():

            for i in range (width-1):
                in_start = (i+1) * width
                in_finish = (i+2) * width - 1

                out_start = i * width
                out_finish = (i+1) * width - 1

                item = assignment_exp % (
                    val, in_finish, in_start, key, out_finish, out_start)

                assignments_list.append(item)

        return assignments_list

    def create_block_code():
        """populat jinja2 template by calling the functions above."""

        # Create list of (list of (signal, bit) tups).
        vec_signal_tups = [get_vec_signals(interface)
                for interface in interfaces.values()]

        # Flatten vec_signal_tups
        vec_signals = sum(vec_signal_tups, [])

        # Print wire definition statements for array signals.
        wire_expression_list = []
        for signal, bits in vec_signals:
            total_bits = bits * area
            wire_expression_list.append(wire_exp % (signal, total_bits-1))

        instances_list =[]
        for n in range(area):
            port_parts = [create_interface_def(n, x) for x in interface_keys]
            port_def = ", ".join(port_parts)
            instances_list.append(str_def % (module_name, n, port_def))

        template_str = load_file(template_file)
        template = Template(template_str)
        content = {
            "module_name": module_name,
            "wire_defs" : wire_expression_list,
            "instances" : instances_list,
            "assignments":create_module_assigmnet()
        }
        print template.render(**content)

    create_block_code()

##############################################################################
def main():
    """main function"""
    args = docopt.docopt(usage, version="0.1")
    #takes the input from the user and stores it in a variable.
    config_file_path = sys.argv[1]
    config_file_path = args["<config>"]
    template_file = args["<template>"]
    generate_code(config_file_path, template_file)
##############################################################################

if __name__ == '__main__':
    main()
