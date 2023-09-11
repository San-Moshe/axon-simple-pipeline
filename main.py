import queue

from detector import Detector
from stream_reader import StreamReader
from pathlib import Path
import threading

from video_presentation import Presenter

if __name__ == '__main__':
    file_to_open = Path("D:/people.mp4")
    read_to_detector_queue = queue.Queue()
    detector_to_presentation_queue = queue.Queue()

    reader = StreamReader(file_path=file_to_open, data_dst=read_to_detector_queue)
    detector = Detector(data_src=read_to_detector_queue, data_dst=detector_to_presentation_queue)
    presenter = Presenter(data_src=detector_to_presentation_queue)

    thread_a = threading.Thread(target=reader.start)
    thread_b = threading.Thread(target=detector.start)
    thread_c = threading.Thread(target=presenter.start)

    thread_a.start()
    thread_b.start()
    thread_c.start()
