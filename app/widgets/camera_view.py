from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from app.theme import Theme


class CameraView(QLabel):
    """가짜 카메라 이미지를 보여주는 영역입니다."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(344, 308)
        self.setStyleSheet(f"background-color: {Theme.CAMERA_BG}; border: 1px solid #111;")
        self.setScaledContents(False)

    def set_frame(self, pixmap: QPixmap):
        self.setPixmap(pixmap)
