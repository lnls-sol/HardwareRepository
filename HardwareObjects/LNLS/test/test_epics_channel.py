#!/usr/bin/env python3

""" Test getting from Epics Command."""

from HardwareRepository.Command.Epics import EpicsChannel

ec = EpicsChannel('pv_command', 'SOL:S:m2')
res = ec.getValue()
print(res)

ec.setValue(res + 1)
res = ec.getValue()
print(res)
