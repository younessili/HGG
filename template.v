module {{ module_name }}(clk, reset, data_in, data_out);

	input clk;
	input reset;
	input [7:0] data_in;
	output [7:0] data_out;

	assign data_out = 0; // for now


//  --------------------input/output data types-----------

{{ wire_defs }}

//  --------------------module instancces-----------------

{% for item in instances %}
	{{ item }}
{%- endfor %}

//  --------------------module assignments-----------------

{% for item in assignments %}
	{{ item }}
{%- endfor %}


endmodule
