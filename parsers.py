#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

"""
Contains the parser logic for ``top`` and ``sensors`` snapshots.
"""

import datetime
import os

import libcomputer

__docformat__ = "restructuredtext en"

def parsefolder(arg, dirname, names):
    """
    Parses a folder. All files are passed to the parsefile function.

    :param arg: Tuble containing program options and the computer.
    :param dirname: Directory to be processes.
    :param names: List of files in this directory.
    """
    options, computer = arg

    names.sort()
    if options.verbose:
        print "Parsing", dirname
    for name in names:
        if not os.path.isfile(dirname+"/"+name):
            continue

        parsefile(dirname, name, options.files, computer)


def gettime(dirname, name):
    """
    Parses a time from the folder name.

    :param dirname: Directory to be processes.
    :param name: List of files in this directory.
    """
    timefolder = os.path.basename(dirname)
    datefolder = os.path.basename(os.path.dirname(dirname))

    time = datetime.datetime(int(datefolder[0:4]), int(datefolder[5:7]), int(datefolder[8:10]), int(timefolder[:2]), int(name[:2]))

    return time


def parsefile(dirname, name, show_files, computer):
    """
    Determines which type of file is given and calls the apropriate parse method.

    :param dirname: Directory to be processes.
    :param name: List of files in this directory.
    :param show_files: Whether to show verbose information.
    :param computer: Computer this file belongs to.
    """
    if name.endswith("processes.log"):
        if show_files:
            print "Parsing", dirname+"/"+name
        parseprocesses(dirname, name, gettime(dirname, name), computer)
    elif name.endswith("sensors.log"):
        if show_files:
            print "Parsing", dirname+"/"+name
        parsetemp(dirname, name, gettime(dirname, name), computer)


def parsetemp(dirname, name, time, computer):
    """
    Parse a temperature file.

    :param dirname: Directory to be processes.
    :param name: List of files in this directory.
    :param time: Time of this snapshot.
    :param computer: Computer this temperature reading belongs to.
    """
    with open(dirname+"/"+name) as f:
      lines = f.read().split("\n")

      if len(lines) < 11:
        return

      cpu = float(lines[9].split()[2])
      mb = float(lines[10].split()[2])

      state = libcomputer.TState(time, cpu, mb)
      computer.tstates.append(state)


def parseprocesses(dirname, name, time, computer):
    """
    Parse a process file.

    :param dirname: Directory to be processes.
    :param name: List of files in this directory.
    :param time: Time of this snapshot.
    :param computer: Computer this process belongs to.
    """
    with open(dirname+"/"+name) as f:
        cpu = float(f.readline().split()[12][:-1])
        f.readline()
        f.readline()
        mem = float(f.readline().split()[3][:-1]) / 1024
        swap = float(f.readline().split()[3][:-1]) / 1024

        f.readline()
        f.readline()

        cstate = libcomputer.CState(time, cpu, mem, swap)

        computer.cstates.append(cstate)

        for line in f:
            data = line.split()

            if len(data) < 12:
                continue

            pid = int(data[0])
            command = data[11]

            state = libcomputer.PState(time, float(data[8]), float(data[9]), data[7])

            key = (pid, command)

            if key in computer.processes:
                current = computer.processes[key]
            else:
                current = libcomputer.Process(pid, command, [])
                computer.processes[(pid, command)] = current

            current.pstates.append(state)
