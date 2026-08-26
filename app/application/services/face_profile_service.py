from app.application.services.profile_service import (
    ProfileService,
)
from app.core.models.application_state import ApplicationState
from app.storage.repositories.profile_repository import (
    ProfileRepository,
)


class FaceProfileService:

    def __init__(
        self,
        repository: ProfileRepository,
        state: ApplicationState,
        recognition,
        profile_service: ProfileService,
    ) -> None:
        self.repository = repository
        self.state = state
        self.recognition = recognition
        self.profile_service = profile_service

    def process(
        self,
        frame,
        faces,
    ):
        identities = [
            profile.face_identity
            for profile in self.repository.get_all()
            if profile.face_identity is not None
        ]

        results = self.recognition.recognize(
            frame=frame,
            faces=faces,
            identities=identities,
        )

        for result in results:
            if result.identity is None:
                continue

            profile = (
                self.profile_service
                .activate_profile_by_face_identity(
                    result.identity.id
                )
            )

            if profile is not None:
                break

        return results
