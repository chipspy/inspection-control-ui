from app.models.io_channel import IOChannel


class IOSimulator:
    """실제 PLC가 아닌, 화면 테스트용 가짜 DI/DO 시뮬레이터입니다."""

    def __init__(self):
        self.tick_count = 0
        self.last_result_ok = True
        self._prev_trigger = False
        self._inspection_done_timer = 0

        di_names = [
            "Conveyor Start",
            "Part Present Sensor",
            "Part Center Sensor",
            "Part Sent Sensor",
            "Part Clamp Sensor",
            "Safety Door Sensor",
            "Air Pressure Sensor",
            "Home Position Sensor",
            "Conveyor Sensor",
            "Vision Ready",
            "Robot Home Sensor",
            "Reject Full Sensor",
            "Light Curtain Sensor",
            "Emergency Normal",
            "Auto Mode Select",
            "Inspection Complete",
        ]
        do_names = [
            "Run Conveyor",
            "Extend Robot Arm",
            "Bend Robot Arm",
            "Start Robot Arm",
            "Turn On Light",
            "Trigger Camera",
            "Reject Cylinder",
            "Buzzer",
            "Tower Lamp Green",
            "Tower Lamp Red",
            "Tower Lamp Yellow",
            "Clamp Solenoid",
            "Vacuum On",
            "Blow Air",
            "Product Stopper",
            "System Ready",
        ]

        self.di_channels = [IOChannel(i + 1, name) for i, name in enumerate(di_names)]
        self.do_channels = [IOChannel(i + 1, name) for i, name in enumerate(do_names)]
        self.do_channels[15].is_on = True

    def update(self):
        """INPUT은 자동 시뮬레이션, OUTPUT은 사용자가 조작한 상태를 유지합니다."""
        self.tick_count += 1
        phase = self.tick_count % 80

        # 항상 ON에 가까운 안전/준비 계통 입력
        always_on_di = [5, 6, 7, 8, 10, 11, 13, 14, 15]
        for index in always_on_di:
            self.di_channels[index].is_on = True

        run_conveyor = self.do_channels[0].is_on
        trigger_camera = self.do_channels[5].is_on
        reject_on = self.do_channels[6].is_on
        clamp_on = self.do_channels[11].is_on

        # 사용자가 DO_06 Trigger Camera를 ON으로 바꾸는 순간 검사 결과를 갱신합니다.
        if trigger_camera and not self._prev_trigger:
            cycle_index = self.tick_count // 40
            self.last_result_ok = cycle_index % 3 != 2
            self._inspection_done_timer = 22
        self._prev_trigger = trigger_camera

        if self._inspection_done_timer > 0:
            self._inspection_done_timer -= 1

        # INPUT은 실제 센서가 아닌 자동 시뮬레이션으로 계속 움직입니다.
        # 단, 사용자가 DO_01 Run Conveyor를 켜면 더 활발하게 움직이는 것처럼 보입니다.
        auto_motion = 10 <= phase <= 65
        conveyor_motion = run_conveyor or auto_motion

        part_in = conveyor_motion and (10 <= phase <= 55)
        center = conveyor_motion and (24 <= phase <= 46)
        sent = conveyor_motion and (48 <= phase <= 65)
        inspection_done = self._inspection_done_timer > 0

        self.di_channels[0].is_on = conveyor_motion
        self.di_channels[1].is_on = part_in
        self.di_channels[2].is_on = center
        self.di_channels[3].is_on = sent
        self.di_channels[4].is_on = clamp_on or center
        self.di_channels[8].is_on = conveyor_motion and phase % 12 < 6
        self.di_channels[9].is_on = True
        self.di_channels[11].is_on = reject_on
        self.di_channels[15].is_on = inspection_done or (58 <= phase <= 70)

    def set_do_state(self, index: int, is_on: bool):
        """화면에서 사용자가 DO를 조작했을 때 호출됩니다."""
        if 0 <= index < len(self.do_channels):
            self.do_channels[index].is_on = is_on

    def di_states(self) -> list[bool]:
        return [channel.is_on for channel in self.di_channels]

    def do_states(self) -> list[bool]:
        return [channel.is_on for channel in self.do_channels]

    def is_camera_trigger_on(self) -> bool:
        return self.do_channels[5].is_on
