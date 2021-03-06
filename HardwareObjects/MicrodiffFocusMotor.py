from HardwareRepository.HardwareObjects.MD2Motor import MD2Motor
from HardwareRepository import HardwareRepository as HWR


class MicrodiffFocusMotor(MD2Motor):
    def __init__(self, name):
        MD2Motor.__init__(self, name)

    def init(self):

        if HWR.beamline.diffractometer.in_plate_mode():
            self.motor_name = self.getProperty("centring_focus")
        else:
            self.motor_name = self.getProperty("alignment_focus")
        MD2Motor.init(self)

    def motorPositionChanged(self, absolutePosition, private={}):
        MD2Motor.motorPositionChanged(self, absolutePosition, private)
