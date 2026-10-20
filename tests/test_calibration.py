import math
from app.pipeline.calibration import build_homography, pixel_to_world, COURT_LENGTH_M, COURT_WIDTH_M

def test_corners_map_back_correctly():
    # Replace these with YOUR actual clicked pixel points from Step 1
    pixel_corners = [
        (5, 1001),   # near-left
        (1919, 999),  # near-right
        (1265, 716),   # far-right
        (647, 703),   # far-left
    ]
    h = build_homography(pixel_corners)

    # The near-left corner should map close to real-world (0, 0)
    x, y = pixel_to_world(pixel_corners[0], h)
    assert math.isclose(x, 0, abs_tol=0.3)
    assert math.isclose(y, 0, abs_tol=0.3)

    # The far-right corner should map close to (COURT_WIDTH_M, COURT_LENGTH_M)
    x, y = pixel_to_world(pixel_corners[2], h)
    assert math.isclose(x, COURT_WIDTH_M, abs_tol=0.3)
    assert math.isclose(y, COURT_LENGTH_M, abs_tol=0.3)

