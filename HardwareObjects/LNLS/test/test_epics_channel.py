#!/usr/bin/env python3

""" Test getting from Epics Command."""

from HardwareRepository.Command.Epics import EpicsChannel

ec = EpicsChannel('pv_command', 'SOL:m2')
ec.getValue()
