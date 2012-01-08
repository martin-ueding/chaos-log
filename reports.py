#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

__docformat__ = "javadoc en"


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


def maximum (computer):
    cpustats = computer.cpustats()
    
    print "CPU Load   Min: %6.1f,   Max: %6.1f,   Avg: %6.1f " % (cpustats["cpu"]["min"], cpustats["cpu"]["max"], cpustats["cpu"]["avg"])
    print "Memory     Min: %6.1f M, Max: %6.1f M, Avg: %6.1f M" % (cpustats["mem"]["min"], cpustats["mem"]["max"], cpustats["mem"]["avg"])
    print "Swap       Min: %6.1f M, Max: %6.1f M, Avg: %6.1f M" % (cpustats["swap"]["min"], cpustats["swap"]["max"], cpustats["swap"]["avg"])
    print
  
    mintemp = computer.mintemp()
    maxtemp = computer.maxtemp()
    avgtemp = computer.avgtemp()
    print "CPU        Min: %3.1f °C,  Max: %3.1f °C,  Avg: %3.1f °C" % (mintemp[0], maxtemp[0], avgtemp[0])
    print "Mainboard  Min: %3.1f °C,  Max: %3.1f °C,  Avg: %3.1f °C" % (mintemp[1], maxtemp[1], avgtemp[1])
        

def computer_overview(outfile, computer):
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    writer.writerow(["Timestamp", "Load Average", "Memory MB", "Swap MB", "Temp CPU °C", "Temp Mainboard °C"])
    for cpu, temp in zip(computer.cstates, computer.tstates):
        data = [time.mktime(cpu.time.timetuple()), cpu.cpu, cpu.mem, cpu.swap, temp.cpu, temp.mb]
        writer.writerow(data)


def mywrite(datalist, writer, outfile, format="plain"):
    """
    Writes a list of data to the outfile either in CSV or plain text format.
    """
    if format == "csv":
        writer.writerow(datalist)
    else:
        outfile.write(" ".join(map(str, datalist))+"\n")
