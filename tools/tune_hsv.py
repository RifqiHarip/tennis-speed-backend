import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import numpy as np


def nothing(x):
    pass


def main(video_path: str):
    cap = cv2.VideoCapture(video_path)
    ok, frame = cap.read()
    if not ok:
        print("Could not read video")
        return

    cv2.namedWindow("mask")
    cv2.createTrackbar("H min", "mask", 25, 179, nothing)
    cv2.createTrackbar("H max", "mask", 65, 179, nothing)
    cv2.createTrackbar("S min", "mask", 70, 255, nothing)
    cv2.createTrackbar("S max", "mask", 255, 255, nothing)
    cv2.createTrackbar("V min", "mask", 70, 255, nothing)
    cv2.createTrackbar("V max", "mask", 255, 255, nothing)

    while True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([
            cv2.getTrackbarPos("H min", "mask"),
            cv2.getTrackbarPos("S min", "mask"),
            cv2.getTrackbarPos("V min", "mask"),
        ])
        upper = np.array([
            cv2.getTrackbarPos("H max", "mask"),
            cv2.getTrackbarPos("S max", "mask"),
            cv2.getTrackbarPos("V max", "mask"),
        ])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)
        cv2.imshow("result", result)

        key = cv2.waitKey(50) & 0xFF
        if key == ord("q"):
            break
        if key == ord("n"):
            ok, new_frame = cap.read()
            if ok:
                frame = new_frame

    print(f"\nFinal range: LOWER = [{lower[0]}, {lower[1]}, {lower[2]}]  "
          f"UPPER = [{upper[0]}, {upper[1]}, {upper[2]}]")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv[1])