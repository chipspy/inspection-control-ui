---
name: inspection-io-camera-ui
description: Use this skill when building a Python PySide6 HMI-style UI for inspection automation equipment. The target screen has INPUT, OUTPUT, and CAMERA windows similar to an industrial automation status-check screen. IO and camera must be simulated unless real hardware specifications are explicitly provided.
---

# Inspection IO Camera UI Skill

You are helping develop a professional HMI-style control software UI for inspection automation equipment.

The target software is not a simple demo.
It should look and behave like a real automation equipment status-check screen.

The reference UI has:
- Light blue industrial HMI background
- INPUT title at the top of the left area
- OUTPUT title at the top of the center area
- CAMERA title at the top of the right area
- Dark digital input list panel
- Dark digital output list panel
- Black camera image display area
- Large yellow EXIT button at the bottom-right
- IO status lamps and output switches
- Fake IO and fake camera simulation

## Absolute safety rule

Do not write real hardware control code.

Do not directly control:
- PLC
- robot arm
- conveyor motor
- servo motor
- pneumatic cylinder
- light controller
- camera SDK
- actuator
- real emergency stop circuit

Unless the user explicitly provides actual hardware specifications and asks for real communication code, always use simulation classes.

For this project, implement:
- Fake digital inputs
- Fake digital outputs
- Fake camera frames
- Fake inspection sequence
- Fake conveyor / sensor / robot-arm behavior

## Target UI layout

The UI should visually follow the reference screen.

Main window:
- Resolution target: around 1256 x 665 or scalable equivalent
- Background color: light blue industrial HMI style
- No unnecessary modern web-style design
- Industrial control-panel feel

Top titles:
- INPUT title above the left panel
- OUTPUT title above the middle panel
- CAMERA title above the right panel
- Title boxes should be light gray or white
- Text should be bold and large

Left panel:
- Header: DIGITAL INPUTS (DIs)
- Dark gray or black panel background
- 16 digital input rows
- Each row should have:
  - input number, for example DI_01
  - signal name
  - at least one round lamp indicator
  - realistic green/gray status
- Example input names:
  - Conveyor Start
  - Part Present Sensor
  - Conveyor Sensor
  - Part Sent Sensor
  - Part Clamp Sensor
  - Safety Door Sensor
  - Air Pressure Sensor
  - Home Position Sensor

Middle panel:
- Header: DIGITAL OUTPUTS (DOs)
- Dark gray or black panel background
- 16 digital output rows
- Each row should have:
  - output number, for example DO_01
  - output name
  - round status lamp
  - switch-style toggle indicator
- Example output names:
  - Run Conveyor
  - Extend Robot Arm
  - Bend Robot Arm
  - Start Robot Arm
  - Turn On Light
  - Trigger Camera
  - Reject Cylinder
  - Buzzer
  - Tower Lamp Green
  - Tower Lamp Red

Right panel:
- Header: CAMERA
- Black camera display area
- The camera area should simulate:
  - idle black screen
  - live camera frame
  - moving product
  - ROI box
  - OK / NG overlay
  - trigger flash effect
  - simple noise or grid if useful
- No real camera SDK should be used.

Bottom-right:
- Large EXIT button
- Yellow background
- Blue bold text
- Industrial bevel-like feel if possible
- Clicking EXIT should close the application safely after stopping timers.

## Application architecture

Use Python and PySide6.

Separate the project into clear files.

Recommended structure:

main.py
- Application entry point only

app/main_window.py
- Main window layout
- Places INPUT, OUTPUT, CAMERA, EXIT button

app/theme.py
- Colors, font sizes, common style values

app/models/io_channel.py
- Data model for DI and DO channels

app/widgets/title_box.py
- Reusable title widget for INPUT / OUTPUT / CAMERA

app/widgets/io_panel.py
- Reusable panel for digital input and output lists

app/widgets/io_row.py
- One row of IO status
- Lamps, labels, and optional output switch

app/widgets/camera_view.py
- Fake camera display
- Draws simulated frames using QPixmap / QPainter

app/widgets/exit_button.py
- Large industrial EXIT button

app/simulators/io_simulator.py
- Fake DI/DO state simulation

app/simulators/camera_simulator.py
- Fake camera frame generation

app/controllers/main_controller.py
- Connects UI and simulators
- Starts and stops timers
- Updates IO and camera periodically

## Development rules

1. Do not put everything in one file.
2. Keep UI code and simulation logic separate.
3. Use QTimer for first-stage simulation.
4. Do not use threads in the first version unless necessary.
5. Use QPainter or QPixmap for fake camera image generation.
6. Use beginner-readable Python.
7. Use Korean comments for important parts.
8. Keep class names clear.
9. Avoid over-engineering.
10. Make the first version runnable quickly.
11. After each change, explain how to run and test.
12. Preserve the target UI style.

## Simulation behavior

The fake IO simulator should behave realistically enough for a demo.

Digital inputs:
- Some sensors should blink or change state over time.
- Part Present Sensor should turn ON when a fake product enters.
- Conveyor Sensor should change during conveyor movement.
- Safety sensors should usually stay ON.
- Some random but controlled changes are acceptable.

Digital outputs:
- DO_01 Run Conveyor should be ON during automatic sequence.
- DO for Trigger Camera should pulse briefly.
- Robot arm outputs can turn ON/OFF in sequence.
- Reject Cylinder should activate on NG result.
- Tower lamp outputs can reflect machine status.

Camera:
- Camera screen should update periodically.
- It should display a fake product region.
- It should show ROI rectangle.
- It should show OK or NG result.
- The visual should look like an inspection machine display, not a game.

Inspection sequence example:
1. Conveyor starts.
2. Part Present Sensor turns ON.
3. Camera trigger output turns ON briefly.
4. Fake camera frame updates.
5. Inspection result is generated.
6. OK or NG is displayed.
7. If NG, reject output activates briefly.
8. Counts or result status may be updated later.

## Style guidelines

Use an industrial HMI feel:
- Blue background
- Dark IO panels
- Green active lamps
- Gray inactive lamps
- White text
- Thin separator lines between rows
- Large simple labels
- Yellow EXIT button

Avoid:
- Web dashboard style
- Excessive gradients
- Too much animation
- Unrealistic colors
- Tiny unreadable text
- Real hardware code

## Required first implementation

When the user asks for the first implementation, create a runnable PySide6 app with:

- Main window
- INPUT title and DI panel
- OUTPUT title and DO panel
- CAMERA title and fake camera area
- EXIT button
- 16 DI rows
- 16 DO rows
- Fake IO state updates
- Fake camera frame updates
- No real hardware dependency

## Response style

Respond in Korean.

For every coding response, use this structure:

1. 이번 단계 목표
2. 생성/수정 파일
3. 핵심 구조 설명
4. 실행 방법
5. 테스트 방법
6. 다음 단계 제안

When giving code, make it copy-paste friendly.

When there is an error, explain it for a beginner.

## Main screen integration rules

The application now needs a Main screen before the I/O monitor screen.

The startup flow should be:

1. main.py starts the application.
2. MainWindow is displayed first.
3. MainWindow contains industrial HMI-style function keys.
4. When the user clicks the I/O function key, the existing I/O monitor screen opens.
5. The existing I/O screen must not be redesigned or rewritten unnecessarily.
6. Refactor the existing I/O screen into a reusable IOMonitorWindow if needed.
7. The I/O screen should keep its DI / DO / CAMERA simulation behavior.
8. The I/O screen EXIT button should close the I/O screen or return to Main, not accidentally destroy the whole application unless explicitly requested.
9. Keep Main screen code and I/O screen code separated.
10. Do not write real PLC, camera, motor, robot, or actuator control code.

## Main screen UI rules

The Main screen should follow the attached reference image provided by the user.

It should feel like an industrial equipment HMI main menu.

Recommended elements:
- Equipment title area
- Function key buttons
- I/O or IO MONITOR button
- Manual button
- Auto button
- Alarm button
- Recipe or Setting button
- Exit button
- Status area if shown in the reference image
- Industrial colors and large readable buttons

## Navigation rule

For the first implementation, prefer this safe method:

- Main screen opens I/O screen as a separate window or child window.
- Keep a reference to the I/O window so it does not disappear immediately.
- If the I/O window is already open, bring it to the front instead of opening duplicates.

Possible implementation pattern:

self.io_window = None

def open_io_monitor(self):
    if self.io_window is None or not self.io_window.isVisible():
        self.io_window = IOMonitorWindow(parent=self)
    self.io_window.show()
    self.io_window.raise_()
    self.io_window.activateWindow()

## Response rule

When modifying this project, always proceed in small safe steps:

1. Inspect current files first.
2. Identify which file currently contains the I/O screen.
3. Do not rewrite the I/O screen.
4. Rename or move only when necessary.
5. Create the Main screen.
6. Connect the Main screen I/O button to the existing I/O screen.
7. Explain how to run and test.