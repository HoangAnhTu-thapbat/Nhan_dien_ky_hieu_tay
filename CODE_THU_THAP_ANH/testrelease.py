import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không thể mở webcam")
else:
    print("Webcam mở thành công")
    cap.release()
