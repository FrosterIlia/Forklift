import pigpio
import time
from controller import *
import threading


MOTOR_LEFT_SPEED_PIN = 17
MOTOR_LEFT_A_PIN = 22
MOTOR_LEFT_B_PIN = 27

STBY_PIN = 18

MOTOR_RIGHT_SPEED_PIN = 11
MOTOR_RIGHT_A_PIN = 10
MOTOR_RIGHT_B_PIN = 9

SERVO_PIN = 12
SERVO_ANGLE_UP = 0
SERVO_ANGLE_DOWN = 30

DEAD_ZONE = 0.5
MAX_PWM = 150

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def drive_motor(pi, pin_a, pin_b, value):
    if value > DEAD_ZONE:
        speed = map(value, 0, 1, DEAD_ZONE, MAX_PWM) 
        
        pi.set_PWM_dutycycle(pin_a, speed)
        pi.write(pin_b, 0)
        
    elif value < -DEAD_ZONE:
        speed = map(abs(value), 0, 1, DEAD_ZONE, MAX_PWM) 
        pi.set_PWM_dutycycle(pin_b, speed)
        pi.write(pin_a, 0)
        
    else:
        pi.write(pin_a, 0)
        pi.write(pin_b, 0)
        
        
def set_servo_angle(pi, angle):
    # MG90 pulse range: 500us - 2500us
    pulse_width = int(map(angle, 0, 180, 500, 2500))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

def main():

    pi = pigpio.pi()

    pi.set_mode(MOTOR_LEFT_SPEED_PIN, pigpio.OUTPUT)
    pi.set_mode(MOTOR_LEFT_A_PIN, pigpio.OUTPUT)
    pi.set_mode(MOTOR_LEFT_B_PIN, pigpio.OUTPUT)

    pi.set_mode(STBY_PIN, pigpio.OUTPUT)

    pi.set_mode(MOTOR_RIGHT_SPEED_PIN, pigpio.OUTPUT)
    pi.set_mode(MOTOR_RIGHT_A_PIN, pigpio.OUTPUT)
    pi.set_mode(MOTOR_RIGHT_B_PIN, pigpio.OUTPUT)

    print("configured pins")

    pi.write(STBY_PIN, 1)
    pi.write(MOTOR_LEFT_SPEED_PIN, 1)
    pi.write(MOTOR_RIGHT_SPEED_PIN, 1)

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    # controller.listen()
    t = threading.Thread(target = controller.listen, daemon = True)
    t.start()

    while True:
        
        left_stick_x = controller.R3_x / 32767
        left_stick_y = controller.R3_y / 32767
        
        left = left_stick_y + left_stick_x
        right = left_stick_y - left_stick_x
        
        max_value = max(abs(left), abs(right), 1)
        
        left = left / max_value
        right = right / max_value
        
        drive_motor(pi, MOTOR_LEFT_A_PIN, MOTOR_LEFT_B_PIN, left)
        drive_motor(pi, MOTOR_RIGHT_A_PIN, MOTOR_RIGHT_B_PIN, right)
        
        if controller.circle:
            set_servo_angle(pi, SERVO_ANGLE_UP)
            
        if controller.square:
            set_servo_angle(pi, SERVO_ANGLE_DOWN)
            
        if controller.up:
            pi.write(MOTOR_LEFT_A_PIN, 0)
            pi.write(MOTOR_LEFT_B_PIN, 1)
            pi.write(MOTOR_RIGHT_A_PIN, 0)
            pi.write(MOTOR_RIGHT_B_PIN, 1)

        elif controller.down:
            pi.write(MOTOR_LEFT_A_PIN, 1)
            pi.write(MOTOR_LEFT_B_PIN, 0)
            pi.write(MOTOR_RIGHT_A_PIN, 1)
            pi.write(MOTOR_RIGHT_B_PIN, 0)

        elif controller.left:
            pi.write(MOTOR_LEFT_A_PIN, 1)
            pi.write(MOTOR_LEFT_B_PIN, 0)
            pi.write(MOTOR_RIGHT_A_PIN, 0)
            pi.write(MOTOR_RIGHT_B_PIN, 1)

        elif controller.right:
            pi.write(MOTOR_LEFT_A_PIN, 0)
            pi.write(MOTOR_LEFT_B_PIN, 1)
            pi.write(MOTOR_RIGHT_A_PIN, 1)
            pi.write(MOTOR_RIGHT_B_PIN, 0)

        else:
            pi.write(MOTOR_LEFT_A_PIN, 0)
            pi.write(MOTOR_LEFT_B_PIN, 0)
            pi.write(MOTOR_RIGHT_A_PIN, 0)
            pi.write(MOTOR_RIGHT_B_PIN, 0)

    pi.stop()

if __name__ == "__main__":
    main()