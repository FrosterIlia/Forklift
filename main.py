# Title: main.py
# Author: Kris Hubler (Updated with Sequence Framework)
# Date: May 6, 2026
# Description: Tele-operated Raspberry Pi Forklift

import time
import pigpio
from stepper import Stepper
from Servo import Servo

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
FR_STEP, FR_DIR = 7, 8 # motor 3
RL_STEP, RL_DIR = 27, 17 # motor 1
RR_STEP, RR_DIR = 24, 23 # motor 4

EN_PINS = [4, 10, 5, 18, 25]

SERVO_RIGHT_PIN = 20
SERVO_RIGHT_ANGLE_UP = 70
SERVO_LEFT_ANGLE_DOWN = 45

#-------------------------------
# CREATE MOTORS
#-------------------------------
FL = Stepper(FL_STEP, FL_DIR, pi)
FR = Stepper(FR_STEP, FR_DIR, pi, 1)
RL = Stepper(RL_STEP, RL_DIR, pi)
RR = Stepper(RR_STEP, RR_DIR, pi, 1)

servo_1 = Servo(15, 30, 0, pi)
servo_2 = Servo(14, 30, 0, pi)
servo_3 = Servo(12, 30, 0, pi)
servo_4 = Servo(19, 30, 0, pi)

motors = [FL, FR, RL, RR]

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_left_servo_angle(angle):
    # MG90 pulse range: 500us - 2500us
    pulse_width = int(map(angle, 0, 180, 500, 2500))
    pi.set_servo_pulsewidth(SERVO_RIGHT_PIN, pulse_width)
    
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
        if action != stop and action != set_left_servo_angle:
            start_all()
        
        time.sleep(duration) 
            
        stop_all()

# Define your routine here! 
ROBOT_SEQUENCE = [
    (forward, 4.0, 1500),
    (stop, 1.0, 0), 
    (move_right, 1.5, 1500),  
    (stop, 1.0, 0),   
    (forward, 1.0, 1500) ,
    (stop, 1.0, 0), 
    (set_left_servo_angle, 1.0, SERVO_RIGHT_ANGLE_UP),
    (stop, 1.0, 0), 
    (backward, 1.0, 1000),
    (stop, 1.0, 0), 
    (turn_right, 6.0, 500), 
    (stop, 1.0, 0), 
    (set_left_servo_angle, 1.0, SERVO_LEFT_ANGLE_DOWN),
    (stop, 1.0, 0), 
    (forward, 5.5, 1500),
    (stop, 1.0, 0), 
    (backward, 3.0, 1000)
    # (move_left, 0.2, 1000)
    
    # (set_left_servo_angle, 1.0, SERVO_LEFT_ANGLE_DOWN)
]

#------------------------------
# MAIN LOOP
#-----------------------------
if __name__ == "__main__":
    try:
        for i in EN_PINS:
            pi.set_mode(i, pigpio.OUTPUT)
            pi.write(i, 0)
        print("Starting sequence...")
        # run_sequence(ROBOT_SEQUENCE)
        # RR.move()
        # start_all()
        
        servo_1.move_up()
        servo_2.move_up()
        servo_3.move_up()
        servo_4.move_up()
        time.sleep(2)
        servo_4.move_down()
        servo_1.move_down()
        servo_2.move_down()
        servo_3.move_down()
        print("Sequence complete!")
        while True:
            pass

    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")

    finally:
        stop_all()
        pi.stop()