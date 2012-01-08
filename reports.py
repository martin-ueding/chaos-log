#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

__doctype__ = "javadoc en"


import csv
import sys
import time


def dump(outfile, computer):
    outfile.write(repr(computer))
    outfile.write("\n")


def process_report(outfile, processes, selected_process, format):
    """
    """
    selected = None
    for process in processes:
        if process[1] == selected_process:
            selected = processes[process]
            
    if selected is None:
        print "There is no process %s." % selected_process
        sys.exit(1)
        
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    mywrite(["Timestamp", "CPU %", "Memory %", "Status"], writer, outfile, format)
    for state in selected.pstates:
        data = [time.mktime(state.time.timetuple()), state.cpu, state.mem, state.status]
        mywrite(data, writer, outfile)
        

def mywrite(datalist, writer, outfile, format="plain"):
    """
    Writes a list of data to the outfile either in CSV or plain text format.
    """
    if format == "csv":
        writer.writerow(datalist)
    else:
        outfile.write(" ".join(map(str, datalist))+"\n")
