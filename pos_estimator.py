import cv2
import numpy as np
import math

class PositioinEstimator:
    def __init__(self, marker_id, marker_dict=cv2.aruco.DICT_6X6_250, transform_matrix=None):
        """
        Initializes the PoseEstimator for the warehouse robot.
        
        Args:
            marker_id (int): The ArUco marker ID assigned to the forklift.
            marker_dict (int): The ArUco dictionary being used.
            transform_matrix (np.ndarray): A 3x3 Homography matrix to convert 
                                           camera pixels to real-world millimeters.
        """
        self.robot_marker_id = marker_id
        self.transform_matrix = transform_matrix
        
        # Setup modern OpenCV ArUco detector (OpenCV 4.7+)
        self.dictionary = cv2.aruco.getPredefinedDictionary(marker_dict)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

    def estimate_pose(self, frame):
        """
        Detects the robot and calculates its state (x, y, theta).
        
        Args:
            frame (np.ndarray): Raw overhead camera frame.
            
        Returns:
            tuple: (x, y, theta) where x, y are in real-world mm and 
                   theta is the heading angle in radians. 
                   Returns None if the robot is not found.
        """
        # 1. Detect the ArUco marker
        corners, ids, rejected = self.detector.detectMarkers(frame)

        if ids is not None and self.robot_marker_id in ids:
            # 2. Extract the specific marker for our robot
            idx = np.where(ids == self.robot_marker_id)[0][0]
            marker_corners = corners[idx][0]  # Shape: (4, 2)

            # ArUco corner ordering: 0: Top-Left, 1: Top-Right, 2: Bottom-Right, 3: Bottom-Left
            # 3. Calculate Center Point (in pixels)
            center_x_px = np.mean(marker_corners[:, 0])
            center_y_px = np.mean(marker_corners[:, 1])

            # 4. Determine Heading (Theta)
            # The "front" of the marker is the midpoint between Top-Left (0) and Top-Right (1)
            front_mid_x = (marker_corners[0][0] + marker_corners[1][0]) / 2.0
            front_mid_y = (marker_corners[0][1] + marker_corners[1][1]) / 2.0

            # Calculate direction vector
            dx = front_mid_x - center_x_px
            # In image coordinates, Y goes down. We invert dy to match standard Cartesian math.
            dy = center_y_px - front_mid_y 
            theta = math.atan2(dy, dx)

            # 5. Transform to Real-World Coordinates (mm)
            if self.transform_matrix is not None:
                # Reshape for perspectiveTransform: needs shape (1, 1, 2)
                point_px = np.array([[[center_x_px, center_y_px]]], dtype=np.float32)
                point_mm = cv2.perspectiveTransform(point_px, self.transform_matrix)
                
                real_x = point_mm[0][0][0]
                real_y = point_mm[0][0][1]
            else:
                # Fallback: return pixel coordinates if no matrix is provided
                real_x, real_y = center_x_px, center_y_px

            return (real_x, real_y, theta)

        # Robot marker not visible in this frame
        return None