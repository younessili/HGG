`define BITS 8

module pusher (clk, reset, item_in, item_out);

	input clk;
	input reset;
	input [`BITS-1:0] item_in;
	output [`BITS-1:0] item_out;

	assign item_out = item;

	 reg [`BITS-1:0] item;

	 always @(posedge clk or posedge reset) begin

	 	if (reset) begin

	 		item <= 0;

	 	end else begin

	 		item <= item_in;
	 		$display("I latched an item: %d", item_in);

	 	end

	 end

endmodule
