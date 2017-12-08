
## SoC Hardware Graph Generator (HGG)

### What?

**HGG** is an automated tool for generating Verilog modules for digital design on a system on chip (SoC) interface which is written in python. The tool gets the HDL design specifications from the user by reading a configuration file which is filled by the user (see _Config file_ on how to do this). The code produced is also known as a hardware graph which is a top-level hardware module that contains instances of the components of the SoC, internal interfaces and connections. 

---
### why?

**HGG** is an opitmal solution for the problem of producing HDL code for systems with very large number of interconnected components and cores. This process takes significant amount of time and is very prone to errors. Additionally, it can be a quick an easy fix for comparing the generated code with a user written one for educational purposes, especially for students who have less expeirence with verilog and HDL design for SoC interfaces. 

---
### How?

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

#### gettting a copy of the software

1. go to the github repository [here](https://github.com/aliyou1333/test-python).
2. clone or download the latest version of the software. 
3. unzip the file to a local directory if nessecary.
4. open the config file in a text viewer such as sublime or notpad++.
5. edit the fields as desired to match your digital design module. (see **configuration file** for step by step process)
6. save the configuration file and run the software in a python compiler such as cygwin or a python emulator.
7. see or copy the output striaght from the emulator output or from the `output.log` file. This is excutable verilog code 

##### Running and testing the program 

* for running the software you need to compiler the `main.py` file with the configuration file `config_v2.json` as an argument to be fed to the software. **example**: `python main.py config_v2.json`
* for testing and implementing the verilog code you will need an HDL compiler such as [Icarus verilog](http://iverilog.icarus.com/)
* The output code will run just like any other verilog code with the `vpp` command. please refer to documentiation on how to do this online or [here](http://iverilog.wikia.com/wiki/Getting_Started)

##### Configuration file 

correctly filling up the configuration file is the most important task for running the software correctly please look at the examples below. The config file is writtne in `json` format so it consist of nested lists of information about the hardware module. In most cases the user is to change the **values** of the json lists and not their **keys** . refer to documentation for more information on this.

* enter the module name e.g. `"module_name":"router",` note at the end of each list or array there should be a `,` unless it is the last entry of the list i.e. data between a pair of `{}`

* enter the module dimensions this is an array of 2 integers `"dimensions":[3,3],` . This is *width* and *height* reespectivley. note that the SoC interfaces, usually have a regular square size, this means the dimensions are the same.

* Next put in all the port names that each module would have. an example is as follows
```"port_names":
	{  
      "north":"CLK",
      "south":"RESET",
      "east":"TX",
      "west":"RX",
      "north_west":"LOCAL"
   },```
Note not to change the port_names keys (*the left hand column*) this could cause the software to crash

* Define the port interfaces and input and output type. for multi bit wires such as a 15 down to 0 wire just write 16 infront of the interface you defined this will be interpretedd as a 16 bit wire. example:
```"TX":
	{  
     "signals":
     {  
        "tx_req":1,
        "tx_ack":4,
        "tx_data":16
     },
     "IO":
     {  
        "input":"tx_ack",
        "output":"tx_req,tx_data"
     }
    },```


---
### Documentation

Add link to dessirtation here.

---
### Authors
* **Ali Younessi** - *Initial work* - [Aliyou1333](https://github.com/aliyou1333/)

* contributors: [Ghaith](https://github.com/gtarawneh) who supervised this project.

---
### Acknowledgments

---

