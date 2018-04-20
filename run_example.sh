#!/bin/bash

echo "Generating top.v ..."

python main.py config/pusher.json template/pusher.v > verilog/top.v

echo "Compiling testbench ..."

iverilog -I verilog verilog/testbench.v

echo "Executing testbench ..."

vvp a.out
