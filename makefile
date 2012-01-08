# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles:=$(wildcard *.py)

###############################################################################
#                               Public Targets                                #
###############################################################################

# Generates documentation from the Python source code.
epydoc: html/index.html

# Runs a test.
test:
	bash testrun.sh

# The usual stuff, cleans all build files or files that can be easily created.
clean:
	$(RM) *.pyc
	$(RM) -r html
	$(RM) chaos_logc

###############################################################################
#                               Private Targets                               #
###############################################################################

html/index.html: chaos_log $(pythonfiles)
	epydoc -v $^
