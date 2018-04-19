module {{ module_name }}(clk,reset, data_in, data_out);

//  --------------------input/output data types-----------
{% for item in wire_defs %}
	{{ item }}
{%- endfor %}

//  --------------------module instancces-----------------

{% for item in instances %}
	{{ item }}
{%- endfor %}

//  --------------------module assignments-----------------

{% for item in assignments %}
	{{ item }}
{%- endfor %}


endmodule
