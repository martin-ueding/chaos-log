#!/bin/bash
# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

# Exercises the chaos_log program with various options. This script fails if
# one of the runs fail.

set -e
set -u

./chaos_log --help
./chaos_log data --max
./chaos_log data --computer
./chaos_log data --process java
./chaos_log data --computer --format plain
./chaos_log data --dump
