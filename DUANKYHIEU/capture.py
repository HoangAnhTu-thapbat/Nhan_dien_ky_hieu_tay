import cv2

class CaptureManager:
    def __init__(self, camera_index=0, frame_width=224, frame_height=224, fps=15):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        self.running = False

    def start(self):
        if not self.cap.isOpened():
            raise RuntimeError("Không mở được webcam.")
        self.running = True

    def stop(self):
        self.running = False

    def read_frame(self):
        if not self.running:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()
