#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

__doctype__ = "javadoc en"


def parsefolder(arg, dirname, names):
    """
    Parses a folder. All files are passed to the parsefile function.
    """
    names.sort()
    if options.verbose:
        print "Parsing", dirname
    for name in names:
        if not os.path.isfile(dirname+"/"+name):
            continue

        parsefile(dirname, name)
        

def gettime(dirname, name):
    """
    Parses a time from the folder name.
    """
    timefolder = os.path.basename(dirname)
    datefolder = os.path.basename(os.path.dirname(dirname))
    
    time = datetime.datetime(int(datefolder[0:4]), int(datefolder[5:7]), int(datefolder[8:10]), int(timefolder[:2]), int(name[:2]))
     
    return time


def parsefile(dirname, name):
    """
    Determines which type of file is given and calls the apropriate parse method.

    Side effects:
        - options
    """
    if name.endswith("processes.log"):
        if options.files:
            print "Parsing", dirname+"/"+name
        parseprocesses(dirname, name, gettime(dirname, name))
    elif name.endswith("sensors.log"):   
        if options.files:
            print "Parsing", dirname+"/"+name
        parsetemp(dirname, name, gettime(dirname, name))


def parsetemp(dirname, name, time):
    """
    Parse a temperature file.

    Side effects:
        - computer
    """
    with open(dirname+"/"+name) as f:
      lines = f.read().split("\n")
      
      if len(lines) < 11:
        return
      
      cpu = float(lines[9].split()[2])
      mb = float(lines[10].split()[2])
      
      state = TState(time, cpu, mb)
      computer.tstates.append(state)


def parseprocesses(dirname, name, time):
    """
    Parse a process file.

    Side effects:
        - computer
    """
    with open(dirname+"/"+name) as f:
        cpu = float(f.readline().split()[12][:-1])
        f.readline()
        f.readline()
        mem = float(f.readline().split()[3][:-1]) / 1024
        swap = float(f.readline().split()[3][:-1]) / 1024
        
        f.readline()
        f.readline()
        
        cstate = CState(time, cpu, mem, swap)
        
        computer.cstates.append(cstate)

        for line in f:
            data = line.split()

            if len(data) < 12:
                continue

            pid = int(data[0])
            command = data[11]

            state = PState(time, float(data[8]), float(data[9]), data[7])

            key = (pid, command)
            
            if key in computer.processes:
                current = computer.processes[key]
            else:
                current = Process(pid, command, [])
                computer.processes[(pid, command)] = current

            current.pstates.append(state)
