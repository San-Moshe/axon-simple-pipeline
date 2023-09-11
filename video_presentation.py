import datetime
import queue
from typing import Any, Dict

import cv2


class Presenter:
    def __init__(self, data_src: queue.Queue, stop_signal):
        self.src_data_queue = data_src
        self.stop_signal = stop_signal

        desired_frame_rate = 25
        self.delay = int(1000 / desired_frame_rate)

    def stop(self):
        cv2.destroyAllWindows()
        self.stop_signal.set()

    def start(self):
        while not self.stop_signal.is_set():
            try:
                frame, boxes = self.read_data()
            except queue.Empty:
                break
            else:
                if self.show_frame(frame, boxes):
                    break

        self.stop()

    def read_data(self) -> Dict[str, Any]:
        return self.src_data_queue.get(timeout=1)

    def show_frame(self, frame, bounding_boxes):
        if bounding_boxes:
            for (x1, y1, x2, y2) in bounding_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                roi = frame[y1:y2, x1:x2]
                blurred_roi = cv2.GaussianBlur(roi, (25, 25), 0)
                frame[y1:y2, x1:x2] = blurred_roi

        current_time = self.get_current_time()
        cv2.putText(frame, current_time, (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('frame', frame)

        if cv2.waitKey(self.delay) == ord('q'):
            return True

    def get_current_time(self):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return time_str
