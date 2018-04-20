`include "pusher.v"

module top(clock, reset, data_in, data_out);

	input clock;
	input reset;
	input [7:0] data_in;
	output [7:0] data_out;

//  --------------------input/output data types-----------

	wire [63:0] item_out;
	wire [63:0] item_in;

//  --------------------module instancces-----------------


	pusher #(.id(0)) r0 (reset, item_out[7:0], item_in[7:0], clock);
	pusher #(.id(1)) r1 (reset, item_out[15:8], item_in[15:8], clock);
	pusher #(.id(2)) r2 (reset, item_out[23:16], item_in[23:16], clock);
	pusher #(.id(3)) r3 (reset, item_out[31:24], item_in[31:24], clock);
	pusher #(.id(4)) r4 (reset, item_out[39:32], item_in[39:32], clock);
	pusher #(.id(5)) r5 (reset, item_out[47:40], item_in[47:40], clock);
	pusher #(.id(6)) r6 (reset, item_out[55:48], item_in[55:48], clock);
	pusher #(.id(7)) r7 (reset, item_out[63:56], item_in[63:56], clock);

//  --------------------module assignments-----------------

	assign item_in[7:0] = data_in;
	assign item_in[15:8] = item_out[7:0];
	assign item_in[23:16] = item_out[15:8];
	assign item_in[31:24] = item_out[23:16];
	assign item_in[39:32] = item_out[31:24];
	assign item_in[47:40] = item_out[39:32];
	assign item_in[55:48] = item_out[47:40];
	assign item_in[63:56] = item_out[55:48];



endmodule
