class Servo:
    def __init__(self, pin, angle_up, angle_down, pi):
        self.pin = pin
        self.angle_up = angle_up
        self.angle_down = angle_down
        self.pi = pi
        
    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def move_up(self):
        # MG90 pulse range: 500us - 2500us
        pulse_width = int(self.map(self.angle_up, 0, 180, 500, 2500))
        self.pi.set_servo_pulsewidth(self.pin, pulse_width)
        
    def move_down(self):
        # MG90 pulse range: 500us - 2500us
        pulse_width = int(self.map(self.angle_down, 0, 180, 500, 2500))
        self.pi.set_servo_pulsewidth(self.pin, pulse_width)