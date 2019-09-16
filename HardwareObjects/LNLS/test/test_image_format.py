from epics import PV
from PyQt4 import  QtGui
import numpy as np
from PIL import Image

""" Get camera image from epics and write to file."""

data = PV('MXROB:image_ueye:ArrayData').get(timeout=0.2)
print('data = ' + str(data))

width = 1280
height = 1024

#qimg = QtGui.QImage(data, 1280, 1024, 1280*32/8, QtGui.QImage.Format_RGB32)
#print('\n\nqimg.width() = ' + str(qimg.width()))
#print('qimg.height() = ' + str(qimg.height()))
#print('qimg.bytesPerLine() = ' + str(qimg.bytesPerLine()))

arr = np.array(data).reshape(height, width, 4)

# Write binary data to a file
#qimg.save(r"./image_qt.jpg",format = 'jpeg') # works
img = Image.fromarray(arr)
img_rot = img.rotate(angle=270, expand=True)
img_rgb = img_rot.convert('RGB')
print(img_rgb.tobytes()[0:100])
img_rgb.save("image_pil.jpg")
