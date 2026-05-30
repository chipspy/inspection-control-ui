from PySide6.QtWidgets import QPushButton

from app.theme import Theme


class ExitButton(QPushButton):
    """큰 노란색 산업용 EXIT 버튼입니다."""

    def __init__(self, parent=None):
        super().__init__("EXIT", parent)
        self.setFixedSize(270, 65)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {Theme.YELLOW};
                color: {Theme.EXIT_BLUE};
                font-size: 36px;
                font-weight: bold;
                border: 2px solid black;
                padding: 4px;
            }}
            QPushButton:hover {{
                background-color: #FFF86A;
            }}
            QPushButton:pressed {{
                background-color: #D8CC00;
                padding-top: 8px;
                padding-left: 8px;
            }}
            """
        )
