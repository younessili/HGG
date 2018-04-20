`define BITS 8

module pusher(reset, item_out, item_in, clock);

	localparam id = 0;

	input clock;
	input reset;
	input [`BITS-1:0] item_in;
	output [`BITS-1:0] item_out;

	assign item_out = item;

	reg [`BITS-1:0] item;

	always @(posedge clock or posedge reset) begin

		if (reset) begin

			item <= 0;

		end else begin

			item <= item_in;
			$display("(pusher %d): I latched item %d", id, item_in);

		end

	end

endmodule
