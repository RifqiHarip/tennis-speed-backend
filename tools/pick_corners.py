"""
Click the 4 court corners in order: near-left, near-right, far-right, far-left.
Prints the pixel coordinates of each click so you can copy them into calibration code.
"""
import cv2
import sys

def main(video_path: str):
    cap = cv2.VideoCapture(video_path)
    ok, frame = cap.read()
    if not ok:
        print("Could not read the video file.")
        return

    points = []

    def on_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            print(f"Point {len(points)}: ({x}, {y})")
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("frame", frame)

    cv2.imshow("frame", frame)
    cv2.setMouseCallback("frame", on_click)
    print("Click the 4 court corners in order: near-left, near-right, far-right, far-left.")
    print("Press any key once done.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("\nAll points:", points)

if __name__ == "__main__":
    main(sys.argv[1])