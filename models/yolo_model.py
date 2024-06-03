from ultralytics import YOLO
from PIL import Image
from typing import List


class YoloModel:
    def __init__(self, checkpoint, device):
        self.model = YOLO(checkpoint)
        self.device = device
        self.item_seqs = {}

    def reset(self):
        self.item_seqs = {}

    def predict(self, images: List[Image.Image]):

        # for image in images:
        results = self.model.predict(
            images,
            imgsz=320,
            device=self.device,
            save=False,
            verbose=False
        )

        for r in results:
            item_conf = r.probs.top5conf.tolist()
            for idx, conf in zip(r.probs.top5, item_conf):
                if r.names[idx] not in self.item_seqs:
                    self.item_seqs[r.names[idx]] = 0

                self.item_seqs[r.names[idx]] += conf

        del results
