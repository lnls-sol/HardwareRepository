"""
LNLSMotor.py
"""
import logging
from AbstractMotor import AbstractMotor
from HardwareRepository.BaseHardwareObjects import Device
from time import sleep
import gevent

#------------------------------------------------------------------------------
# Constant names from lnls-motor.xml
MOTOR_VAL  = 'epicsMotor_val'
MOTOR_RLV  = 'epicsMotor_rlv'
MOTOR_RBV  = 'epicsMotor_rbv'
MOTOR_DMOV = 'epicsMotor_dmov'
MOTOR_STOP = 'epicsMotor_stop'
MOTOR_VELO = 'epicsMotor_velo'
MOTOR_DLLM = 'epicsMotor_dllm'
MOTOR_DHLM = 'epicsMotor_dhlm'
MOTOR_EGU  = 'epicsMotor_egu'

#------------------------------------------------------------------------------
class LNLSMotor(AbstractMotor, Device):
    (NOTINITIALIZED, UNUSABLE, READY, MOVESTARTED, MOVING, ONLIMIT) = (0,1,2,3,4,5)
    EXPORTER_TO_MOTOR_STATE = { "Invalid": NOTINITIALIZED,
                                "Fault": UNUSABLE,
                                "Ready": READY,
                                "Moving": MOVING,
                                "Created": NOTINITIALIZED,
                                "Initializing": NOTINITIALIZED,
                                "Unknown": UNUSABLE }

    def __init__(self, name):
        AbstractMotor.__init__(self)
        Device.__init__(self, name)

    def init(self):
        self.motorState = LNLSMotor.READY
        # Set current position
        self.motorPosition = self.getPosition()
        self.motorgen = None

        self.monitorgen = None

        self.chan_motor_rbv = self.getChannelObject(MOTOR_RBV)
        if self.chan_motor_rbv is not None:
            self.chan_motor_rbv.connectSignal('update', self.positionChanged)

        self.chan_motor_dmov = self.getChannelObject(MOTOR_DMOV)
        if self.chan_motor_dmov is not None:
            self.chan_motor_dmov.connectSignal('update', self.statusChanged)

    def monitor(self, monitor):
        pass

    def connectNotify(self, signal):
        if signal == 'positionChanged':
            self.emit('positionChanged', (self.getPosition(), ))
        elif signal == 'stateChanged':
            self.motorStateChanged(self.getState())
        elif signal == 'limitsChanged':
            self.motorLimitsChanged()

    def updateState(self):
        pass

    def updateMotorState(self, motor_state):
        self.motorState = motor_state

    def motorStateChanged(self, state):
        self.emit('stateChanged', (self.motorState, ))

    def getState(self):
        return self.motorState

    def isReady(self):
        return (self.motorState == LNLSMotor.READY)

    def motorLimitsChanged(self):
        self.emit('limitsChanged', (self.getLimits(), ))

    def getLimits(self):
        try:
            limits = (self.getValue(MOTOR_DLLM), self.getValue(MOTOR_DHLM))
        except:
            logging.getLogger("HWR").error('Error getting motor limits for: %s' % self.motor_name)
            # Set a default limit
            limits = (-1E4,1E4)
            pass

        return limits

    def getPosition(self):
        return self.getValue(MOTOR_RBV)

    def setVelocity(self, value):
        self.setValue(MOTOR_VELO, value)

    def getVelocity(self):
        return self.getValue(MOTOR_VELO)

    def isMoving(self):
        return (self.getValue(MOTOR_DMOV) == 0)

    def getDialPosition(self):
        return self.getPosition()

    def move(self, absolutePosition, wait=False):
        self.setValue(MOTOR_VAL, absolutePosition)

        if (wait):
            self.waitEndOfMove(0.1)
        else:
            self.motorgen = gevent.spawn(self.waitEndOfMove, 0.1)

    def moveRelative(self, relativePosition, wait=False):
        self.setValue(MOTOR_RLV, relativePosition)

        if (wait):
            self.waitEndOfMove(0.1)
        else:
            self.motorgen = gevent.spawn(self.waitEndOfMove, 0.1)

    def waitEndOfMove(self, timeout=None):
        gevent.sleep(0.1)
        if (self.getValue(MOTOR_DMOV) == 0):
            self.motorState = LNLSMotor.MOVING
            self.emit('stateChanged', (self.motorState))

        while (self.getValue(MOTOR_DMOV) == 0):
            self.motorPosition = self.getPosition()
            self.emit('positionChanged', (self.motorPosition))
            gevent.sleep(0.1)
        self.motorState = LNLSMotor.READY
        self.emit('stateChanged', (self.motorState))
        self.motorPosition = self.getPosition()
        self.emit('positionChanged', (self.motorPosition))

    def positionChanged(self, value):
        self.motorPosition = value
        self.emit('positionChanged', (value))

    def statusChanged(self, value):
        if (value == 0):
            self.motorState = LNLSMotor.MOVING
        elif (value == 1):
            self.motorState = LNLSMotor.READY

        self.emit('stateChanged', (self.motorState))

    def syncMoveRelative(self, relative_position, timeout=None):
        self.motorPosition = relative_position

    def syncMove(self, position, timeout=None):
        self.motorPosition = position

    def motorIsMoving(self):
        return self.isMoving()

    def getMotorMnemonic(self):
        return self.motor_name

    def getEgu(self):
        try:
            return self.getValue(MOTOR_EGU)
        except:
            return "Unknown"

    def stop(self):
        self.setValue(MOTOR_STOP, 1)
        gevent.sleep(0.2)
        self.setValue(MOTOR_STOP, 0)

    def update_values(self):
        self.emit('positionChanged', (self.motorPosition))
        self.emit('stateChanged', (self.motorState))

    def __del__(self):
        print("LNLSMotor __del__")
        self.monitor(False)
