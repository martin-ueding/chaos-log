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

pythonfiles:=$(wildcard *.py)

###############################################################################
#                               Public Targets                                #
###############################################################################

# Generates documentation from the Python source code.
epydoc: html/index.html

check-doc: chaos_log $(pythonfiles)
	epydoc -v --check $^

# Runs a test.
test:
	bash testrun.sh

# The usual stuff, cleans all build files or files that can be easily created.
clean:
	$(RM) *.pyc
	$(RM) -r html
	$(RM) chaos_logc

###############################################################################
#                               Private Targets                               #
###############################################################################

html/index.html: chaos_log $(pythonfiles)
	epydoc -v $^
