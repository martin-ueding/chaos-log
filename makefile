pythonfiles:=$(wildcard *.py)

epydoc: html/index.html

html/index.html: chaos_log $(pythonfiles)
	epydoc $^
