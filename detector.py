import cv2
import imutils
import queue
import numpy as np
from typing import List, Tuple, Optional


class Detector:
    def __init__(self, data_src: queue.Queue, data_dst: queue.Queue, stop_signal):
        self.src_data_queue = data_src
        self.dst_data_queue = data_dst
        self.stop_signal = stop_signal

        self.frame_counter = 0
        self.prev_frame = None

    def start(self):
        while not self.stop_signal.is_set():
            try:
                frame = self.read_frame()
            except queue.Empty:
                break
            else:
                detections, frame_with_boxes = self.detect(frame)
                self.send_detections(frame, detections)

    def read_frame(self):
        return self.src_data_queue.get(timeout=1)

    def detect(self, frame) -> Tuple[Optional[List[Tuple[int, int, int, int]]], Optional['numpy.ndarray']]:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.frame_counter == 0:
            self.prev_frame = gray_frame
            self.frame_counter += 1
            bounding_boxes = None  # No boxes for the first frame
        else:
            diff = cv2.absdiff(gray_frame, self.prev_frame)
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            self.prev_frame = gray_frame
            self.frame_counter += 1

            bounding_boxes = []

            for contour in cnts:
                (x, y, w, h) = cv2.boundingRect(contour)
                bounding_boxes.append((x, y, x + w, y + h))

            if bounding_boxes:
                frame_with_boxes = frame.copy()
                for (x1, y1, x2, y2) in bounding_boxes:
                    cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return bounding_boxes, frame

    def send_detections(self, original_frame, detections=None):
        self.dst_data_queue.put((original_frame, detections))
