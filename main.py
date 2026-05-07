# Title: main.py
# Author: Kris Hubler (Updated with Sequence Framework)
# Date: May 6, 2026
# Description: Tele-operated Raspberry Pi Forklift

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

SERVO_PIN = 20
SERVO_ANGLE_UP = 0
SERVO_ANGLE_DOWN = 30

#-------------------------------
# CREATE MOTORS
#-------------------------------
FL = Stepper(FL_STEP, FL_DIR, pi, 1)
FR = Stepper(FR_STEP, FR_DIR, pi)
RL = Stepper(RL_STEP, RL_DIR, pi, 1)
RR = Stepper(RR_STEP, RR_DIR, pi)

motors = [FL, FR, RL, RR]   

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_servo_angle(angle):
    # MG90 pulse range: 500us - 2500us
    pulse_width = int(map(angle, 0, 180, 500, 2500))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

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
    FL.set_dir(1)
    FR.set_dir(0)
    RL.set_dir(0)
    RR.set_dir(1)

def move_left(speed=500):
    set_all_speeds(speed)
    FL.set_dir(0)
    FR.set_dir(1)
    RL.set_dir(1)
    RR.set_dir(0)

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

def stop(speed=0):
    stop_all()

#------------------------------
# SEQUENCE FRAMEWORK
#-----------------------------
def run_sequence(sequence):
    for step_num, (action, duration, speed) in enumerate(sequence, 1):
        print(f"Step {step_num}: {action.__name__} for {duration}s at speed {speed}")
        
        action(speed)
        if action != stop:
            start_all()
        
        time.sleep(duration) 
            
        stop_all()

# Define your routine here! 
ROBOT_SEQUENCE = [
    # (forward, 4.0, 1500),
    # (stop, 1.0, 0),    
    # (move_right, 2.0, 1500),    
    # (stop, 1.0, 0),     
    # (forward, 1.0, 1500) ,
    # (stop, 1.0, 0),
    # (turn_right, 4.0, 1000), 
    # (stop, 1.0, 0), 
    # (forward, 4.0, 1500),
    (set_servo_angle, 1.0, SERVO_ANGLE_UP),
    (set_servo_angle, 1.0, SERVO_ANGLE_DOWN)
]

#------------------------------
# MAIN LOOP
#-----------------------------
if __name__ == "__main__":
    try:
        print("Starting sequence...")
        run_sequence(ROBOT_SEQUENCE)
        print("Sequence complete!")

    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")

    finally:
        stop_all()
        pi.stop()