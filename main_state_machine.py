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
from StateMachine import *



class MainStateMachine(HierarchicalStateMachine):
    def __init__(self, pi):
        super().__init__()
        
        # --- Hardware & Controller Initialization ---
        self.pi = pi
        
        self.top_camera = NetworkCamera(IP, PORT_1)
        self.center_camera = NetworkCamera(IP, PORT_2)

        self.cap = cv2.VideoCapture(0)
        
        self.servo_1 = Servo(SERVO_1_PIN, SERVO_UP_POSITION, SERVO_DOWN_POSITION, pi)
        self.servo_2 = Servo(SERVO_2_PIN, SERVO_UP_POSITION, SERVO_DOWN_POSITION, pi)
        self.servo_3 = Servo(SERVO_3_PIN, SERVO_UP_POSITION, SERVO_DOWN_POSITION, pi)
        self.servo_4 = Servo(SERVO_4_PIN, SERVO_UP_POSITION, SERVO_DOWN_POSITION, pi)
        
        self.drive_controller = MecanumDrive(pi, MECANUM_LX, MECANUM_LY)
        self.pos_estimator = PositioinEstimator(FORKLIFT_ARUCO_ID)
        self.position_controller = PositionController()

        # --- State Instantiation ---
        self.init_state = InitState(self)
        self.get_out_state = GetOutState(self)
        self.delivery_state = DeliveryState(self)
        self.scan_state = ScanState(self)
        self.aim_state = AimState(self)
        self.engage_payload_state = EngagePayloadState(self)
        self.grab_state = GrabState(self)
        self.turn_around_state = TurnAroundState(self)
        self.navigate_to_bay_state = NavigateToBayState(self)
        self.dock_and_drop_state = DockAndDropState(self)
        self.evacuate_state = EvacuateState(self)
        self.run_away_state = RunAwayState(self)
        self.debug_state = DebugState(self)

        # --- Hierarchy Wiring ---
        # Delivery branch
        self.scan_state.set_parent(self.delivery_state)
        self.aim_state.set_parent(self.delivery_state)
        self.engage_payload_state.set_parent(self.delivery_state)
        self.grab_state.set_parent(self.delivery_state)
        self.turn_around_state.set_parent(self.delivery_state)
        self.navigate_to_bay_state.set_parent(self.delivery_state)
        self.dock_and_drop_state.set_parent(self.delivery_state)

        # Evacuate branch
        self.run_away_state.set_parent(self.evacuate_state)

        # --- Default Substates ---
        self.delivery_state.set_default_sub_state(self.scan_state)

class InitState(State):
    def onEnter(self):
        print("Entered InitState")
        
        
    def onRun(self):
        print("init state running")


class GetOutState(State):
    def onEnter(self):
        print("Entered GetOutState")

    def onRun(self):
        print("get out state running")
        
class DeliveryState(State):
    def onEnter(self):
        print("Entered DeliveryState")

    def onRun(self):
        print("delivery state running")


class ScanState(State):
    def onEnter(self):
        print("Entered ScanState")

    def onRun(self):
        print("scan state running")


class AimState(State):
    def onEnter(self):
        print("Entered AimState")

    def onRun(self):
        print("aim state running")


class EngagePayloadState(State):
    def onEnter(self):
        print("Entered EngagePayloadState")

    def onRun(self):
        print("engage payload state running")


class GrabState(State):
    def onEnter(self):
        print("Entered GrabState")

    def onRun(self):
        print("grab state running")


class TurnAroundState(State):
    def onEnter(self):
        print("Entered TurnAroundState")

    def onRun(self):
        print("turn around state running")


class NavigateToBayState(State):
    def onEnter(self):
        print("Entered NavigateToBayState")

    def onRun(self):
        print("navigate to bay state running")


class DockAndDropState(State):
    def onEnter(self):
        print("Entered DockAndDropState")

    def onRun(self):
        print("dock and drop state running")
        
class EvacuateState(State):
    def onEnter(self):
        print("Entered EvacuateState")

    def onRun(self):
        print("evacuate state running")


class RunAwayState(State):
    def onEnter(self):
        print("Entered RunAwayState")

    def onRun(self):
        print("run away state running")
        
class DebugState(State):
    def onEnter(self):
        print("Entered DebugState")

    def onRun(self):
        frame_top = self._sm.top_camera.receive_frame("Top")
        if frame_top is not None:
            cv2.imshow('Overhead Camera', frame_top)
            state = self._sm.pos_estimator.estimate_pose(frame_top)
            if state:
                x, y, theta = state
                theta -= math.radians(90) # This is our 0, forks are pointed towards the wall with boxes
                current_position = Position(x, y, theta)
                target_position = Position(150, 300, math.radians(180))
                vels = self._sm.position_controller.get_local_velocities(current_position, target_position)
                print(f"y_vel: {vels[1]}, x_vel: {vels[0]}, theta_vel: {vels[2]}")
                # self._sm.drive_controller.set_velocities(vels[1], vels[0], vels[2])
                print(f"Robot Location: X: {x:.1f}mm, Y: {y:.1f}mm, Heading: {math.degrees(theta):.1f} degrees")
            else:
                print("Robot not detected.")
                
            # ret, frame = cap.read()
            
            # cv2.imshow('camera', frame)