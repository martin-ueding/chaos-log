# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles:=$(wildcard *.py)

###############################################################################
#                               Public Targets                                #
###############################################################################

epydoc: html/index.html

test:
	bash testrun.sh

clean:
	$(RM) *.pyc
	$(RM) -r html
	$(RM) chaos_logc

###############################################################################
#                               Private Targets                               #
###############################################################################

html/index.html: chaos_log $(pythonfiles)
	epydoc -v $^
