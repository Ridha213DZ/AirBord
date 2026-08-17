from dataclasses import dataclass


@dataclass
class DrawingSettings:
    color: str = "#000000"

    brush_size: float = 5.0

    eraser_enabled: bool = False

    def enable_eraser(self) -> None:
        self.eraser_enabled = True

    def disable_eraser(self) -> None:
        self.eraser_enabled = False