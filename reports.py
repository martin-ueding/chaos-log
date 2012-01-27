#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

"""
Reports for the gathered data.
"""

import csv
import sys
import time

def dump(outfile, computer):
    """
    Dumps the `computer` object.

    This can be reimported with `eval()` since it is a valid Python expression.
    Testing suggested that it might be faster to just reread the logfiles
    themselves.

    @param outfile: Filedescriptor to be written to.
    @param computer: Computer object containing all the data.
    """
    outfile.write(repr(computer))
    outfile.write("\n")


def process_report(outfile, processes, selected_process, format):
    """
    Writes all data concerning one specific process.

    @param outfile: Filedescriptor to be written to.
    @param processes: Dict of all the processes.
    @param selected_process: Process name that should be reported.
    @param format: Format for mywrite().
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
    """
    Reports minimum, maximum and average of different dimensions.

    This report is always written to STDOUT since it would be backwards to
    parse this. Write a new report instead.

    @param computer: Computer object containing all the data.
    """
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
    """
    Reports a table with the computers vitals.

    This includes time and load average, memory, temperature.

    @param outfile: Filedescriptor to be written to.
    @param computer: Computer object containing all the data.
    """
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    writer.writerow(["Timestamp", "Load Average", "Memory MB", "Swap MB", "Temp CPU °C", "Temp Mainboard °C"])
    for cpu, temp in zip(computer.cstates, computer.tstates):
        data = [time.mktime(cpu.time.timetuple()), cpu.cpu, cpu.mem, cpu.swap, temp.cpu, temp.mb]
        writer.writerow(data)


def mywrite(datalist, writer, outfile, format="plain"):
    """
    Writes a list of data to the outfile either in CSV or plain text format.

    @param datalist: List with data columns.
    @param writer: CSV writer object.
    @param outfile: Filedescriptor to be written to.
    @param format: "plain" or "csv" format to be written.
    """
    if format == "csv":
        writer.writerow(datalist)
    else:
        outfile.write(" ".join(map(str, datalist))+"\n")
