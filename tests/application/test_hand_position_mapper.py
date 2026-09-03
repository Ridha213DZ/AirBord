from app.application.hand_position_mapper import HandPositionMapper
from app.core.models.point import Point


def test_hand_position_mapper_converts_normalized_position_to_pixels():
    mapper = HandPositionMapper()

    result = mapper.map(
        position=Point(
            x=0.25,
            y=0.5,
        ),
        width=1920,
        height=1080,
    )

    assert result == Point(
        x=480.0,
        y=540.0,
    )


def test_hand_position_mapper_scales_position_for_different_target_sizes():
    mapper = HandPositionMapper()

    position = Point(
        x=0.25,
        y=0.5,
    )

    result = mapper.map(
        position=position,
        width=1280,
        height=720,
    )

    assert result == Point(
        x=320.0,
        y=360.0,
    )


def test_hand_position_mapper_maps_normalized_boundaries_to_canvas_boundaries():
    mapper = HandPositionMapper()

    top_left = mapper.map(
        position=Point(
            x=0.0,
            y=0.0,
        ),
        width=1920,
        height=1080,
    )

    bottom_right = mapper.map(
        position=Point(
            x=1.0,
            y=1.0,
        ),
        width=1920,
        height=1080,
    )

    assert top_left == Point(
        x=0.0,
        y=0.0,
    )

    assert bottom_right == Point(
        x=1919.0,
        y=1079.0,
    )
