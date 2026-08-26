from app.vision.face_pipeline import FacePipeline
from app.vision.models.detected_face import DetectedFace


class FakeFaceDetector:
    def detect(self, frame):
        return [
            DetectedFace(
                x=50,
                y=50,
                width=80,
                height=80,
                confidence=0.95,
            ),
            DetectedFace(
                x=300,
                y=100,
                width=150,
                height=150,
                confidence=0.90,
            ),
        ]


class FakeFaceSelector:

    def __init__(self):
        self.received_faces = None
        self.received_target_region = None
        self.selected_face = None

    def select(
        self,
        faces,
        target_region=None,
    ):
        self.received_faces = faces
        self.received_target_region = target_region

        return self.selected_face


def test_face_pipeline_detects_faces_and_selects_one():
    detector = FakeFaceDetector()
    selector = FakeFaceSelector()

    pipeline = FacePipeline(
        detector=detector,
        selector=selector,
    )

    frame = object()

    faces = detector.detect(frame)

    selector.selected_face = faces[1]

    selected = pipeline.process(frame)

    assert selector.received_faces == faces
    assert selected is selector.selected_face


def test_face_pipeline_passes_target_region_to_selector():
    detector = FakeFaceDetector()
    selector = FakeFaceSelector()

    pipeline = FacePipeline(
        detector=detector,
        selector=selector,
    )

    frame = object()

    target_region = (
        200,
        100,
        300,
        300,
    )

    pipeline.process(
        frame,
        target_region=target_region,
    )

    assert selector.received_target_region == target_region


def test_face_pipeline_returns_none_when_no_face_is_selected():
    detector = FakeFaceDetector()
    selector = FakeFaceSelector()

    selector.selected_face = None

    pipeline = FacePipeline(
        detector=detector,
        selector=selector,
    )

    frame = object()

    result = pipeline.process(
        frame,
    )

    assert result is None


def test_face_pipeline_returns_none_when_no_faces_are_detected():
    class EmptyFaceDetector:
        def detect(self, frame):
            return []

    detector = EmptyFaceDetector()
    selector = FakeFaceSelector()

    pipeline = FacePipeline(
        detector=detector,
        selector=selector,
    )

    frame = object()

    result = pipeline.process(frame)

    assert result is None
    assert selector.received_faces is None


def test_face_pipeline_produces_detected_face():
    detector = FakeFaceDetector()
    selector = FakeFaceSelector()

    expected_face = detector.detect(object())[1]
    selector.selected_face = expected_face

    pipeline = FacePipeline(
        detector=detector,
        selector=selector,
    )

    result = pipeline.process(
        object(),
    )

    assert result is expected_face
    assert isinstance(
        result,
        DetectedFace,
    )
