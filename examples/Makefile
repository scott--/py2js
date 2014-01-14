
generate: gol.html triangulation.html ui.html can.html three_demo.html

%.html: %.py
	@echo "Compiling [$<]"
	@PYTHONPATH=.. python $< > $@

clean:
	@rm -fv *.html *~
