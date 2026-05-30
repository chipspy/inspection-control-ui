from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from app.controllers.main_controller import MainController
from app.simulators.io_simulator import IOSimulator
from app.theme import Theme
from app.widgets.camera_view import CameraView
from app.widgets.exit_button import ExitButton
from app.widgets.io_panel import IOPanel
from app.widgets.title_box import TitleBox


class MainWindow(QMainWindow):
    """검사자동화 설비 상태 점검용 메인 화면입니다."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inspection Automation Status Check UI - Simulation")
        self.setFixedSize(Theme.WINDOW_WIDTH, Theme.WINDOW_HEIGHT)

        # 패널 생성을 위해 채널 이름만 먼저 가져옵니다.
        initial_io = IOSimulator()

        self.input_panel = IOPanel(
            header="DIGITAL INPUTS (DIs)",
            prefix="DI",
            channels=initial_io.di_channels,
            show_switch=False,
        )
        self.output_panel = IOPanel(
            header="DIGITAL OUTPUTS (DOs)",
            prefix="DO",
            channels=initial_io.do_channels,
            show_switch=True,
        )
        self.camera_view = CameraView()
        self.exit_button = ExitButton()

        self._build_layout()

        self.controller = MainController(self)
        self.exit_button.clicked.connect(self.close)
        self.controller.start()

    def _build_layout(self):
        central = QWidget()
        central.setStyleSheet(f"background-color: {Theme.BACKGROUND};")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(34, 86, 12, 14)
        root.setSpacing(14)

        top_area = QHBoxLayout()
        top_area.setSpacing(41)
        root.addLayout(top_area)

        input_column = self._make_io_column("INPUT", self.input_panel)
        output_column = self._make_io_column("OUTPUT", self.output_panel)
        camera_column = self._make_camera_column()

        top_area.addWidget(input_column, 0, Qt.AlignTop)
        top_area.addWidget(output_column, 0, Qt.AlignTop)
        top_area.addWidget(camera_column, 0, Qt.AlignTop)
        top_area.addStretch(1)

        bottom_area = QHBoxLayout()
        bottom_area.addStretch(1)
        bottom_area.addWidget(self.exit_button)
        root.addLayout(bottom_area)

    def _make_io_column(self, title: str, panel: QWidget) -> QWidget:
        column = QWidget()
        column.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(column)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(TitleBox(title), 0, Qt.AlignHCenter)
        layout.addWidget(panel)
        return column

    def _make_camera_column(self) -> QWidget:
        column = QWidget()
        column.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(column)
        layout.setContentsMargins(14, 0, 0, 0)
        layout.setSpacing(36)
        layout.addWidget(TitleBox("CAMERA"), 0, Qt.AlignHCenter)

        camera_frame = QFrame()
        camera_frame.setStyleSheet("background: transparent; border: none;")
        camera_layout = QHBoxLayout(camera_frame)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.addWidget(self.camera_view)
        layout.addWidget(camera_frame)
        return column

    def closeEvent(self, event):  # noqa: N802
        # 종료 시 타이머만 안전하게 정지합니다. 실제 장비 제어는 없습니다.
        self.controller.stop()
        event.accept()
