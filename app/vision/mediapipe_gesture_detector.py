import mediapipe as mp
import numpy as np


class MediaPipeGestureDetector:

    def __init__(
        self,
        recognizer=None,
        recognizer_factory=None,
    ):
        if recognizer is not None:
            self.recognizer = recognizer

        elif recognizer_factory is not None:
            self.recognizer = recognizer_factory()

        else:
            raise ValueError(
                "A recognizer or recognizer_factory is required."
            )

    def detect(self, image):
        if isinstance(image, mp.Image):
            media_image = image
        else:
            rgb_image = np.ascontiguousarray(
                np.asarray(image)[..., ::-1]
            )

            media_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_image,
            )

        return self.recognizer.recognize(
            media_image
        )
