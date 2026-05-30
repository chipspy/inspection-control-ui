import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen, QPixmap


class WebcamCamera:
    """PC에 연결된 일반 웹캠 영상을 읽는 클래스입니다.

    주의:
    - PLC/장비 제어와 무관합니다.
    - 카메라 SDK가 아니라 OpenCV의 일반 VideoCapture만 사용합니다.
    - 카메라가 없거나 열리지 않으면 안내 화면을 반환합니다.
    """

    def __init__(self, camera_index: int = 0, width: int = 344, height: int = 308):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.capture = None
        self.is_opened = False

    def start(self):
        self.capture = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

        if not self.capture.isOpened():
            # CAP_DSHOW가 실패하는 PC도 있으므로 기본 방식으로 한 번 더 시도합니다.
            self.capture.release()
            self.capture = cv2.VideoCapture(self.camera_index)

        self.is_opened = self.capture.isOpened()

        if self.is_opened:
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def stop(self):
        if self.capture is not None:
            self.capture.release()
        self.capture = None
        self.is_opened = False

    def read_pixmap(self) -> QPixmap:
        if not self.is_opened or self.capture is None:
            return self._make_message_pixmap("CAMERA NOT OPENED")

        ok, frame = self.capture.read()
        if not ok or frame is None:
            return self._make_message_pixmap("NO CAMERA FRAME")

        # OpenCV는 BGR, Qt는 RGB를 사용합니다.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w

        image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        canvas = QPixmap(self.width, self.height)
        canvas.fill(QColor("#000000"))

        painter = QPainter(canvas)
        x = (self.width - pixmap.width()) // 2
        y = (self.height - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        self._draw_live_overlay(painter)
        painter.end()

        return canvas

    def _draw_live_overlay(self, painter: QPainter):
        # 실제 영상 위에 검사 화면 느낌의 ROI만 표시합니다.
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor("#00FF66"), 2))
        painter.drawRect(108, 88, 130, 105)

        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(112, 84, "ROI")

        painter.setPen(QPen(QColor("#00BFFF"), 2))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(12, 24, "LIVE CAMERA")

    def _make_message_pixmap(self, message: str) -> QPixmap:
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(QColor("#000000"))

        painter = QPainter(pixmap)
        painter.setPen(QColor("#FFDD00"))
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, message)

        painter.setPen(QColor("#AAAAAA"))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(12, self.height - 18, f"Camera index: {self.camera_index}")
        painter.end()

        return pixmap
