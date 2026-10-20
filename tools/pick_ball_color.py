import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import numpy as np

samples = []


def main(video_path: str):
    cap = cv2.VideoCapture(video_path)
    ok, frame = cap.read()
    if not ok:
        print("Could not read video")
        return

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def on_click(event, x, y, flags, param):
        nonlocal frame, hsv_frame
        if event == cv2.EVENT_LBUTTONDOWN:
            # average a small 5x5 patch around the click, not just one pixel
            patch = hsv_frame[max(0, y-2):y+3, max(0, x-2):x+3]
            h, s, v = patch.reshape(-1, 3).mean(axis=0)
            samples.append((h, s, v))
            print(f"Clicked ({x},{y}) -> HSV = ({h:.0f}, {s:.0f}, {v:.0f})")
            cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
            cv2.imshow("frame", frame)

    cv2.imshow("frame", frame)
    cv2.setMouseCallback("frame", on_click)
    print("Click on the ball several times across different frames (press 'n' for next frame).")
    print("Press 'q' when done.")

    while True:
        key = cv2.waitKey(50) & 0xFF
        if key == ord("q"):
            break
        if key == ord("n"):
            ok, new_frame = cap.read()
            if ok:
                frame = new_frame
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                cv2.imshow("frame", frame)

    cv2.destroyAllWindows()

    if not samples:
        print("No samples clicked.")
        return

    arr = np.array(samples)
    h_min, s_min, v_min = arr.min(axis=0)
    h_max, s_max, v_max = arr.max(axis=0)

    # pad the range a bit so you're not too strict
    pad_h, pad_sv = 6, 40
    print(f"\n--- Suggested range from {len(samples)} samples ---")
    print(f"LOWER_YELLOW = np.array([{max(0, h_min-pad_h):.0f}, {max(0, s_min-pad_sv):.0f}, {max(0, v_min-pad_sv):.0f}])")
    print(f"UPPER_YELLOW = np.array([{min(179, h_max+pad_h):.0f}, 255, 255])")


if __name__ == "__main__":
    main(sys.argv[1])