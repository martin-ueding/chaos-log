#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

import datetime
import itertools
import optparse
import os


class Process(object):
    def __init__(self, pid, command):
        self.pid = pid
        self.command = command
        self.pstates = []

    def add_pstate(self, pstate):
        self.pstates.append(pstate)

		
	def __repr__(self):
		return pid, command, pstates

class Computer(object):
    def __init__(self):
        self.pstates = []
        self.tstates = []
        self.processes = []

	def __repr__(self):
		return processes

class PState(object):
    def __init__(self, time, cpu, mem, status):
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.status = status

	def __repr__(self):
		return time, cpu, mem, status

class TState(object):
    def __init__(self, cpu, mb):
        self.cpu = cpu
        self.mb = mb


def main():
    parser = optparse.OptionParser()
    #parser.add_option("", dest="", type="", default=, help=)

    (options, args) = parser.parse_args()
    del parser

    global computer
    computer = Computer()

    for infolder in args:
        os.path.walk(infolder, parsefolder, None)

    print computer

def parsefolder(arg, dirname, names):
    names.sort()
    print "Parsing", dirname
    for name in names:
        if not os.path.isfile(dirname+"/"+name):
            continue

        parsefile(dirname, name)

def parsefile(dirname, name):
    if name.endswith("processes.log"):
        print "Parsing", name
        parseprocesses(dirname, name)

def parseprocesses(dirname, name):
    timefolder = os.path.basename(dirname)
    datefolder = os.path.basename(os.path.dirname(dirname))

    time = datetime.datetime(
        int(datefolder[0:4]),
        int(datefolder[5:7]),
        int(datefolder[8:10]),
        int(timefolder[:2])
    )

    with open(dirname+"/"+name) as f:
        for lineno, line in zip(itertools.count(), f):
            if (lineno < 7):
                continue

            else:
                data = line.split()

                if len(data) < 12:
                    continue

                pid = data[0]
                command = data[11]

                state = PState(time, data[8], data[9], data[7])

                current = None
                for process in computer.processes:
                    if process.pid == pid and process.command == command:
                        corrent = process
                        break

                if current is None:
                    current = Process(pid, command)
                    computer.processes.append(current)

                current.pstates.append(state)





if __name__ == "__main__":
	main()
