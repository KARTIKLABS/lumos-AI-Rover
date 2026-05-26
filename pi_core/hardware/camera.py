import cv2
import threading
import logging

class CameraManager:
    def __init__(self, config: dict):
        self.index = config.get("index", 0)
        self.width = config.get("width", 640)
        self.height = config.get("height", 480)
        self.fps = config.get("fps", 30)
        
        self.cap = None
        self.current_frame = None
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def start(self):
        self.cap = cv2.VideoCapture(self.index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        if not self.cap.isOpened():
            logging.error(f"Failed to open camera index {self.index}")
            return False
            
        self._running = True
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        return True

    def _update_loop(self):
        while self._running:
            ret, frame = self.cap.read()
            if ret:
                with self._lock:
                    self.current_frame = frame

    def get_frame(self):
        with self._lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
            return None

    def stop(self):
        self._running = False
        if self.cap:
            self.cap.release()
