`timescale 1ns/1ps
`include "top.v"

module testbench();

	reg clk, reset;

	reg [7:0] item_in;

	initial begin
		reset <= 1;
		clk <= 0;
		item_in <= 0;
		#0.5 reset <= 0;
	end

	always begin
		#0.5 clk <= ~clk;
	end

	always begin
		#1 item_in <= item_in + 1;
	end

	localparam DURATION = 20; // duration of simulation (time units)

	initial begin
		#DURATION $finish;
	end

	wire [7:0] item_out;

	top top1 (clk, reset, item_in, item_out);

endmodule
