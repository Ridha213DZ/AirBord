from app.core.enums.hand_gesture import HandGesture
from app.core.models.hand_gesture_event import HandGestureEvent
from app.core.models.point import Point


class HandGestureRecognizer:

    MIN_CONFIDENCE = 0.5

    def recognize(
        self,
        gesture_name: str,
        confidence: float,
        position: Point | None = None,
    ) -> HandGestureEvent | None:

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "Confidence must be between 0.0 and 1.0."
            )

        if confidence < self.MIN_CONFIDENCE:
            return None

        if gesture_name == "Open_Palm":
            gesture = HandGesture.OPEN

        elif gesture_name == "Closed_Fist":
            gesture = HandGesture.FIST

        else:
            raise ValueError(
                f"Unknown hand gesture: {gesture_name}"
            )

        return HandGestureEvent(
            gesture=gesture,
            position=position,
            confidence=confidence,
        )

    def recognize_mediapipe(
        self,
        result,
    ) -> HandGestureEvent | None:

        if (
            not result.gestures
            or not result.gestures[0]
        ):
            return None

        if (
            not result.hand_landmarks
            or not result.hand_landmarks[0]
        ):
            return None

        category = result.gestures[0][0]
        landmark = result.hand_landmarks[0][0]

        return self.recognize(
            gesture_name=category.category_name,
            confidence=category.score,
            position=Point(
                x=landmark.x,
                y=landmark.y,
            ),
        )
