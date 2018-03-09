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
