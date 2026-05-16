import numpy as np
import cv2


def get_homography_matrix():
    # 1. Define your real-world arena corners (in mm) 
    # Example: A 2000mm x 1500mm warehouse grid
    # Format: [Bottom-Left, Bottom-Right, Top-Right, Top-Left]
    real_world_pts = np.array([
        [0, 0],           
        [1300, 0],        
        [1300, 1100],     
        [0, 1100]         
    ], dtype=np.float32)

    # 2. Define where those exact same corners appear in your camera's PIXELS
    # You only need to measure these pixel coordinates once during calibration
    camera_pixel_pts = np.array([
        [27, 581],   # Bottom-Left pixel
        [583, 576],  # Bottom-Right pixel
        [585, 27],  # Top-Right pixel
        [29, 23]    # Top-Left pixel
    ], dtype=np.float32)

    # 3. Calculate the transform matrix
    homography_matrix, _ = cv2.findHomography(camera_pixel_pts, real_world_pts)
    return homography_matrix