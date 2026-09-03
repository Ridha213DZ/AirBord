from app.application.canvas_coordinate_mapper import (
    CanvasCoordinateMapper,
)
from app.core.models.point import Point


def test_canvas_coordinate_mapper_converts_screen_point_to_canvas_local_point():
    mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    result = mapper.map(
        Point(
            x=960.0,
            y=540.0,
        )
    )

    assert result == Point(
        x=672.0,
        y=378.0,
    )


def test_canvas_coordinate_mapper_maps_canvas_boundaries():
    mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    top_left = mapper.map(
        Point(
            x=288.0,
            y=162.0,
        )
    )

    bottom_right = mapper.map(
        Point(
            x=1632.0,
            y=918.0,
        )
    )

    assert top_left == Point(
        x=0.0,
        y=0.0,
    )

    assert bottom_right == Point(
        x=1344.0,
        y=756.0,
    )


def test_canvas_coordinate_mapper_rejects_point_outside_canvas():
    mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    result = mapper.map(
        Point(
            x=100.0,
            y=540.0,
        )
    )

    assert result is None


import pytest


@pytest.mark.parametrize(
    "position",
    [
        Point(x=960.0, y=100.0),
        Point(x=960.0, y=1000.0),
        Point(x=100.0, y=540.0),
        Point(x=1800.0, y=540.0),
    ],
)
def test_canvas_coordinate_mapper_rejects_points_in_all_tool_margins(
    position,
):
    mapper = CanvasCoordinateMapper(
        screen_width=1920,
        screen_height=1080,
        margin_ratio=0.15,
    )

    result = mapper.map(position)

    assert result is None
