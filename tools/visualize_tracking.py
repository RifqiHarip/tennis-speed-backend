import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
from app.pipeline.tracking import track_ball

# Replace with YOUR real corner points from Step 3
PIXEL_CORNERS = [
    (5, 1001),   # near-left
    (1919, 999),  # near-right
    (1265, 716),   # far-right
    (647, 703),   # far-left
]


def main(video_path: str):
    detections = track_ball(video_path, pixel_corners=PIXEL_CORNERS)
    by_frame = {d["frame"]: d for d in detections}

    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_idx in by_frame:
            d = by_frame[frame_idx]
            cv2.circle(frame, (int(d["x"]), int(d["y"])), 8, (0, 0, 255), 2)
        cv2.imshow("tracking check", frame)
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break
        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Detected ball in {len(detections)} of {frame_idx} frames "
          f"({100 * len(detections) / frame_idx:.1f}%)")


if __name__ == "__main__":
    main(sys.argv[1])