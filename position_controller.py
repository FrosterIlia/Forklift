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
        self.x_pid = PID(4, 1, 0, inverted = True, i_min = -50, i_max = 50)
        self.y_pid = PID(4, 1, 0, inverted = True, i_min = -50, i_max = 50)
        self.angle_pid = PID(0.1, 0, 0)
        
        # --- Timing variables for PID throttling ---
        self.last_run_time = time.time()
        self.min_dt = 0.05  # Limit to 20Hz (50ms). Change to 0.033 for ~30Hz.
        self.last_velocities = (0.0, 0.0) # Fallback to prevent breaking main loop
        
    def get_local_velocities(self, current_pos, target_pos):
        current_time = time.time()
        dt = current_time - self.last_run_time
        
        if dt < self.min_dt:
            return self.last_velocities
            
        self.last_run_time = current_time
        
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
        
        # Save the freshly calculated velocities to use as the fallback next time
        self.last_velocities = (vx_local, vy_local)
        
        return (vx_local, vy_local)