import numpy as np
import cv2
import base64

from memory_profiler import profile


class JsonDecoder:
    def __init__(self) -> None:
        pass

    @profile
    def decode_image(self, jd: dict) -> np.ndarray:
        try:
            image = cv2.imdecode(
                np.fromstring(
                    base64.b64decode(jd['base64']),
                    np.uint8
                ),
                cv2.IMREAD_COLOR
            )
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            return image

        except Exception as e:
            print(e)
            return None
