# Title: main.py
# Author: Kris Hubler
# Date: MAy 2, 2026
# Description: Tele-operated Raspberry Pi Forklift
#              Uses 4 - 17HS3401 Stepper Motors at 12V
#              Uses 4 - TMC2209 v1.3 Motor Drivers
#              Uses 1 - CNC Shield V3.0 
#              Uses 1 - Raspberry Pi 4 Model B 8GB

import time
import pigpio
from stepper import Stepper

# Connect to pigpio with some error checking
pi = pigpio.pi()

if not pi.connected:
    print("Not connected to pigpio daemon! Run sudo systemctl start pigpiod")
    exit()

print("Connected to pigpio!")

#-------------------------------
# PIN DEFINITIONS
#-------------------------------
FL_STEP, FL_DIR = 13, 6
FR_STEP, FR_DIR = 24, 23
RL_STEP, RL_DIR = 27, 17
RR_STEP, RR_DIR = 11, 9

#-------------------------------
# CREATE MOTORS
# #-------------------------------

FL = Stepper(FL_STEP, FL_DIR, pi, 1)
FR = Stepper(FR_STEP, FR_DIR, pi)
RL = Stepper(RL_STEP, RL_DIR, pi, 1)
RR = Stepper(RR_STEP, RR_DIR, pi)

motors = [FL, FR, RL, RR]   

#------------------------------
# HELPERS
#------------------------------

def set_all_speeds(speed):
    for m in motors:
        m.set_steps_per_second(speed)

def start_all():
    for m in motors:
        m.move()

def stop_all():
    for m in motors:
        m.stop()

def tick_all():
    for m in motors:
        m.tick()

#------------------------------
# MECANUM MOVEMENTS
#-----------------------------

def forward(speed=300):
    set_all_speeds(speed)
    FL.set_dir(1)
    FR.set_dir(1)
    RL.set_dir(1)
    RR.set_dir(1)

def backward(speed=300):
    set_all_speeds(speed)
    FL.set_dir(0)
    FR.set_dir(0)
    RL.set_dir(0)
    RR.set_dir(0)

def move_right(speed=500):
    set_all_speeds(speed)
    FL.set_dir(0)
    FR.set_dir(1)
    RL.set_dir(1)
    RR.set_dir(0)

def move_left(speed=500):
    set_all_speeds(speed)
    FL.set_dir(1)
    FR.set_dir(0)
    RL.set_dir(0)
    RR.set_dir(1)

def turn_right(speed=500):
    set_all_speeds(speed)
    FL.set_dir(1)
    FR.set_dir(0)
    RL.set_dir(1)
    RR.set_dir(0)

def turn_left(speed=500):
    set_all_speeds(speed)
    FL.set_dir(0)
    FR.set_dir(1)
    RL.set_dir(0)
    RR.set_dir(1)

#------------------------------
# DEMO LOOP
#-----------------------------
if __name__ == "__main__":
    try:
        
        while True:
            tick_all()
            turn_left()
            start_all()
            
            print("running")

    except KeyboardInterrupt:
        pass

    finally:
        stop_all()
        pi.stop()
