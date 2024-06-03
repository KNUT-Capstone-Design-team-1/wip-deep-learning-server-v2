from mobile_sam import SamPredictor, sam_model_registry

import numpy as np


class SamModel:
    def __init__(self, checkpoint, device="cpu") -> None:
        self.model = sam_model_registry['vit_t'](checkpoint=checkpoint)
        self.model = self.model.to(device=device)
        self.model.eval()

        self.predictor = SamPredictor(self.model)
        self.masks = []

    def segment(self, image: np.ndarray, xyxy: np.ndarray) -> None:
        self.predictor.set_image(image)

        for box in xyxy:
            masks, scores, _ = self.predictor.predict(
                box=box,
                multimask_output=True
            )
            index = np.argmax(scores)
            self.masks.append(masks[index])

            del masks
            del scores

        self.predictor.reset_image()

    def segment_no_xyxy(self, image: np.ndarray) -> None:
        h, w = image.shape[:2]
        h = h//2
        w_c = w//2
        w1 = w_c - (w_c//2)
        w2 = w_c + (w_c//2)

        self.predictor.set_image(image)

        masks, scores, _ = self.predictor.predict(
            point_coords=np.array([[w1, h]]),
            point_labels=np.array([1]),
            multimask_output=True
        )

        idx = np.argmax(scores)
        self.masks.append(masks[idx])

        masks, scores, _ = self.predictor.predict(
            point_coords=np.array([[w2, h]]),
            point_labels=np.array([1]),
            multimask_output=True
        )

        idx = np.argmax(scores)
        self.masks.append(masks[idx])

        self.predictor.reset_image()

    def reset(self):
        self.masks = []
