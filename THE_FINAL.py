#import RPi.GPIO as GPIO

#Code for controlling the direction of the motor based on the light sensor value. It basically mimics the phenomenon of phototropism where the plant grows to the light.
#Uses multitasking of python to operate the motors simultaneously.
from time import sleep
import RPi.GPIO as GPIO
import wiringpi2
from multiprocessing import Process
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import time


pin_base = 65
i2c_addr = 0x20

wiringpi2.wiringPiSetup()
wiringpi2.mcp23017Setup(pin_base, i2c_addr)
motor1=[4,17,27,22]
motor2=[5,6,13,19]
motor3=[26,14,15,18]
motor4 = [65,66,67,68]
motor5 = [69,70,71,72]
motor6 = [73,74,75,76]
motor7 = [77,78,79,80]

seq1 = [[1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1]]

seq2 = [[0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1]]

class Motor(object):
    def __init__(self, pins, mode=3):
        """Initialise the motor object.

        pins -- a list of 4 integers referring to the GPIO pins that the IN1, IN2
                IN3 and IN4 pins of the ULN2003 board are wired to
        mode -- the stepping mode to use:
                1: wave drive (not yet implemented)
                2: full step drive
                3: half step drive (default)

        """
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.mode = mode
        self.deg_per_step = 5.625 / 64  # for half-step drive (mode 3)
        self.steps_per_rev = int(360 / self.deg_per_step)  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

    def _set_rpm(self, rpm):
        """Set the turn speed in RPM."""
        self._rpm = rpm
        # T is the amount of time to stop between signals
        self._T = (60.0 / rpm) / self.steps_per_rev

    # This means you can set "rpm" as if it is an attribute and
    # behind the scenes it sets the _T attribute
    rpm = property(lambda self: self._rpm, _set_rpm)

    def move_to(self, angle):
        """Take the shortest route to a particular angle (degrees)."""
        # Make sure there is a 1:1 mapping between angle and stepper angle
        target_step_angle = 8 * (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle - self.step_angle
        steps = (steps % self.steps_per_rev)
        if steps > self.steps_per_rev / 2:
            steps -= self.steps_per_rev
            #print "moving " + `steps` + " steps"
            if self.mode == 2:
                self._move_acw_2(-steps / 8)
            else:
                self._move_acw_3(-steps / 8)
        else:
            #print "moving " + `steps` + " steps"
            if self.mode == 2:
                self._move_cw_2(steps / 8)
            else:
                self._move_cw_3(steps / 8)
        self.step_angle = target_step_angle

    def __clear(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    def _move_acw_2(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            GPIO.output(self.P1, 1)
            sleep(self._T * 2)
            GPIO.output(self.P2, 0)
            GPIO.output(self.P4, 1)
            sleep(self._T * 2)
            GPIO.output(self.P1, 0)
            GPIO.output(self.P3, 1)
            sleep(self._T * 2)
            GPIO.output(self.P4, 0)
            GPIO.output(self.P2, 1)
            sleep(self._T * 2)

    def _move_cw_2(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P4, 0)
            GPIO.output(self.P2, 1)
            sleep(self._T * 2)
            GPIO.output(self.P1, 0)
            GPIO.output(self.P3, 1)
            sleep(self._T * 2)
            GPIO.output(self.P2, 0)
            GPIO.output(self.P4, 1)
            sleep(self._T * 2)
            GPIO.output(self.P3, 0)
            GPIO.output(self.P1, 1)
            sleep(self._T * 2)

    def _move_acw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)

    def _move_cw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)

    def turn(self, rev):
        self._move_cw(rev * self.steps_per_rev / 8)

def rotate1(motorp,dir):

    m = Motor(motorp)
    m.rpm = 5
    if dir==1:
         for i in range(2):
             m.move_to(90)
             sleep(.01)
             m.move_to(180)
             sleep(.01)
             m.mode = 2
             m.move_to(360)
             sleep(.01)
             m.move_to(0.01)
     #m.turn(2)
    elif dir==2:
        for i in range(2):
            m.move_to(-90)
            sleep(.01)
            m.move_to(180)
            sleep(.01)
            m.mode = 2
            m.move_to(90)
            sleep(.01)
            m.move_to(0)
            sleep(.01)
            m.move_to(0)

def rotate2(ControlPin,dir):


    for p in ControlPin:
        wiringpi2.pinMode(p, 1)

    if dir == 1:
        seq = seq1
    elif dir == 2:
        seq = seq2

    for j in range(5):
        for i in range(128):
            for hs in range(8):
                for pin in range(4):
                   wiringpi2.digitalWrite(ControlPin[pin], seq[hs][pin])
            time.sleep(0.00020)


if __name__ == "__main__":

    #print "Pause in seconds: " + `m._T`
    #FOR MOTORS 1-3  (use second argument 1 for left and 2 for right)
    #execfile("lightsensorfinal.py")
    p1 = Process(target=rotate1,args=(motor1,2))
    p1.start()
    p2 = Process(target=rotate1, args=(motor2, 2))
    p2.start()
    p3=Process(target=rotate1, args=(motor3, 2))
    p3.start()
    p4 = Process(target=rotate1, args=(motor4, 2))
    p4.start()
    p5 = Process(target=rotate1, args=(motor5, 2))
    p5.start()
    p6 = Process(target=rotate1, args=(motor6, 2))
    p6.start()
    p7 = Process(target=rotate1, args=(motor7, 2))
    p7.start()
    #rotate1(motor2,1)
    #rotate1(motor3,1)
    #rotate2(motor4,1)
    #rotate2(motor5, 1)
    #rotate2(motor6, 1)
    #rotate2(motor7, 1)
    GPIO.cleanup()
