from datetime import datetime
from uuid import UUID

from app.core.models.face_identity import FaceIdentity
from app.core.models.page import Page
from app.core.models.point import Point
from app.core.models.profile import Profile
from app.core.models.stroke import Stroke


class ProfileSerializer:
    """
    Converts Profile domain objects to JSON-compatible dictionaries
    and reconstructs them back into domain objects.
    """

    # ============================================================
    # Public API
    # ============================================================

    @classmethod
    def to_dict(
        cls,
        profile: Profile,
    ) -> dict:
        """
        Convert a Profile domain object into
        a JSON-compatible dictionary.
        """

        return {
            "id": str(profile.id),
            "name": profile.name,
            "face_identity": cls._face_identity_to_dict(
                profile.face_identity
            ),
            "pages": [
                cls._page_to_dict(page)
                for page in profile.pages
            ],
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> Profile:
        """
        Reconstruct a Profile domain object
        from serialized dictionary data.
        """

        face_identity_data = data.get(
            "face_identity"
        )

        face_identity = None

        if face_identity_data is not None:
            face_identity = (
                cls._face_identity_from_dict(
                    face_identity_data
                )
            )

        pages = [
            cls._page_from_dict(page_data)
            for page_data in data.get(
                "pages",
                [],
            )
        ]

        return Profile(
            id=UUID(data["id"]),
            name=data.get(
                "name",
                "",
            ),
            face_identity=face_identity,
            pages=pages,
            created_at=cls._parse_datetime(
                data["created_at"]
            ),
            updated_at=cls._parse_datetime(
                data["updated_at"]
            ),
        )

    # ============================================================
    # FaceIdentity
    # ============================================================

    @classmethod
    def _face_identity_to_dict(
        cls,
        face_identity: FaceIdentity | None,
    ) -> dict | None:

        if face_identity is None:
            return None

        return {
            "id": str(face_identity.id),
            "embedding": list(
                face_identity.embedding
            ),
            "image_path": (
                face_identity.image_path
            ),
            "created_at": (
                face_identity.created_at.isoformat()
            ),
        }

    @classmethod
    def _face_identity_from_dict(
        cls,
        data: dict,
    ) -> FaceIdentity:

        return FaceIdentity(
            id=UUID(data["id"]),
            embedding=list(
                data.get(
                    "embedding",
                    [],
                )
            ),
            image_path=data.get(
                "image_path"
            ),
            created_at=cls._parse_datetime(
                data["created_at"]
            ),
        )

    # ============================================================
    # Page
    # ============================================================

    @classmethod
    def _page_to_dict(
        cls,
        page: Page,
    ) -> dict:

        return {
            "id": str(page.id),
            "strokes": [
                cls._stroke_to_dict(stroke)
                for stroke in page.strokes
            ],
            "created_at": (
                page.created_at.isoformat()
            ),
            "updated_at": (
                page.updated_at.isoformat()
            ),
        }

    @classmethod
    def _page_from_dict(
        cls,
        data: dict,
    ) -> Page:

        strokes = [
            cls._stroke_from_dict(
                stroke_data
            )
            for stroke_data in data.get(
                "strokes",
                [],
            )
        ]

        return Page(
            id=UUID(data["id"]),
            strokes=strokes,
            created_at=cls._parse_datetime(
                data["created_at"]
            ),
            updated_at=cls._parse_datetime(
                data["updated_at"]
            ),
        )

    # ============================================================
    # Stroke
    # ============================================================

    @classmethod
    def _stroke_to_dict(
        cls,
        stroke: Stroke,
    ) -> dict:

        return {
            "id": str(stroke.id),
            "points": [
                cls._point_to_dict(point)
                for point in stroke.points
            ],
            "color": stroke.color,
            "width": stroke.width,
            "created_at": (
                stroke.created_at.isoformat()
            ),
        }

    @classmethod
    def _stroke_from_dict(
        cls,
        data: dict,
    ) -> Stroke:

        points = [
            cls._point_from_dict(
                point_data
            )
            for point_data in data.get(
                "points",
                [],
            )
        ]

        return Stroke(
            id=UUID(data["id"]),
            points=points,
            color=data.get(
                "color",
                "#000000",
            ),
            width=data.get(
                "width",
                5.0,
            ),
            created_at=cls._parse_datetime(
                data["created_at"]
            ),
        )

    # ============================================================
    # Point
    # ============================================================

    @classmethod
    def _point_to_dict(
        cls,
        point: Point,
    ) -> dict:

        return {
            "x": point.x,
            "y": point.y,
        }

    @classmethod
    def _point_from_dict(
        cls,
        data: dict,
    ) -> Point:

        return Point(
            x=data["x"],
            y=data["y"],
        )

    # ============================================================
    # Utilities
    # ============================================================

    @staticmethod
    def _parse_datetime(
        value: str,
    ) -> datetime:

        return datetime.fromisoformat(
            value
        )