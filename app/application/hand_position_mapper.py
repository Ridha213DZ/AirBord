from app.core.models.point import Point


class HandPositionMapper:

    def map(
        self,
        position: Point,
        width: int,
        height: int,
    ) -> Point:
        return Point(
            x=min(
                position.x * width,
                width - 1,
            ),
            y=min(
                position.y * height,
                height - 1,
            ),
        )
