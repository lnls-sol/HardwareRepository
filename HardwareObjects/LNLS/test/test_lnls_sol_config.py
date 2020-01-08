#!/usr/bin/env python3

""" Test config in HR/configuration/lnls_sol."""

# Use these command in python shell to keep polling imgs
import os, sys, time
from HardwareRepository import HardwareRepository as hwr

BL_CONFIG_NAME = 'lnls_sol'

# Path to custom ho classes
fname = '/opt/mxcube3/mxcube3/HardwareRepository/'
path_to_xmls = '/opt/mxcube3/mxcube3/HardwareRepository/configuration/' + BL_CONFIG_NAME

print('\n\nTesting config for ' + BL_CONFIG_NAME)
print('\n\nPath to HardwareRepository: ' + str(fname))
print('Path to XMLs:' + str(path_to_xmls))

# Connect to HardwareRepository
print('\n\nSetting up HR')
hwr.addHardwareObjectsDirs([os.path.join(fname, 'HardwareObjects')])
hwr.init_hardware_repository(path_to_xmls)
my_hwr = hwr.getHardwareRepository()
my_hwr.connect()
print('my_hwr = ' + str(my_hwr))

# 1) Load machine info HO by xml
print('\n\nLoading machine info')
ho_mach_info = my_hwr.getHardwareObject('machine_info')
print('type(ho_mach_info) = ' + str(ho_mach_info))
print('ho_mach_info.getCurrent() = ' + str(ho_mach_info.getCurrent()))

# 2) Load a motor HO by xml
motor_name = 'udiff_phix'
print('\n\nLoading a motor ' + motor_name)
ho_motor = my_hwr.getHardwareObject(motor_name)
ho_motor.init()
print('type(ho_motor) = ' + str(ho_motor))
pos = ho_motor.get_position()
print('initial ho_motor.getPosition() = ' + str(pos))
print('moving to 6')
ho_motor.move(6)
time.sleep(4)
print('new pos= ' + str(ho_motor.get_position()))
ho_motor.move(pos)
time.sleep(4)

# 3) Load camera HO by xml
# PS: For starting AD pattern simulation:
# caput 13SIM1:cam1:Acquire 1
# caput 13SIM1:image1:EnableCallbacks 1
# caput 13SIM1:cam1:ColorMode RGB1
# caget -#100 13SIM1:image1:ArrayData

print('\n\nLoading camera')
ho_cam = my_hwr.getHardwareObject('md_camera')
print('type(ho_cam) = ' + str(ho_cam))
error_cam = ho_cam.getCameraImage()
print('error = ' + str(error_cam))
print('ho_cam.imgArray = ' + str(ho_cam.imgArray))
print('ho_cam.get_pixel_size() = ' + str(ho_cam.get_pixel_size()))
print('ho_cam.get_width() = ' + str(ho_cam.get_width()))
print('ho_cam.get_pixel_size() = ' + str(ho_cam.get_height()))

print('\n\nEnd of SOL config test.')
