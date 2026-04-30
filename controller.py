from pyPS4Controller.controller import Controller

class MyController(Controller):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Joysticks: -32767 to 32767
        self.L3_x = 0
        self.L3_y = 0
        self.R3_x = 0
        self.R3_y = 0
        # Triggers: 0 to 32767
        self.L2 = 0
        self.R2 = 0
        # Buttons: bool
        self.x       = False
        self.circle  = False
        self.triangle = False
        self.square  = False
        
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    # --- Left stick ---
    def on_L3_up(self, value):
        self.L3_y = value  # negative = up, flip if you want up = positive

    def on_L3_down(self, value):
        self.L3_y = value

    def on_L3_left(self, value):
        self.L3_x = value

    def on_L3_right(self, value):
        self.L3_x = value

    # --- Right stick ---
    def on_R3_up(self, value):
        self.R3_y = value

    def on_R3_down(self, value):
        self.R3_y = value

    def on_R3_left(self, value):
        self.R3_x = value

    def on_R3_right(self, value):
        self.R3_x = value

    # --- Triggers ---
    def on_L2_press(self, value):
        self.L2 = value

    def on_L2_release(self):
        self.L2 = 0

    def on_R2_press(self, value):
        self.R2 = value

    def on_R2_release(self):
        self.R2 = 0

    # --- Buttons ---
    def on_x_press(self):
        self.x = True

    def on_x_release(self):
        self.x = False

    def on_circle_press(self):
        self.circle = True

    def on_circle_release(self):
        self.circle = False

    def on_triangle_press(self):
        self.triangle = True

    def on_triangle_release(self):
        self.triangle = False

    def on_square_press(self):
        self.square = True

    def on_square_release(self):
        self.square = False
        
    def on_up_arrow_press(self):
        self.up = True

    def on_down_arrow_press(self):
        self.down = True
        
    def on_up_down_arrow_release(self):
        self.down = False
        self.up = False

    def on_left_arrow_press(self):
        self.left = True
        
    def on_left_right_arrow_release(self):
        self.left = False
        self.right = False

    def on_right_arrow_press(self):
        self.right = True
