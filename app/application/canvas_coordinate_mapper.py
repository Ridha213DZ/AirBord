from app.core.models.point import Point


class CanvasCoordinateMapper:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        margin_ratio: float = 0.15,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin_ratio = margin_ratio

        self.left = screen_width * margin_ratio
        self.top = screen_height * margin_ratio

        self.width = screen_width * (
            1.0 - 2.0 * margin_ratio
        )
        self.height = screen_height * (
            1.0 - 2.0 * margin_ratio
        )

    def map(
        self,
        position: Point,
    ) -> Point | None:
        if (
            position.x < self.left
            or position.x > self.left + self.width
            or position.y < self.top
            or position.y > self.top + self.height
        ):
            return None

        return Point(
            x=position.x - self.left,
            y=position.y - self.top,
        )
