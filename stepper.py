# Title: stepper.py 
# Author: IM/KH
# Date: May 6, 2026
# Description:

import time
import pigpio

class SimpleTimer:
    def __init__(self):
        self.period = 0.0
        self.last_time = time.time()

    def set_period(self, period_us):
        self.period = period_us / 1_000_000.0 # converts us to s
    
    def is_ready(self):
        now = time.time()
        if now - self.last_time >= self.period:
            self.last_time = now
            return True
        return False

class Stepper:
    def __init__(self, step_pin, dir_pin, pi, inverted = 0):
        self._step_pin = step_pin
        self._dir_pin = dir_pin
        
        self.inverted = inverted
        
        # connect to pigpio daemon
        self.pi = pi
        if not self.pi.connected:
            raise RuntimeError("Could not connect to pigpio daemon. Run 'sudo pigpoid'.")
        
        self.pi.set_mode(self._step_pin, pigpio.OUTPUT)
        self.pi.set_mode(self._dir_pin, pigpio.OUTPUT)

        self._dir = 0
        self._moving = False
        self._step_high = False
        self._steps_per_second = 0

        self._main_timer = SimpleTimer()

        
        
    def set_dir(self, direction):
        if self.inverted:
            self._dir = 0 if direction else 1
        else:
            self._dir = 1 if direction else 0

    def move(self):
        self._moving = True
    
    def stop(self):
        self._moving = False
        self._step_high = False
        self.pi.write(self._step_pin, 0)

    def get_steps_per_second(self, value):
        return self._steps_per_second
    
    def set_steps_per_second(self, value):
        self._steps_per_second = value

    def is_moving(self):
        return self._moving
    
    def tick(self):
        # Set direction pin
        self.pi.write(self._dir_pin, self._dir)
        
        sps = self._steps_per_second if self._steps_per_second else 1
        half_period_us = 500000 // sps
        if half_period_us == 0:
            half_period_us = 1

        self._main_timer.set_period(half_period_us)

        if self._main_timer.is_ready() and self._moving:
            self._step_high = not self._step_high
            self.pi.write(self._step_pin, int(self._step_high))



