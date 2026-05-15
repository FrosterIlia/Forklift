# Title: main.py
# Author: Kris Hubler (Updated with Sequence Framework)
# Date: May 6, 2026
# Description: Tele-operated Raspberry Pi Forklift

import time
import pigpio
import cv2

from network_camera import NetworkCamera
from stepper import Stepper
from Servo import Servo

IP = '192.168.0.100'
PORT = 4015

# Connect to pigpio with some error checking
pi = pigpio.pi()

top_camera = NetworkCamera(IP, PORT)
center_camera = NetworkCamera(IP, 5015)


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
        
        print("Sequence complete!")
        while True:
            frame_top = top_camera.receive_frame("Top")
            if frame_top is not None:
                cv2.imshow('Overhead Camera', frame_top)
                
            frame_center = center_camera.receive_frame("Center")
            if frame_center is not None:
                cv2.imshow('Center Camera', frame_center)
                
                
            if cv2.waitKey(5) & 0xFF == ord('q'):
                    print("Exiting camera view...")
                    break


    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")

    finally:
        stop_all()
        pi.stop()
        cv2.destroyAllWindows()