# Title: main.py
# Author: Kris Hubler (Updated with Sequence Framework)
# Date: May 6, 2026
# Description: Tele-operated Raspberry Pi Forklift

import time
import pigpio
import cv2

from network_camera import NetworkCamera
from mecanum_drive import MecanumDrive
from Servo import Servo

IP = '192.168.0.100'
PORT = 4015

# Connect to pigpio with some error checking
pi = pigpio.pi()

top_camera = NetworkCamera(IP, PORT)
center_camera = NetworkCamera(IP, 5015)

cap = cv2.VideoCapture(0)

if not pi.connected:
    print("Not connected to pigpio daemon! Run sudo systemctl start pigpiod")
    exit()

print("Connected to pigpio!")

servo_1 = Servo(15, 30, 0, pi)
servo_2 = Servo(14, 30, 0, pi)
servo_3 = Servo(12, 30, 0, pi)
servo_4 = Servo(19, 30, 0, pi)

drive_controller = MecanumDrive(pi, 1, 1)


if __name__ == "__main__":
    try:
        drive_controller.set_velocities(500, 0, 0)
        # drive_controller.stop_all()
        print("Sequence complete!")
        while True:
            # frame_top = top_camera.receive_frame("Top")
            # if frame_top is not None:
            #     cv2.imshow('Overhead Camera', frame_top)
                
            # frame_center = center_camera.receive_frame("Center")
            # if frame_center is not None:
            #     cv2.imshow('Center Camera', frame_center)
                
            # ret, frame = cap.read()
            
            # cv2.imshow('camera', frame)
            
            
                
            if cv2.waitKey(5) & 0xFF == ord('q'):
                print("Exiting camera view...")
                break


    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")

    finally:
        pi.stop()
        drive_controller.stop_all()
        cv2.destroyAllWindows()