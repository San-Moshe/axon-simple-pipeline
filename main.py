from stream_reader import StreamReader
from pathlib import Path

if __name__ == '__main__':
    file_to_open = Path("D:/people.mp4")

    reader = StreamReader(file_to_open)
    reader.start()

