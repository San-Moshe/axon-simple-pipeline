import multiprocessing

from detector import Detector
from stream_reader import StreamReader
from pathlib import Path
from video_presentation import Presenter

if __name__ == '__main__':
    file_to_open = Path("D:/people.mp4")
    read_to_detector_queue = multiprocessing.Queue()
    detector_to_presentation_queue = multiprocessing.Queue()

    stop_signal = multiprocessing.Event()

    reader = StreamReader(file_path=file_to_open, data_dst=read_to_detector_queue, stop_signal=stop_signal)
    detector = Detector(data_src=read_to_detector_queue, data_dst=detector_to_presentation_queue,
                        stop_signal=stop_signal)
    presenter = Presenter(data_src=detector_to_presentation_queue, stop_signal=stop_signal)

    proc_a = multiprocessing.Process(target=reader.start)
    proc_b = multiprocessing.Process(target=detector.start)
    proc_c = multiprocessing.Process(target=presenter.start)

    proc_a.start()
    proc_b.start()
    proc_c.start()

    proc_a.join()
    proc_b.join()
    proc_c.join()
