pythonfiles:=$(wildcard *.py)

epydoc: html/index.html

test:
	bash testrun.sh

html/index.html: chaos_log $(pythonfiles)
	epydoc -v $^
