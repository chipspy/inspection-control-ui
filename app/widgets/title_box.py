from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from app.theme import Theme


class TitleBox(QLabel):
    """INPUT / OUTPUT / CAMERA 제목 상자입니다."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(162, 42)
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {Theme.TITLE_BG};
                color: {Theme.TITLE_TEXT};
                font-size: 25px;
                font-weight: bold;
            }}
            """
        )
