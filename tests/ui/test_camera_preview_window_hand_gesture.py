import numpy as np

from PySide6.QtWidgets import QApplication

from app.core.enums.application_mode import ApplicationMode
from app.core.enums.hand_gesture import HandGesture
from app.core.models.application_state import ApplicationState
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point
from app.ui.camera_preview_window import CameraPreviewWindow


def test_camera_preview_window_sends_camera_frame_to_hand_gesture_pipeline_in_drawing_mode():
    app = QApplication.instance() or QApplication([])

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    class FakeCameraFrameSource:

        def __init__(self, frame):
            self.frame = frame

        def read(self):
            return self.frame

    class FakeHandGesturePipeline:

        def __init__(self):
            self.received_frame = None

        def process(self, frame):
            self.received_frame = frame
            return None

    state = ApplicationState()
    state.mode = ApplicationMode.DRAWING

    source = FakeCameraFrameSource(
        frame=frame,
    )

    pipeline = FakeHandGesturePipeline()

    window = CameraPreviewWindow(
        source=source,
        application_state=state,
        hand_gesture_pipeline=pipeline,
    )

    window.update_frame()

    assert pipeline.received_frame is frame


def test_camera_preview_window_does_not_run_face_detection_in_drawing_mode():
    app = QApplication.instance() or QApplication([])

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    class FakeCameraFrameSource:

        def read(self):
            return frame

    class FakeFaceDetector:

        def __init__(self):
            self.called = False

        def detect(self, frame):
            self.called = True
            return []

    class FakeHandGesturePipeline:

        def process(self, frame):
            return None

    state = ApplicationState()
    state.mode = ApplicationMode.DRAWING

    face_detector = FakeFaceDetector()

    window = CameraPreviewWindow(
        source=FakeCameraFrameSource(),
        face_detector=face_detector,
        application_state=state,
        hand_gesture_pipeline=(
            FakeHandGesturePipeline()
        ),
    )

    window.update_frame()

    assert face_detector.called is False


def test_camera_preview_window_forwards_hand_gesture_event_to_controller():
    app = QApplication.instance() or QApplication([])

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8,
    )

    class FakeSource:

        def __init__(self, frame):
            self.frame = frame

        def read(self):
            return self.frame

    class FakePipeline:

        def __init__(self, event):
            self.event = event
            self.received_frame = None

        def process(self, frame):
            self.received_frame = frame
            return self.event

    class FakeController:

        def __init__(self):
            self.received_event = None

        def handle(self, event):
            self.received_event = event

    state = ApplicationState()
    state.mode = ApplicationMode.DRAWING

    event = HandGestureEvent(
        gesture=HandGesture.FIST,
        position=Point(500, 400),
        confidence=0.95,
    )

    source = FakeSource(frame)
    pipeline = FakePipeline(event)
    controller = FakeController()

    window = CameraPreviewWindow(
        source=source,
        application_state=state,
        hand_gesture_pipeline=pipeline,
        hand_gesture_controller=controller,
    )

    window.update_frame()

    assert controller.received_event == event
