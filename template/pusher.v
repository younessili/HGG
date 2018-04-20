`include "pusher.v"

module top(clock, reset, data_in, data_out);

	input clock;
	input reset;
	input [7:0] data_in;
	output [7:0] data_out;

//  --------------------input/output data types-----------
{% for item in wire_defs %}
	{{ item }}
{%- endfor %}

//  --------------------module instancces-----------------

{% for item in instances %}
	{{ item }}
{%- endfor %}

//  --------------------module assignments-----------------

	assign item_in[7:0] = data_in;
{%- for item in assignments %}
	{{ item }}
{%- endfor %}



endmodule
