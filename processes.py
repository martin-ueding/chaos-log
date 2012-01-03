#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

import optparse
import itertools
import os


class Process(object):
    def __init__(self, pid, command):
        self.pid = pid
        self.command = command
        self.pstates = []

    def add_pstate(self, pstate):
        self.pstates.append(pstate)

class Computer(object):
    def __init__(self):
        self.pstates = []
        self.tstates = []
        self.processes = []

class PState(object):
    def __init__(self, time, cpu, mem, status):
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.status = status

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
    with open(dirname+"/"+name) as f:
        for lineno, line in zip(itertools.count(), f):
            if (lineno < 7):
                continue

            else:
                data = line.split()

                for process in computer.processes:
                    pass


if __name__ == "__main__":
	main()
