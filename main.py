import multiprocessing

from detector import Detector
from stream_reader import StreamReader
from pathlib import Path
from video_presentation import Presenter
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a video file",
                                           filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])

    if not file_path:
        print("File selection canceled.")
        exit()

    video_path = Path(file_path)
    read_to_detector_queue = multiprocessing.Queue()
    detector_to_presentation_queue = multiprocessing.Queue()

    stop_signal = multiprocessing.Event()

    reader = StreamReader(file_path=video_path, data_dst=read_to_detector_queue, stop_signal=stop_signal)
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
