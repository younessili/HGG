run: prepare_output
	@ ./main.py config_v2.json template.v\
	>> output.log 2>&1

testbench:
	@ iverilog -I verilog -o build/a.out verilog/testbench.v
	@ vvp build/a.out

clean:
	@ rm -rf build/*

prepare_output:
	@ date > output.log
	@ date | sed 's/./#/g' >> output.log
	@ echo "" >> output.log
