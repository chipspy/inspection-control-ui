from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget

from app.controllers.main_controller import MainController
from app.simulators.io_simulator import IOSimulator
from app.theme import Theme
from app.widgets.camera_view import CameraView
from app.widgets.io_panel import IOPanel
from app.widgets.title_box import TitleBox


class IOMonitorWindow(QWidget):
    """기존 I/O 모니터 화면을 Main 화면 내부에서 재사용하기 위한 위젯입니다."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {Theme.BACKGROUND};")

        # 패널 생성에 필요한 DI/DO 채널 이름은 기존 시뮬레이터를 그대로 사용합니다.
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

        self._build_layout()

        # Main 화면과 I/O 화면 전환 시 실제 웹캠 재오픈 지연을 줄이기 위해
        # I/O 화면의 카메라는 가짜 카메라 프레임을 사용합니다.
        self.controller = MainController(self, use_webcam=False)
        self._is_running = False

    def _build_layout(self):
        root = QVBoxLayout(self)
        # Main 화면의 하단 기능키 위 영역에 들어가도록 여백을 줄였습니다.
        root.setContentsMargins(8, 16, 8, 8)
        root.setSpacing(8)

        top_area = QHBoxLayout()
        top_area.setSpacing(20)
        root.addLayout(top_area)

        input_column = self._make_io_column("INPUT", self.input_panel)
        output_column = self._make_io_column("OUTPUT", self.output_panel)
        camera_column = self._make_camera_column()

        top_area.addWidget(input_column, 0, Qt.AlignTop)
        top_area.addWidget(output_column, 0, Qt.AlignTop)
        top_area.addWidget(camera_column, 0, Qt.AlignTop)
        top_area.addStretch(1)

        # EXIT 버튼은 Main 화면의 기능키 구조와 맞지 않으므로 제거했습니다.
        root.addStretch(1)

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

    def start_monitor(self):
        """I/O 화면이 표시될 때 시뮬레이션 타이머와 카메라를 시작합니다."""
        if not self._is_running:
            self.controller.start()
            self._is_running = True

    def stop_monitor(self):
        """I/O 화면에서 다른 화면으로 이동하거나 종료할 때 안전하게 정지합니다."""
        if self._is_running:
            self.controller.stop()
            self._is_running = False

    def closeEvent(self, event):  # noqa: N802
        self.stop_monitor()
        event.accept()
