
generate: gol.html triangulation.html ui.html can.html

%.html: %.py
	@echo "Compiling [$<]"
	@PYTHONPATH=.. python $< > $@

clean:
	@rm -fv *.html *~
