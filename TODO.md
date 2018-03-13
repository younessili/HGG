# TODOS

## 2017-27-11

1. Add explicit net declarations, e.g. `wire [99:0] data` (numbers will depend on module count and interface definitions). DONE

2. Remove `port_types` from config file, and adjust code as necessary DONE

3. Add docstrings to all functions DONE

4. Create README in markdown DONE

- see this for example:

https://github.com/gtarawneh/copter/blob/master/README.md

- Read some articles under the "Articles" section of :

https://github.com/matiassingers/awesome-readme

## 2018-03-07

1. Fix issue with template (printing array instead of invidivual items as
lines) = by using Jinja2 for loops DONE

2. Create two directories `templates` and `config`, and place template and
config files inside (giving them meaningful names, like `pusher` and
`arbiter`). DONE

3. (for Ghaith): complete simulation testbench

4. (if time permits), have a look at PEP8 (style guidelines) and PEP20 (Zen of Python):

https://www.python.org/dev/peps/pep-0008/
https://www.python.org/dev/peps/pep-0020/

# Plan for Literature Review

## General organization of literature review:

1. The need for HDL code generation tools in general (reference systems such
as SpiNNaker and POETS)

2. Different types of code generation tool:

  - Tools that instantiate and connect components (e.g. SOPC) [this is the sub-category of code generation tools that HGG fit under]. Other examples of tools in this category are "Xilinx System Generator", and Matlab's Code HDL Coder.

  Have a look at: https://www.nutaq.com/matlab-hdl-coder-xilinx-system-generator

  and: https://www.xilinx.com/products/design-tools/vivado/integration/sysgen.html

  - Tools that perform language translations (e.g. high-level synthesis)

Light reads on System on Chip (SoC):

https://en.m.wikipedia.org/wiki/System_on_a_chip

and on Networks on Chip (NoC):

http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1652898

https://link.springer.com/chapter/10.2991/978-94-91216-92-3_5

## Altera Quartus SOPC Builder

This is a tool for generating system HDL by draggina and dropping components
in a GUI. It is similar to HGG in the sense that it enables hardware designers
to compose building clocks into larger systems.

Write a paragraph or two providing an overview of this tool, taking ideas from
say the first two pages of the tool's documentation, here:

https://www.altera.com/content/dam/altera-www/global/en_US/pdfs/literature/ug/ug_sopc_builder.pdf
