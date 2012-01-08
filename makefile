# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles:=$(wildcard *.py)

epydoc: html/index.html

test:
	bash testrun.sh

html/index.html: chaos_log $(pythonfiles)
	epydoc -v $^

clean:
	$(RM) *.pyc
	$(RM) -r html
	$(RM) chaos_logc
