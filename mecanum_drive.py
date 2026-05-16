from stepper import Stepper
from constants import *

class MecanumDrive:
    def __init__(self, pi, Lx, Ly):
        self.vx = 0
        self.vy = 0
        self.w = 0
        
        self.Lx = Lx
        self.Ly = Ly
        
        self.pi = pi
        
        self.FL = Stepper(FL_STEP, FL_DIR, FL_EN, self.pi)
        self.RR = Stepper(FR_STEP, FR_DIR, FR_EN, self.pi, 1)
        self.RL = Stepper(RL_STEP, RL_DIR, RL_EN, self.pi)
        self.FR = Stepper(RR_STEP, RR_DIR, RR_EN, self.pi, 1)
        
        self.motors = [self.FL, self.FR, self.RL, self.RR]
        
        self.set_velocities(0, 0, 0)
        self.start_all()
        
        
        
    def get_wheel_velocities(self):
        w1 = self.vx - self.vy - self.w * (self.Lx + self.Ly)
        w2 = self.vx + self.vy + self.w * (self.Lx + self.Ly)
        w3 = self.vx + self.vy - self.w * (self.Lx + self.Ly)
        w4 = self.vx - self.vy + self.w * (self.Lx + self.Ly)
        
        return (w1, w3, w2, w4)
    
    def set_velocities(self, vx, vy, w):
        self.vx = vx
        self.vy = vy
        self.w = w
        
        vels = self.get_wheel_velocities()
        for motor, vel in zip(self.motors, vels):
            if vel < 0:
                motor.set_dir(0)
            else:
                motor.set_dir(1)
            if motor.get_steps_per_second() != abs(vel):
                motor.set_steps_per_second(abs(vel))
        self.start_all()
        # motor.enable()
    
    def start_all(self):
        for m in self.motors:
            m.move()

    def stop_all(self):
        for m in self.motors:
            m.stop()
            
  