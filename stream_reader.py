import queue
import cv2


class StreamReader:
    def __init__(self, file_path, data_dst: queue.Queue, stop_signal):
        self.video_path = file_path.as_posix()
        self.cap = None
        self.dst_data_queue = data_dst
        self.stop_signal = stop_signal

    def start(self):
        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            raise ValueError("Can't open video file provided")

        while not self.stop_signal.is_set():
            ret, frame = self.cap.read()

            if not ret:
                break

            self.send_next(frame)

        self.stop()

    def send_next(self, frame):
        self.dst_data_queue.put(frame)

    def stop(self):
        self.cap.release()
