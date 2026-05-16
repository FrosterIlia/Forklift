# Title: main.py
# Author: Kris Hubler (Updated with Sequence Framework)
# Date: May 6, 2026
# Description: Tele-operated Raspberry Pi Forklift

import time
import pigpio
import cv2
import math

from network_camera import NetworkCamera
from mecanum_drive import MecanumDrive
from Servo import Servo
from pos_estimator import PositioinEstimator
from homography_matrix_def import *
from constants import *
from position_controller import PositionController, Position
from main_state_machine import *

# Connect to pigpio with some error checking
pi = pigpio.pi()

if not pi.connected:
    print("Not connected to pigpio daemon! Run sudo systemctl start pigpiod")
    exit()

print("Connected to pigpio!")


main_sm = MainStateMachine(pi)


def main():
    try:
        main_sm.initialize(main_sm.debug_state)
        while True:
            main_sm.update()
                
            if cv2.waitKey(5) & 0xFF == ord('q'):
                print("Exiting camera view...")
                break


    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")
        main_sm.drive_controller.stop_all()
        pi.stop()
        cv2.destroyAllWindows()

    finally:
        pi.stop()
        main_sm.drive_controller.stop_all()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()