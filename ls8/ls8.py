#!/usr/bin/env python3

"""Main."""

import sys
# from examples import mult.ls8
from cpu import *

cpu = CPU()

cpu.load(sys.argv)
cpu.run()
