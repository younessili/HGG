module {{ module_name }}();

// some code to generate clock


//  --------------------input/output data types-----------

{{ wire_defs }}

//  --------------------module instancces-----------------

{% for item in instances %}
	{{ item }}
{%- endfor %}

//  --------------------module assignments-----------------

{{ assignments }}

endmodule
