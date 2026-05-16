import math
import time
from pid import PID

class Position:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

class PositionController:
    def __init__(self):
        self.x_pid = PID(4.5, 0.35, 0, inverted=True)
        self.y_pid = PID(7, 1, 0, inverted=True)
        
        self.angle_pid = PID(250, 0, 0, i_min=-50, i_max=50) 
        
        self.last_run_time = time.time()
        self.min_dt = 0.05  
        self.last_velocities = (0.0, 0.0, 0.0) 
        
    def get_local_velocities(self, current_pos, target_pos):
        current_time = time.time()
        dt = current_time - self.last_run_time
        
        if dt < self.min_dt:
            return self.last_velocities
            
        self.last_run_time = current_time
        
        self.x_pid.set_input(current_pos.x)
        self.y_pid.set_input(current_pos.y)
        
        self.x_pid.set_setpoint(target_pos.x)
        self.y_pid.set_setpoint(target_pos.y)
        
        self.x_pid.compute()
        self.y_pid.compute()
        
        vx_global = self.x_pid.get_output()
        vy_global = self.y_pid.get_output()
        
        # Calculate raw error
        raw_error_angle = target_pos.angle - current_pos.angle
        
        # Wrap error to strictly [-pi, pi]
        wrapped_error_angle = math.atan2(math.sin(raw_error_angle), math.cos(raw_error_angle))
        
        # Trick the PID by passing the wrapped error as the setpoint and 0 as input
        self.angle_pid.set_setpoint(wrapped_error_angle)
        self.angle_pid.set_input(0)
        
        self.angle_pid.compute()
        
        v_theta = self.angle_pid.get_output() 
        
        theta = current_pos.angle
        
        vx_local = (vx_global * math.cos(theta)) + (vy_global * math.sin(theta))
        vy_local = (-vx_global * math.sin(theta)) + (vy_global * math.cos(theta))
        
        self.last_velocities = (vx_local, vy_local, v_theta)
        
        return (vx_local, vy_local, v_theta)