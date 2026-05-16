import time

class PID:
    def __init__(self, kp, ki, kd, setpoint = 0, inverted = 0, i_min = -170, i_max = 170):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.input = 0
        self.output = 0

        self.I = 0
        
        # Adjustable integral windup limits
        self.i_min = i_min
        self.i_max = i_max

        self.prev_time = time.time()
        self.prev_error = 0
        self.error = 0
        
        self.inverted = inverted


    def compute(self):  
        current_time = time.time()
        dt = current_time - self.prev_time
        
        # Prevent divide-by-zero if the loop runs instantly
        if dt <= 0.0:
            dt = 0.001 

        error = (self.setpoint - self.input)
        
        if self.inverted:
            error = -error # Apply to the local variable!

        self.I = self.I + (error * self.ki * dt) 
        
        # Apply the adjustable limits
        self.I = max(min(self.I, self.i_max), self.i_min)
        
        D = (error - self.prev_error) / dt

        self.output = (error * self.kp) + self.I + (D * self.kd) 
        
        self.prev_error = error # Store local error for next time
        self.prev_time = current_time

    def get_output(self):
        return self.output
    
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_input(self, input):
        self.input = input

    def set_i_limits(self, i_min, i_max):
        self.i_min = i_min
        self.i_max = i_max