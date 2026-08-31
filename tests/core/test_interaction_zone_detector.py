from app.core.enums.interaction_zone import InteractionZone
from app.core.models.point import Point


def test_interaction_zone_detector_detects_color_ring():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(100, 540)
    )

    assert zone == InteractionZone.COLOR_RING


def test_interaction_zone_detector_detects_eraser_ring():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(1820, 540)
    )

    assert zone == InteractionZone.ERASER_RING


def test_interaction_zone_detector_detects_undo_zone():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(480, 950)
    )

    assert zone == InteractionZone.UNDO


def test_interaction_zone_detector_detects_redo_zone():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(1440, 950)
    )

    assert zone == InteractionZone.REDO


def test_interaction_zone_detector_detects_canvas_zone():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(960, 540)
    )

    assert zone == InteractionZone.CANVAS


def test_interaction_zone_detector_detects_tool_ring():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(960, 80)
    )

    assert zone == InteractionZone.TOOL_RING


def test_interaction_zone_detector_prioritizes_color_ring_in_top_left_corner():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(100, 80)
    )

    assert zone == InteractionZone.COLOR_RING


def test_interaction_zone_detector_prioritizes_eraser_ring_in_top_right_corner():
    from app.application.services.interaction_zone_detector import (
        InteractionZoneDetector,
    )

    detector = InteractionZoneDetector(
        screen_width=1920,
        screen_height=1080,
    )

    zone = detector.detect(
        Point(1820, 80)
    )

    assert zone == InteractionZone.ERASER_RING
