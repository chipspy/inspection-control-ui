from PySide6.QtCore import QPointF, QDateTime, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.cameras.webcam_camera import WebcamCamera
from app.io_monitor_window import IOMonitorWindow
from app.theme import Theme


PAGE_MAIN = 0
PAGE_MANUAL = 1
PAGE_TEACH = 2
PAGE_IO = 3
PAGE_MANAGE = 4


class StatusLamp(QWidget):
    """Main 화면의 RUN / STOP / ALARM 상태 램프입니다."""

    def __init__(self, color: str, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(24, 24)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(QPen(QColor("#20242A"), 2))
        painter.drawEllipse(2, 2, 20, 20)


class RunCircle(QWidget):
    """System Status 영역의 큰 RUN 표시입니다."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(92, 92)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#1B1E24"))
        painter.setPen(QPen(QColor("#080A0D"), 3))
        painter.drawEllipse(4, 4, 84, 84)

        painter.setBrush(QColor("#35DE36"))
        painter.setPen(QPen(QColor("#17821F"), 4))
        painter.drawEllipse(16, 16, 60, 60)

        painter.setPen(QColor("#153B17"))
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, "RUN")


class FunctionButton(QPushButton):
    """하단 기능키 버튼입니다. 텍스트와 아이콘을 직접 그려서 알아보기 쉽게 표시합니다."""

    def __init__(self, icon_kind: str, label_text: str, parent=None):
        super().__init__(parent)
        self.icon_kind = icon_kind
        self.label_text = label_text
        self._active = False
        self.setText("")
        self.setFixedHeight(100)
        self.setCursor(Qt.PointingHandCursor)

    def set_active(self, active: bool):
        self._active = active
        self.update()

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isDown():
            bg = QColor("#0A7EAC")
        elif self._active:
            bg = QColor("#12AEEB")
        else:
            bg = QColor("#777D83")

        border = QColor("#30C6FF" if self._active else "#38A7D0")
        rect = self.rect().adjusted(2, 2, -2, -2)

        painter.setPen(QPen(border, 2))
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 8, 8)

        icon_color = QColor("#D8DCE0")
        text_color = QColor("#FFFFFF")

        painter.setPen(QPen(icon_color, 3))
        painter.save()
        painter.translate(self.width() / 2, 35)
        painter.scale(0.68, 0.68)
        painter.translate(-self.width() / 2, -35)
        self._draw_icon(painter, self.icon_kind)
        painter.restore()

        painter.setPen(text_color)
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(QRectF(0, 66, self.width(), 28), Qt.AlignCenter, self.label_text)

    def _draw_icon(self, painter: QPainter, icon_kind: str):
        cx = self.width() / 2

        if icon_kind == "home":
            roof = QPolygonF(
                [
                    QPointF(cx - 28, 38),
                    QPointF(cx, 14),
                    QPointF(cx + 28, 38),
                ]
            )
            painter.drawPolyline(roof)
            painter.drawRect(QRectF(cx - 20, 36, 40, 28))
            painter.drawLine(QPointF(cx - 6, 64), QPointF(cx - 6, 48))
            painter.drawLine(QPointF(cx + 6, 64), QPointF(cx + 6, 48))

        elif icon_kind == "manual":
            painter.drawLine(QPointF(cx, 18), QPointF(cx, 48))
            painter.drawEllipse(QRectF(cx - 8, 10, 16, 16))
            painter.drawRoundedRect(QRectF(cx - 24, 48, 48, 10), 4, 4)
            painter.drawLine(QPointF(cx - 16, 58), QPointF(cx - 24, 66))
            painter.drawLine(QPointF(cx + 16, 58), QPointF(cx + 24, 66))
            painter.drawLine(QPointF(cx - 24, 66), QPointF(cx + 24, 66))

        elif icon_kind == "teach":
            painter.drawLine(QPointF(cx - 20, 58), QPointF(cx + 18, 20))
            painter.drawLine(QPointF(cx + 18, 20), QPointF(cx + 28, 30))
            painter.drawLine(QPointF(cx + 28, 30), QPointF(cx - 10, 68))
            painter.drawLine(QPointF(cx - 20, 58), QPointF(cx - 10, 68))
            painter.drawLine(QPointF(cx - 14, 62), QPointF(cx - 26, 72))

        elif icon_kind == "io":
            painter.drawRoundedRect(QRectF(cx - 32, 22, 64, 30), 6, 6)
            painter.setFont(QFont("Arial", 14, QFont.Bold))
            painter.drawText(QRectF(cx - 32, 22, 64, 30), Qt.AlignCenter, "I/O")

        elif icon_kind == "manage":
            painter.drawEllipse(QRectF(cx - 34, 22, 28, 28))
            painter.drawEllipse(QRectF(cx - 26, 30, 12, 12))
            for dx, dy in [(-40, 36), (-6, 36), (-20, 16), (-20, 56)]:
                painter.drawLine(QPointF(cx + dx, dy), QPointF(cx + dx + 8, dy))

            painter.drawEllipse(QRectF(cx - 2, 44, 18, 18))
            painter.drawEllipse(QRectF(cx + 3, 49, 8, 8))

            star = QPolygonF(
                [
                    QPointF(cx + 40, 18),
                    QPointF(cx + 48, 38),
                    QPointF(cx + 68, 46),
                    QPointF(cx + 48, 54),
                    QPointF(cx + 40, 74),
                    QPointF(cx + 32, 54),
                    QPointF(cx + 12, 46),
                    QPointF(cx + 32, 38),
                ]
            )
            painter.drawPolygon(star)


class MainWindow(QMainWindow):
    """검사자동화 설비 제어용 Main 화면입니다."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPY Inspection System")
        self.setFixedSize(Theme.WINDOW_WIDTH, Theme.WINDOW_HEIGHT)

        self.current_camera_index = 0
        self.main_camera = WebcamCamera(camera_index=self.current_camera_index, width=670, height=430)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)

        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera)

        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status_values)

        self.status_tick = 0
        self.production_count = 0
        self.ng_count = 0
        self.total_count = 10

        self._build_layout()
        self._connect_events()

        self.show_page(PAGE_MAIN)
        self.clock_timer.start(1000)
        self.status_timer.start(1000)
        self.update_clock()
        self.update_status_values()

    def _build_layout(self):
        central = QWidget()
        central.setStyleSheet("background-color: #171B20;")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(18, 8, 18, 8)
        root.setSpacing(8)

        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background-color: #171B20; border: none;")
        root.addWidget(self.pages, 1)

        self.main_page = self._make_main_page()
        self.manual_page = self._make_text_page("MANUAL")
        self.teach_page = self._make_text_page("TEACH")
        self.io_page = IOMonitorWindow(parent=self)
        self.manage_page = self._make_text_page("MANAGE")

        self.pages.addWidget(self.main_page)
        self.pages.addWidget(self.manual_page)
        self.pages.addWidget(self.teach_page)
        self.pages.addWidget(self.io_page)
        self.pages.addWidget(self.manage_page)

        root.addLayout(self._make_function_keys())

    def _make_main_page(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background-color: #171B20;")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        layout.addLayout(self._make_header())

        content = QHBoxLayout()
        content.setSpacing(6)
        layout.addLayout(content, 1)

        content.addWidget(self._make_camera_selection_panel())
        content.addWidget(self._make_camera_panel(), 1)
        content.addWidget(self._make_status_panel())

        return page

    def _make_text_page(self, text: str) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background-color: #171B20;")
        layout = QVBoxLayout(page)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 64px; font-weight: bold;")
        layout.addWidget(label)
        return page

    def _make_header(self) -> QHBoxLayout:
        header = QHBoxLayout()

        logo = QLabel("SPY")
        logo.setFixedWidth(190)
        logo.setStyleSheet("color: #4CB6D5; font-size: 35px; font-weight: bold;")

        title = QLabel("SPY Inspection System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #5CB7D6; font-size: 30px; font-weight: bold;")

        self.clock_label = QLabel()
        self.clock_label.setFixedWidth(260)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.clock_label.setStyleSheet("color: white; font-size: 25px; font-weight: bold;")

        header.addWidget(logo)
        header.addWidget(title, 1)
        header.addWidget(self.clock_label)
        return header

    def _make_panel(self) -> QFrame:
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: #292E35;
                border: 2px solid #11151A;
                border-radius: 6px;
            }
            """
        )
        return panel

    def _make_camera_selection_panel(self) -> QFrame:
        panel = self._make_panel()
        panel.setFixedWidth(210)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(10)

        title = QLabel("Camera Selection")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; border: none;")
        layout.addWidget(title)

        self.camera_buttons: list[QPushButton] = []
        for camera_number in range(1, 6):
            prefix = "*" if camera_number == 1 else "o"
            button = QPushButton(f"{prefix}  CAM {camera_number}")
            button.setCheckable(True)
            button.setFixedHeight(70)
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(self._camera_button_style())
            if camera_number == 1:
                button.setChecked(True)
            button.clicked.connect(lambda checked, number=camera_number: self.select_camera(number))
            layout.addWidget(button)
            self.camera_buttons.append(button)

        layout.addStretch(1)
        return panel

    def _camera_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #292E35;
            color: #FFFFFF;
            border: 1px solid #343A42;
            border-radius: 6px;
            text-align: left;
            padding-left: 12px;
            font-size: 20px;
            font-weight: bold;
        }
        QPushButton:checked {
            background-color: #31404B;
            color: #5ACDFF;
            border: 2px solid #35AEEA;
        }
        QPushButton:hover {
            border: 2px solid #35AEEA;
        }
        """

    def _make_camera_panel(self) -> QFrame:
        panel = self._make_panel()

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(8)

        self.current_camera_label = QLabel("Current CAM1")
        self.current_camera_label.setStyleSheet("color: #4CB6D5; font-size: 24px; font-weight: bold; border: none;")
        layout.addWidget(self.current_camera_label)

        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setFixedSize(670, 430)
        self.camera_label.setStyleSheet("background-color: black; border: 1px solid #111111;")
        layout.addWidget(self.camera_label, 0, Qt.AlignCenter)

        return panel

    def _make_status_panel(self) -> QFrame:
        panel = self._make_panel()
        panel.setFixedWidth(330)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        title = QLabel("System Status")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; border: none;")
        layout.addWidget(title)

        run_area = QHBoxLayout()
        run_area.setContentsMargins(0, 0, 0, 8)
        run_area.addWidget(RunCircle())
        run_area.addLayout(self._make_lamp_list())
        layout.addLayout(run_area)

        layout.addWidget(self._make_line())
        self.tact_time_1 = self._make_value_label("00:07:18")
        self.tact_time_2 = self._make_value_label("00:07:10")
        layout.addLayout(self._make_status_row("Tactile time", self.tact_time_1))
        layout.addLayout(self._make_status_row("Tactile time", self.tact_time_2))
        layout.addWidget(self._make_line())
        layout.addLayout(self._make_production_area())
        layout.addWidget(self._make_line())
        layout.addLayout(self._make_model_row())
        self.quantity_label = self._make_value_label("100")
        layout.addLayout(self._make_status_row("Quantity Reset", self.quantity_label))

        add_button = QPushButton("Add")
        add_button.setEnabled(False)
        add_button.setFixedHeight(42)
        add_button.setStyleSheet(
            """
            QPushButton {
                background-color: #303640;
                color: #777777;
                border: 2px solid #434A54;
                border-radius: 6px;
                font-size: 18px;
            }
            """
        )
        layout.addWidget(add_button)
        layout.addStretch(1)
        return panel

    def _make_lamp_list(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        for text, color in [("RUN", "#31E448"), ("STOP", "#FFD43B"), ("ALARM", "#FF2D2D")]:
            row = QHBoxLayout()
            row.addWidget(StatusLamp(color))
            label = QLabel(text)
            label.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none;")
            row.addWidget(label)
            row.addStretch(1)
            layout.addLayout(row)
        return layout

    def _make_value_label(self, value: str) -> QLabel:
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFixedWidth(130)
        value_label.setStyleSheet(
            """
            QLabel {
                background-color: #111419;
                color: #D8DCE0;
                border: 1px solid #252B32;
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            """
        )
        return value_label

    def _make_status_row(self, name: str, value_label: QLabel) -> QHBoxLayout:
        row = QHBoxLayout()
        label = QLabel(name)
        label.setStyleSheet("color: white; font-size: 18px; border: none;")

        row.addWidget(label)
        row.addStretch(1)
        row.addWidget(value_label)
        return row

    def _make_production_area(self) -> QGridLayout:
        grid = QGridLayout()
        headers = ["Production", "NG", "Total"]
        values = [("OK", "#4AB94A"), ("NG", "#D13D3D"), ("10", "#FFFFFF")]

        for column, header in enumerate(headers):
            label = QLabel(header)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; font-size: 17px; font-weight: bold; border: none;")
            grid.addWidget(label, 0, column)

        for column, (value, color) in enumerate(values):
            label = QLabel(value)
            if value == "OK":
                self.ok_count_label = label
            elif value == "NG":
                self.ng_count_label = label
            elif value == "10":
                self.total_count_label = label
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color: {color}; font-size: 34px; font-weight: bold; border: none;")
            grid.addWidget(label, 1, column)

        return grid

    def _make_model_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        label = QLabel("Model Select")
        label.setStyleSheet("color: white; font-size: 18px; border: none;")

        combo = QComboBox()
        combo.addItems(["M.1", "M.2", "M.3"])
        combo.setFixedWidth(130)
        combo.setStyleSheet(
            """
            QComboBox {
                background-color: #303640;
                color: white;
                border: 2px solid #434A54;
                border-radius: 6px;
                font-size: 18px;
                padding-left: 8px;
            }
            """
        )

        row.addWidget(label)
        row.addStretch(1)
        row.addWidget(combo)
        return row

    def _make_line(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #3A4048; border: none;")
        line.setFixedHeight(2)
        return line

    def _make_function_keys(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.main_button = FunctionButton("home", "MAIN")
        self.manual_button = FunctionButton("manual", "MANUAL")
        self.teach_button = FunctionButton("teach", "TEACH")
        self.io_button = FunctionButton("io", "I/O")
        self.manage_button = FunctionButton("manage", "MANAGE")

        self.function_buttons = {
            PAGE_MAIN: self.main_button,
            PAGE_MANUAL: self.manual_button,
            PAGE_TEACH: self.teach_button,
            PAGE_IO: self.io_button,
            PAGE_MANAGE: self.manage_button,
        }

        for button in self.function_buttons.values():
            layout.addWidget(button, 1)

        return layout

    def _connect_events(self):
        self.main_button.clicked.connect(lambda: self.show_page(PAGE_MAIN))
        self.manual_button.clicked.connect(lambda: self.show_page(PAGE_MANUAL))
        self.teach_button.clicked.connect(lambda: self.show_page(PAGE_TEACH))
        self.io_button.clicked.connect(lambda: self.show_page(PAGE_IO))
        self.manage_button.clicked.connect(lambda: self.show_page(PAGE_MANAGE))

    def show_page(self, page_index: int):
        previous_index = self.pages.currentIndex()
        if previous_index == PAGE_IO and page_index != PAGE_IO:
            self.io_page.stop_monitor()

        self.pages.setCurrentIndex(page_index)

        for index, button in self.function_buttons.items():
            button.set_active(index == page_index)

        if page_index == PAGE_MAIN:
            self.start_main_camera()
        elif page_index == PAGE_IO:
            self.stop_main_camera(release=False)

        if page_index == PAGE_IO:
            self.io_page.start_monitor()

    def start_main_camera(self):
        if not self.main_camera.is_opened:
            self.main_camera.start()
        if not self.camera_timer.isActive():
            self.camera_timer.start(33)
        self.update_camera()

    def stop_main_camera(self, release: bool = False):
        if self.camera_timer.isActive():
            self.camera_timer.stop()
        if release:
            self.main_camera.stop()

    def update_clock(self):
        now = QDateTime.currentDateTime()
        self.clock_label.setText(now.toString("yyyy-MM-dd HH:mm"))

    def update_status_values(self):
        # 실제 장비 카운터가 아닌 Main 화면 표시용 시뮬레이터입니다.
        self.status_tick += 1

        tact_1 = 430 + self.status_tick
        tact_2 = 420 + (self.status_tick * 2)
        self.tact_time_1.setText(self._format_elapsed(tact_1))
        self.tact_time_2.setText(self._format_elapsed(tact_2))

        if self.status_tick % 3 == 0:
            self.production_count += 1
            self.total_count += 1

        if self.status_tick % 11 == 0:
            self.ng_count += 1

        self.ok_count_label.setText(str(self.production_count))
        self.ng_count_label.setText(str(self.ng_count))
        self.total_count_label.setText(str(self.total_count))
        self.quantity_label.setText(str(100 + (self.status_tick % 25)))

    def _format_elapsed(self, total_seconds: int) -> str:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_camera(self):
        frame = self.main_camera.read_pixmap()
        self.camera_label.setPixmap(frame)

    def select_camera(self, camera_number: int):
        # 실제 장비 제어 없이 OpenCV 카메라 인덱스만 변경합니다.
        self.current_camera_index = camera_number - 1

        for index, button in enumerate(self.camera_buttons, start=1):
            selected = index == camera_number
            button.setChecked(selected)
            button.setText(f"*  CAM {index}" if selected else f"o  CAM {index}")

        self.current_camera_label.setText(f"Current CAM{camera_number}")
        self.main_camera.stop()
        self.main_camera = WebcamCamera(camera_index=self.current_camera_index, width=670, height=430)
        self.main_camera.start()
        self.update_camera()

    def closeEvent(self, event):  # noqa: N802
        # Main 화면 종료 시 카메라와 I/O 시뮬레이션을 안전하게 정리합니다.
        self.stop_main_camera(release=True)
        self.clock_timer.stop()
        self.status_timer.stop()
        self.io_page.stop_monitor()
        event.accept()
