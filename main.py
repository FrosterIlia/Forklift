# Title: main.py
# Author: Kris Hubler (Updated with Sequence Framework)
# Date: May 2, 2026
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
#-------------------------------
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

def stop(speed=0):
    """Added so you can program pauses into the sequence easily."""
    stop_all()

#------------------------------
# SEQUENCE FRAMEWORK
#-----------------------------
def run_sequence(sequence):
    """
    Executes a list of hardcoded movements.
    Keeps tick_all() running so the stepper motors don't stall.
    """
    for step_num, (action, duration, speed) in enumerate(sequence, 1):
        print(f"Step {step_num}: {action.__name__} for {duration}s at speed {speed}")
        
        # Initiate the movement
        action(speed)
        if action != stop:
            start_all()
        
        # Track time while continuously ticking the motors
        start_time = time.time()
        while (time.time() - start_time) < duration:
            tick_all()
            
        # Stop the robot briefly before the next move
        stop_all()


# Define your routine here! 
# Format: (movement_function, duration_in_seconds, speed)
ROBOT_SEQUENCE = [
    (forward, 2.0, 300),      # Move forward for 2 seconds at 300 speed
    (move_left, 3.0, 500),    # Strafe left for 3 seconds at 500 speed
    (stop, 1.0, 0),           # Pause for 1 second
    (backward, 1.5, 300),     # Move backward for 1.5 seconds at 300 speed
    (turn_right, 2.0, 400),   # Spin right for 2 seconds at 400 speed
    (stop, 0.5, 0)            # Final stop
]

#------------------------------
# MAIN LOOP
#-----------------------------
if __name__ == "__main__":
    try:
        print("Starting sequence...")
        
        # Run the hardcoded sequence
        run_sequence(ROBOT_SEQUENCE)
        
        print("Sequence complete!")

    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")

    finally:
        stop_all()
        pi.stop()