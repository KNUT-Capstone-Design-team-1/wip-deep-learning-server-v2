from groundingdino.util.inference import Model

import torch
import torchvision
import supervision as sv

import numpy as np

from memory_profiler import profile


class GdinoModel:
    def __init__(self, checkpoint, device="cpu") -> None:

        self.model = Model(
            model_config_path="./models/config/GroundingDINO_SwinT_OGC.py",
            model_checkpoint_path=checkpoint,
            device=device
        )

    @profile
    def predict(self, image: np.ndarray, classes: list, box_threshold=0.25, text_threshold=0.15) -> sv.Detections:

        detections = self.model.predict_with_classes(
            image=image,
            classes=classes,
            box_threshold=box_threshold,
            text_threshold=text_threshold
        )

        nms_idx = torchvision.ops.nms(
            torch.from_numpy(detections.xyxy),
            torch.from_numpy(detections.confidence),
            0.8
        ).detach().cpu().numpy().tolist()

        detections.xyxy = detections.xyxy[nms_idx]
        detections.confidence = detections.confidence[nms_idx]
        detections.class_id = detections.class_id[nms_idx]

        return detections
