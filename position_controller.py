import math
from pid import PID

class Position:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

class PositionController:
    def __init__(self):
        self.x_pid = PID(1, 0, 0)
        self.y_pid = PID(1, 0, 0)
        self.angle_pid = PID(0.1, 0, 0)
        
    def get_local_velocities(self, current_pos, target_pos):
        error_x = target_pos.x - current_pos.x
        error_y = target_pos.y - current_pos.y
        
        # error_angle = target_pos.angle - current_pos.angle
        # error_angle = math.atan2(math.sin(error_angle), math.cos(error_angle))
        
        self.x_pid.set_input(current_pos.x)
        self.y_pid.set_input(current_pos.y)
        
        self.x_pid.set_setpoint(target_pos.x)
        self.y_pid.set_setpoint(target_pos.y)
        
        self.x_pid.compute()
        self.y_pid.compute()
        
        vx_global = self.x_pid.get_output()
        vy_global = self.y_pid.get_output()
        
        theta = current_pos.angle
        
        # Apply matrix transformation on the angle that the forklift is currently oriented
        vx_local = (vx_global * math.cos(theta)) + (vy_global * math.sin(theta))
        vy_local = (-vx_global * math.sin(theta)) + (vy_global * math.cos(theta))
        
        return (vx_local, vy_local)