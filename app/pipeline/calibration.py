import numpy as np
import cv2

COURT_LENGTH_M = 23.77
COURT_WIDTH_M = 10.97

WORLD_CORNERS = np.array([
    [0, 0],
    [COURT_WIDTH_M, 0],
    [COURT_WIDTH_M, COURT_LENGTH_M],
    [0, COURT_LENGTH_M],
], dtype=np.float32)


def build_homography(pixel_corners: list[tuple[float, float]]) -> np.ndarray:
    pixel_pts = np.array(pixel_corners, dtype=np.float32)
    homography, _ = cv2.findHomography(pixel_pts, WORLD_CORNERS)
    return homography


def pixel_to_world(point: tuple[float, float], homography: np.ndarray) -> tuple[float, float]:
    px = np.array([[point]], dtype=np.float32)
    world = cv2.perspectiveTransform(px, homography)
    x_m, y_m = world[0][0]
    return float(x_m), float(y_m)