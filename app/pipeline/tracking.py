import cv2
import numpy as np

LOWER_YELLOW = np.array([27, 90, 130])
UPPER_YELLOW = np.array([47, 255, 255])

MIN_RADIUS = 2
MAX_RADIUS = 25


def build_court_mask(frame_shape, pixel_corners: list[tuple[float, float]], margin_px: int = 40):
    h, w = frame_shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    pts = np.array(pixel_corners, dtype=np.int32)

    center = pts.mean(axis=0)
    expanded = []
    for p in pts:
        direction = p - center
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction = direction / norm
        expanded.append(p + direction * margin_px)
    expanded = np.array(expanded, dtype=np.int32)

    cv2.fillPoly(mask, [expanded], 255)
    return mask


def track_ball(video_path: str, pixel_corners: list[tuple[float, float]] | None = None) -> list[dict]:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=30, varThreshold=25, detectShadows=False
    )

    detections = []
    frame_idx = 0
    court_mask = None

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if pixel_corners is not None and court_mask is None:
            court_mask = build_court_mask(frame.shape, pixel_corners)

        # Motion
        fg_mask = bg_subtractor.apply(frame)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # Color
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)

        # Must satisfy BOTH: the right color AND currently moving
        combined = cv2.bitwise_and(fg_mask, color_mask)

        if court_mask is not None:
            combined = cv2.bitwise_and(combined, court_mask)

        contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best = None
        for c in contours:
            (x, y), radius = cv2.minEnclosingCircle(c)
            if MIN_RADIUS <= radius <= MAX_RADIUS:
                area = cv2.contourArea(c)
                circle_area = np.pi * radius * radius
                circularity = area / circle_area if circle_area > 0 else 0
                if best is None or circularity > best[2]:
                    best = (x, y, circularity)

        if best is not None:
            detections.append({
                "frame": frame_idx,
                "timestamp_sec": frame_idx / fps,
                "x": best[0],
                "y": best[1],
                "confidence": round(min(best[2], 1.0), 3),
            })

        frame_idx += 1

    cap.release()
    return detections