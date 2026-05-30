from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.models.io_channel import IOChannel
from app.theme import Theme
from app.widgets.io_row import IORow


class IOPanel(QWidget):
    """DI 또는 DO 16개를 표시하는 어두운 패널입니다."""

    output_changed = Signal(int, bool)

    def __init__(self, header: str, prefix: str, channels: list[IOChannel], show_switch: bool, parent=None):
        super().__init__(parent)
        self.rows: list[IORow] = []
        self.setObjectName("ioPanel")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.setFixedSize(386, 434)
        self.setStyleSheet(
            f"""
            QWidget#ioPanel {{
                background-color: {Theme.PANEL_BG};
                border: 2px solid {Theme.PANEL_BORDER};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 8, 9, 10)
        layout.setSpacing(0)

        title = QLabel(header)
        title.setStyleSheet(
            f"""
            QLabel {{
                color: {Theme.PANEL_HEADER_TEXT};
                font-size: 12px;
                font-weight: bold;
                border: none;
                background: transparent;
            }}
            """
        )
        title.setFixedHeight(24)
        layout.addWidget(title)

        for channel in channels:
            row = IORow(channel, prefix=prefix, show_switch=show_switch)
            if show_switch:
                row.toggled.connect(
                    lambda state, channel_number=channel.number: self.output_changed.emit(channel_number - 1, state)
                )
            layout.addWidget(row)
            self.rows.append(row)

        layout.addStretch(1)

    def update_states(self, states: list[bool]):
        for row, state in zip(self.rows, states):
            row.set_state(state)

    def paintEvent(self, event):  # noqa: N802
        # 스타일시트가 OS/테마 영향으로 약하게 적용되는 경우를 막기 위해
        # 패널 바탕을 QPainter로 한 번 더 검정색으로 칠합니다.
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(Theme.PANEL_BG))
        painter.setPen(QPen(QColor(Theme.PANEL_BORDER), 2))
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
