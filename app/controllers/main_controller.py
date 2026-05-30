from PySide6.QtCore import QTimer

from app.cameras.webcam_camera import WebcamCamera
from app.simulators.io_simulator import IOSimulator


class MainController:
    """UI와 가짜 시뮬레이터를 연결하는 컨트롤러입니다."""

    def __init__(self, window):
        self.window = window
        self.io_simulator = IOSimulator()
        self.webcam_camera = WebcamCamera()

        self.io_timer = QTimer()
        self.io_timer.timeout.connect(self.update_io)

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera)

        self.window.output_panel.output_changed.connect(self.set_output)

    def start(self):
        self.webcam_camera.start()
        self.io_timer.start(120)
        self.camera_timer.start(33)
        self.update_io()
        self.update_camera()

    def stop(self):
        self.io_timer.stop()
        self.camera_timer.stop()
        self.webcam_camera.stop()

    def update_io(self):
        self.io_simulator.update()
        self.window.input_panel.update_states(self.io_simulator.di_states())
        self.window.output_panel.update_states(self.io_simulator.do_states())

    def update_camera(self):
        # CAMERA만 실제 PC 연결 카메라 영상을 표시합니다.
        # I/O는 계속 가짜 시뮬레이션입니다.
        frame = self.webcam_camera.read_pixmap()
        self.window.camera_view.set_frame(frame)

    def set_output(self, index: int, is_on: bool):
        # 사용자가 OUTPUT 스위치를 클릭하면 가짜 DO 상태만 변경합니다.
        # 실제 PLC나 장비 출력 제어는 하지 않습니다.
        self.io_simulator.set_do_state(index, is_on)
        self.window.output_panel.update_states(self.io_simulator.do_states())
