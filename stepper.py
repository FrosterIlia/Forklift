# Title: stepper.py 
# Author: IM/KH (Hardware PWM Version)
# Date: May 6, 2026

import time
import pigpio

class Stepper:
    def __init__(self, step_pin, dir_pin, pi, inverted=0):
        self._step_pin = step_pin
        self._dir_pin = dir_pin
        self.inverted = inverted
        
        # connect to pigpio daemon
        self.pi = pi
        if not self.pi.connected:
            raise RuntimeError("Could not connect to pigpio daemon. Run 'sudo pigpiod'.")
        
        self.pi.set_mode(self._step_pin, pigpio.OUTPUT)
        self.pi.set_mode(self._dir_pin, pigpio.OUTPUT)

        self._dir = 0
        self._moving = False
        self._steps_per_second = 0
        
        # Initialize pins
        self.pi.write(self._step_pin, 0)
        self.pi.write(self._dir_pin, self._dir)
        
    def set_dir(self, direction):
        if self.inverted:
            new_dir = 0 if direction else 1
        else:
            new_dir = 1 if direction else 0
            
        if self._dir != new_dir:
            self._dir = new_dir
            self.pi.write(self._dir_pin, self._dir)

    def set_steps_per_second(self, value):
        self._steps_per_second = int(value)
        # If we are currently moving, update the hardware frequency immediately
        if self._moving:
            self.pi.set_PWM_frequency(self._step_pin, self._steps_per_second)

    def get_steps_per_second(self): 
        return self._steps_per_second

    def move(self):
        if self._steps_per_second > 0:
            self._moving = True
            # Set frequency (Steps per second)
            self.pi.set_PWM_frequency(self._step_pin, self._steps_per_second)
            # Set duty cycle to 128 (50% out of 255) to start the square wave
            self.pi.set_PWM_dutycycle(self._step_pin, 128)
    
    def stop(self):
        self._moving = False
        # Set duty cycle to 0 to stop the pulses
        self.pi.set_PWM_dutycycle(self._step_pin, 0)

    def is_moving(self):
        return self._moving
        
    # NOTE: The tick() function and SimpleTimer are completely gone!