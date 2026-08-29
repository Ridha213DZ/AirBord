from app.application.services.face_profile_service import (
    FaceProfileService,
)
from app.core.models.application_state import ApplicationState
from app.core.models.face_identity import FaceIdentity
from app.core.models.profile import Profile


class FakeProfileRepository:

    def __init__(self):
        self.profiles = []

    def get_all(self):
        return list(self.profiles)


class FakeFaceRecognition:

    def __init__(self, identity):
        self.identity = identity

    def recognize(
        self,
        frame,
        faces,
        identities,
    ):
        class Result:

            def __init__(
                self,
                identity,
            ):
                self.identity = identity

        return [
            Result(self.identity)
        ]


class FakeProfileService:

    def __init__(
        self,
        state,
    ):
        self.state = state
        self.received_face_identity_id = None
        self.profile_to_return = None

    def activate_profile_by_face_identity(
        self,
        face_identity_id,
    ):
        self.received_face_identity_id = (
            face_identity_id
        )

        if self.profile_to_return is not None:
            self.state.activate_profile(
                self.profile_to_return
            )

        return self.profile_to_return


def test_face_profile_service_activates_profile_for_recognized_face():
    repository = FakeProfileRepository()
    state = ApplicationState()

    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    profile = Profile(
        name="Ridha",
        face_identity=identity,
    )

    repository.profiles.append(profile)

    recognition = FakeFaceRecognition(
        identity=identity,
    )

    profile_service = FakeProfileService(
        state=state,
    )

    profile_service.profile_to_return = profile

    service = FaceProfileService(
        repository=repository,
        state=state,
        recognition=recognition,
        profile_service=profile_service,
    )

    service.process(
        frame=object(),
        faces=[object()],
    )

    assert state.current_profile is profile
    assert state.current_page is profile.current_page


def test_face_profile_service_does_not_activate_when_face_is_unknown():
    repository = FakeProfileRepository()
    state = ApplicationState()

    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    profile = Profile(
        name="Ridha",
        face_identity=identity,
    )

    repository.profiles.append(profile)

    recognition = FakeFaceRecognition(
        identity=None,
    )

    profile_service = FakeProfileService(
        state=state,
    )

    service = FaceProfileService(
        repository=repository,
        state=state,
        recognition=recognition,
        profile_service=profile_service,
    )

    service.process(
        frame=object(),
        faces=[object()],
    )

    assert state.current_profile is None
    assert state.current_page is None
    assert (
        profile_service.received_face_identity_id
        is None
    )


def test_face_profile_service_passes_profile_face_identities_to_recognition():
    repository = FakeProfileRepository()
    state = ApplicationState()

    first_identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    second_identity = FaceIdentity(
        embedding=[0.4, 0.5, 0.6],
    )

    repository.profiles.extend(
        [
            Profile(
                name="Ridha",
                face_identity=first_identity,
            ),
            Profile(
                name="Ahmed",
                face_identity=second_identity,
            ),
            Profile(
                name="Without Face",
            ),
        ]
    )

    class InspectingFaceRecognition:

        def __init__(self):
            self.received_identities = None

        def recognize(
            self,
            frame,
            faces,
            identities,
        ):
            self.received_identities = identities

            return []

    recognition = InspectingFaceRecognition()

    profile_service = FakeProfileService(
        state=state,
    )

    service = FaceProfileService(
        repository=repository,
        state=state,
        recognition=recognition,
        profile_service=profile_service,
    )

    service.process(
        frame=object(),
        faces=[],
    )

    assert recognition.received_identities == [
        first_identity,
        second_identity,
    ]


def test_face_profile_service_activates_profile_through_profile_service():
    repository = FakeProfileRepository()
    state = ApplicationState()

    identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    profile = Profile(
        name="Ridha",
        face_identity=identity,
    )

    repository.profiles.append(profile)

    recognition = FakeFaceRecognition(
        identity=identity,
    )

    profile_service = FakeProfileService(
        state=state,
    )

    profile_service.profile_to_return = profile

    service = FaceProfileService(
        repository=repository,
        state=state,
        recognition=recognition,
        profile_service=profile_service,
    )

    service.process(
        frame=object(),
        faces=[object()],
    )

    assert (
        profile_service.received_face_identity_id
        == identity.id
    )


def test_face_profile_service_continues_after_unactivatable_recognized_face():
    repository = FakeProfileRepository()
    state = ApplicationState()

    first_identity = FaceIdentity(
        embedding=[0.1, 0.2, 0.3],
    )

    second_identity = FaceIdentity(
        embedding=[0.4, 0.5, 0.6],
    )

    first_profile = Profile(
        name="First",
        face_identity=first_identity,
    )

    second_profile = Profile(
        name="Second",
        face_identity=second_identity,
    )

    repository.profiles.extend(
        [
            first_profile,
            second_profile,
        ]
    )

    class MultipleResultRecognition:

        def recognize(
            self,
            frame,
            faces,
            identities,
        ):
            class Result:

                def __init__(
                    self,
                    identity,
                ):
                    self.identity = identity

            return [
                Result(first_identity),
                Result(second_identity),
            ]

    class SelectiveProfileService(FakeProfileService):

        def activate_profile_by_face_identity(
            self,
            face_identity_id,
        ):
            self.received_face_identity_id = (
                face_identity_id
            )

            if face_identity_id == second_identity.id:
                self.state.activate_profile(
                    second_profile
                )

                return second_profile

            return None

    recognition = MultipleResultRecognition()

    profile_service = SelectiveProfileService(
        state=state,
    )

    service = FaceProfileService(
        repository=repository,
        state=state,
        recognition=recognition,
        profile_service=profile_service,
    )

    service.process(
        frame=object(),
        faces=[object()],
    )

    assert state.current_profile is second_profile
    assert state.current_page is second_profile.current_page
    assert (
        profile_service.received_face_identity_id
        == second_identity.id
    )
