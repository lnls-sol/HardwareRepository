#!/usr/bin/env python3

from epics import PV
from PyQt4 import  QtGui
import numpy as np
from PIL import Image

""" Get camera image from epics and write to file."""

#data = PV('13SIM1:image1:ArrayData').get(timeout=10)
data = PV('MNC:B:BZOOM:image1:ArrayData').get(timeout=10)
print('data = ' + str(data))

pixel_size = 3
#width = 1024
#height = 1024
width = 2560
height = 2048

#qimg = QtGui.QImage(data, 1280, 1024, 1280*32/8, QtGui.QImage.Format_RGB32)
#print('\n\nqimg.width() = ' + str(qimg.width()))
#print('qimg.height() = ' + str(qimg.height()))
#print('qimg.bytesPerLine() = ' + str(qimg.bytesPerLine()))

arr = np.array(data).reshape(height, width, pixel_size)

# Write binary data to a file
#qimg.save(r"./image_qt.jpg",format = 'jpeg') # works
img = Image.fromarray(arr)
#img_rot = img.rotate(angle=0, expand=True)
img_rgb = img.convert('RGB')
print(img_rgb.tobytes()[0:100])
img_rgb.save("image_pil.jpg")
