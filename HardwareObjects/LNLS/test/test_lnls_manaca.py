#!/usr/bin/env python

""" Test config in lnls/manaca."""

# Use these command in python shell to keep polling imgs
import os, sys
from HardwareRepository import HardwareRepository as hwr

# Path to custom ho classes
fname = '/opt/mxcube3/mxcube3/HardwareRepository/'
path_to_xmls = '/opt/mxcube3/mxcube3/HardwareRepository/HardwareObjects/LNLS/lnls_sim'

print('\n\nTesting config for lnls/manaca')
print('\n\nPath to HardwareRepository: ' + str(fname))
print('Path to XMLs:' + str(path_to_xmls))

# Connect to HardwareRepository
print('\n\nSetting up HR')
hwr.addHardwareObjectsDirs([os.path.join(fname, 'HardwareObjects')])
my_hwr = hwr.getHardwareRepository(path_to_xmls)
my_hwr.connect()
print('my_hwr = ' + str(my_hwr))

# Load machine info HO by xml
print('\n\nLoading machine info')
#ho_mach_info = my_hwr.getHardwareObject('mach-info')
#print('type(ho_mach_info) = ' + str(ho_mach_info))
#print('ho_mach_info.getCurrent() = ' + str(ho_mach_info.getCurrent()))

# Load a motor (omega) HO by xml
print('\n\nLoading omega motor')
ho_omega = my_hwr.getHardwareObject('udiff_omega')
print('type(ho_omega) = ' + str(ho_omega))
print('ho_omega.getPosition() = ' + str(ho_omega.getPosition()))

# Load camera HO by xml
print('\n\nLoaing camera')
ho_cam = my_hwr.getHardwareObject('md_camera')
print('type(ho_cam) = ' + str(ho_cam))
error_cam = ho_cam.getCameraImage()
print('error = ' + str(error_cam))
print('ho_cam.imgArray = ' + str(ho_cam.imgArray))
