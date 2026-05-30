from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPixmap

from app.theme import Theme


class CameraSimulator:
    """카메라 SDK 없이 QPainter로 가짜 검사 화면을 생성합니다."""

    def __init__(self, width: int = 344, height: int = 308):
        self.width = width
        self.height = height
        self.frame_count = 0
        self.last_result_text = "WAIT"
        self.last_result_ok = True

    def make_frame(self, trigger_on: bool, result_ok: bool) -> QPixmap:
        self.frame_count += 1
        self.last_result_ok = result_ok

        if trigger_on:
            self.last_result_text = "OK" if result_ok else "NG"

        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(QColor(Theme.CAMERA_BG))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        self._draw_grid(painter)
        self._draw_product(painter)
        self._draw_roi(painter)
        self._draw_result(painter, trigger_on)

        painter.end()
        return pixmap

    def _draw_grid(self, painter: QPainter):
        painter.setPen(QPen(QColor("#202020"), 1))
        for x in range(0, self.width, 28):
            painter.drawLine(x, 0, x, self.height)
        for y in range(0, self.height, 28):
            painter.drawLine(0, y, self.width, y)

    def _draw_product(self, painter: QPainter):
        # 제품이 좌우로 천천히 움직이는 것처럼 표시
        x = 35 + (self.frame_count * 3) % 210
        y = 115

        painter.setBrush(QColor("#6E6E6E"))
        painter.setPen(QPen(QColor("#C0C0C0"), 2))
        painter.drawRoundedRect(x, y, 92, 58, 8, 8)

        painter.setBrush(QColor("#2D2D2D"))
        painter.drawEllipse(x + 18, y + 14, 16, 16)
        painter.drawEllipse(x + 58, y + 14, 16, 16)

        painter.setPen(QPen(QColor("#A0A0A0"), 2))
        painter.drawLine(x + 12, y + 44, x + 80, y + 44)

    def _draw_roi(self, painter: QPainter):
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(Theme.ROI), 2))
        painter.drawRect(108, 88, 130, 105)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(112, 84, "ROI")

    def _draw_result(self, painter: QPainter, trigger_on: bool):
        color = Theme.OK if self.last_result_text == "OK" else Theme.NG if self.last_result_text == "NG" else "#FFFFFF"
        painter.setPen(QPen(QColor(color), 2))
        painter.setFont(QFont("Arial", 30, QFont.Bold))
        painter.drawText(15, 48, self.last_result_text)

        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.setPen(QColor("#B0B0B0"))
        painter.drawText(15, self.height - 16, "FAKE CAMERA - SIMULATION ONLY")

        if trigger_on:
            # 트리거 순간에는 노란 테두리로 플래시 느낌을 줌
            painter.setPen(QPen(QColor("#FFD800"), 5))
            painter.drawRect(3, 3, self.width - 6, self.height - 6)
