from dataclasses import dataclass, field

from app.core.enums.application_mode import ApplicationMode
from app.core.models.drawing_settings import DrawingSettings
from app.core.models.gesture_event import GestureEvent
from app.core.models.page import Page
from app.core.models.profile import Profile


@dataclass
class ApplicationState:
    mode: ApplicationMode = ApplicationMode.IDLE

    current_profile: Profile | None = None

    current_page: Page | None = None

    drawing_settings: DrawingSettings = field(
        default_factory=DrawingSettings
    )

    active_gesture: GestureEvent | None = None

    def activate_profile(
        self,
        profile: Profile,
    ) -> None:

        self.current_profile = profile
        self.current_page = profile.current_page

        self.mode = (
            ApplicationMode.PROFILE_ACTIVE
        )

    def activate_drawing(self) -> None:

        if self.current_profile is None:
            raise RuntimeError(
                "Cannot enter drawing mode "
                "without an active profile."
            )

        if self.current_page is None:
            self.current_page = (
                self.current_profile.current_page
            )

        self.mode = ApplicationMode.DRAWING

    def clear_profile(self) -> None:

        self.current_profile = None
        self.current_page = None
        self.active_gesture = None

        self.mode = ApplicationMode.IDLE