from PySide6.QtCore import QTimer

from app.cameras.webcam_camera import WebcamCamera
from app.simulators.camera_simulator import CameraSimulator
from app.simulators.io_simulator import IOSimulator


class MainController:
    """UI와 I/O, 카메라 시뮬레이션을 연결하는 컨트롤러입니다."""

    def __init__(self, window, use_webcam: bool = True):
        self.window = window
        self.io_simulator = IOSimulator()
        self.use_webcam = use_webcam

        # 화면 전환 지연을 줄이기 위해 I/O 페이지에서는 가짜 카메라를 사용할 수 있게 했습니다.
        self.webcam_camera = WebcamCamera() if use_webcam else None
        self.camera_simulator = CameraSimulator()

        self.io_timer = QTimer()
        self.io_timer.timeout.connect(self.update_io)

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera)

        self.window.output_panel.output_changed.connect(self.set_output)

    def start(self):
        if self.webcam_camera is not None:
            self.webcam_camera.start()
        self.io_timer.start(120)
        self.camera_timer.start(33)
        self.update_io()
        self.update_camera()

    def stop(self):
        self.io_timer.stop()
        self.camera_timer.stop()
        if self.webcam_camera is not None:
            self.webcam_camera.stop()

    def update_io(self):
        self.io_simulator.update()
        self.window.input_panel.update_states(self.io_simulator.di_states())
        self.window.output_panel.update_states(self.io_simulator.do_states())

    def update_camera(self):
        if self.webcam_camera is not None:
            frame = self.webcam_camera.read_pixmap()
        else:
            frame = self.camera_simulator.make_frame(
                trigger_on=self.io_simulator.is_camera_trigger_on(),
                result_ok=self.io_simulator.last_result_ok,
            )
        self.window.camera_view.set_frame(frame)

    def set_output(self, index: int, is_on: bool):
        # 실제 PLC 출력 제어가 아니라 화면 시뮬레이터 상태만 변경합니다.
        self.io_simulator.set_do_state(index, is_on)
        self.window.output_panel.update_states(self.io_simulator.do_states())
