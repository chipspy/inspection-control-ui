from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget

from app.models.io_channel import IOChannel
from app.theme import Theme


class LampWidget(QWidget):
    """동그란 상태 램프입니다."""

    def __init__(self, diameter: int = 14, parent=None):
        super().__init__(parent)
        self._is_on = False
        self._diameter = diameter
        self.setFixedSize(diameter + 4, diameter + 4)

    def set_on(self, is_on: bool):
        self._is_on = is_on
        self.update()

    def paintEvent(self, event):  # noqa: N802 - Qt 메서드 이름
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = Theme.LAMP_ON if self._is_on else Theme.LAMP_OFF
        painter.setBrush(QColor(color))
        painter.setPen(QPen(QColor(Theme.LAMP_BORDER), 1))
        painter.drawEllipse(2, 2, self._diameter, self._diameter)


class SwitchWidget(QWidget):
    """DO를 스위치처럼 보이게 하는 표시 위젯입니다."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_on = False
        self.setFixedSize(34, 18)

    def set_on(self, is_on: bool):
        self._is_on = is_on
        self.update()

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg = Theme.SWITCH_ON if self._is_on else Theme.SWITCH_OFF
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(bg))
        painter.drawRoundedRect(1, 2, 32, 14, 7, 7)

        knob_x = 18 if self._is_on else 3
        painter.setBrush(QColor(Theme.SWITCH_KNOB))
        painter.drawEllipse(knob_x, 3, 12, 12)


class IORow(QWidget):
    """IO 한 줄을 표시합니다. DO인 경우 스위치 표시가 추가됩니다."""

    toggled = Signal(bool)

    def __init__(self, channel: IOChannel, prefix: str, show_switch: bool = False, parent=None):
        super().__init__(parent)
        self.channel = channel
        self.prefix = prefix
        self.show_switch = show_switch

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(False)
        self.setFixedHeight(23)
        self.setStyleSheet(
            f"""
            IORow {{
                background-color: {Theme.PANEL_BG};
                border: none;
            }}
            """
        )

        self.main_lamp = LampWidget()
        self.sub_lamp = LampWidget()
        self.label = QLabel(self._make_label_text())
        self.label.setStyleSheet(
            f"""
            QLabel {{
                color: {Theme.TEXT};
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                border: none;
            }}
            """
        )
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.switch = SwitchWidget() if show_switch else None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 0, 8, 0)
        layout.setSpacing(5)
        layout.addWidget(self.main_lamp)
        layout.addWidget(self.sub_lamp)
        layout.addWidget(self.label, 1)
        if self.switch:
            layout.addWidget(self.switch)

        self.set_state(channel.is_on)

    def _make_label_text(self) -> str:
        return f"{self.prefix}_{self.channel.code}: {self.channel.name}"

    def set_state(self, is_on: bool):
        self.channel.is_on = is_on
        self.main_lamp.set_on(is_on)
        # 보조 램프는 현장 화면 느낌을 위해 반대 상태로 표시합니다.
        self.sub_lamp.set_on(not is_on)
        if self.switch:
            self.switch.set_on(is_on)

    def mousePressEvent(self, event):  # noqa: N802
        # DO 행은 사용자가 클릭해서 직접 ON/OFF 조작할 수 있습니다.
        if self.show_switch and event.button() == Qt.LeftButton:
            new_state = not self.channel.is_on
            self.set_state(new_state)
            self.toggled.emit(new_state)
        super().mousePressEvent(event)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        # 각 IO 행 배경도 강제로 검정색으로 칠합니다.
        painter.fillRect(self.rect(), QColor(Theme.PANEL_BG))
        painter.setPen(QPen(QColor(Theme.ROW_LINE), 1))
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
