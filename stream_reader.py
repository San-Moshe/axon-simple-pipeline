import cv2


class StreamReader:
    def __init__(self, file_path):
        self.video_path = file_path.as_posix()
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            raise ValueError("Can't open video file provided")

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            cv2.imshow("name", frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    def stop(self):
        self.cap.release()
