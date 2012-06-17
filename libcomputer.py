#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

###############################################################################
#                                   License                                   #
###############################################################################
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

"""
Models a computer with temperature states and multiple processes.
"""

__docformat__ = "restructuredtext en"

class Process(object):
    """
    Models a running process with several states.
    """
    def __init__(self, pid, command, pstates=[]):
        self.pid = pid
        self.command = command
        self.pstates = pstates

    def add_pstate(self, pstate):
        """
        Appends a process state to this process.

        :param pstate: PState object to add.
        """
        self.pstates.append(pstate)

    def __repr__(self):
        return "Process(%s, %s, %s)" % (repr(self.pid), repr(self.command), repr(self.pstates))


class Computer(object):
    """
    A computer which has several processes and temperature and overal usage states.
    """
    def __init__(self, cstates=[], tstates=[], processes={}):
        self.cstates = cstates
        self.tstates = tstates
        self.processes = processes

    def __repr__(self):
        return "Computer(%s, %s, %s)" % (repr(self.cstates), repr(self.tstates), repr(self.processes))

    def mintemp(self):
        """
        Minimal temperature of CPU and mainboard.

        :return: Tuple with min CPU an MB temperatures.
        """
        return min([x.cpu for x in self.tstates]), min([x.mb for x in self.tstates])

    def maxtemp(self):
        """
        Maximal temperature of CPU and mainboard.

        :return: Tuple with max CPU an MB temperatures.
        """
        return max([x.cpu for x in self.tstates]), max([x.mb for x in self.tstates])

    def avgtemp(self):
        """
        Average temperature of CPU and mainboard.

        :return: Tuple with average CPU an MB temperatures.
        """
        return avg([x.cpu for x in self.tstates]), avg([x.mb for x in self.tstates])

    def cpustats(self):
        """
        Calculates the min, max and average for the computer's performance over all time.

        :return: Dict with cpu, mem and swap, each containing a dict with min, max and avg.
        """
        return {"cpu":  {"min": min([x.cpu for x in self.cstates]), "max": max([x.cpu for x in self.cstates]), "avg": avg([x.cpu for x in self.cstates])},
                "mem":  {"min": min([x.mem for x in self.cstates]), "max": max([x.mem for x in self.cstates]), "avg": avg([x.mem for x in self.cstates])},
                "swap": {"min": min([x.swap for x in self.cstates]), "max": max([x.swap for x in self.cstates]), "avg": avg([x.swap for x in self.cstates])}
          }


class PState(object):
    """
    Process state.
    """
    def __init__(self, time, cpu, mem, status):
        """
        New PState object.

        :param time: Datetime.
        :param cpu: CPU usage.
        :param mem: Memory usage.
        :param status: Process status.
        """
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.status = status

    def __repr__(self):
        return "PState(%s, %s, %s, %s)" % (repr(self.time), repr(self.cpu), repr(self.mem), repr(self.status))


class CState(object):
    """
    Computer state.
    """
    def __init__(self, time, cpu, mem, swap):
        """
        New CState object.

        :param time: Datetime.
        :param cpu: Load average.
        :param mem: Memory usage.
        :param swap: Swap usage.
        """
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.swap = swap

    def __repr__(self):
        return "CState(%s, %s, %s, %s)" % (repr(self.time), repr(self.cpu), repr(self.mem), repr(self.swap))


class TState(object):
    """
    Temperature state.
    """
    def __init__(self, time, cpu, mb):
        """
        New CState object.

        :param time: Datetime.
        :param cpu: CPU temperature.
        :param mb: Mainboard temperature.
        """
        self.time = time
        self.cpu = cpu
        self.mb = mb

    def __repr__(self):
        return "TState(%s, %s, %s)" % (repr(self.time), repr(self.cpu), repr(self.mb))


def avg(l):
    """
    Return the average of list items.

    :param l: List with summable items.
    :return: Average of the list.
    """
    return sum(l) / len(l)
