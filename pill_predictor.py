from pathlib import Path

import torch
import base64
import numpy as np
import cv2

from typing import Dict

from utils.json_encoder import JsonEncoder
from utils.image_preprocess import ImagePreprocess

from models.gdino_model import GdinoModel
from models.sam_model import SamModel
from models.yolo_model import YoloModel


class PillPredictor:
    def __init__(self) -> None:

        # 모델 불러오기 & 설정
        model_dir = Path("./weights")

        # gdino_checkpoint = model_dir / "pre_gdino_model.pth"
        sam_checkpoint = model_dir / "mobile_sam.pt"
        cls_checkpoint = model_dir / "pill_cls_model.pt"

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.gdino_classes = ["pill"]

        # self.gdino_model = GdinoModel(str(gdino_checkpoint), device)
        self.sam_model = SamModel(str(sam_checkpoint), device)
        self.cls_model = YoloModel(str(cls_checkpoint), device)

        self.json_encoder = JsonEncoder()
        self.image_preprocess = ImagePreprocess()

        self.image = None

    def set_image_form_json(self, params: Dict):
        try:
            self.image = cv2.imdecode(
                np.fromstring(
                    base64.b64decode(params['base64']),
                    np.uint8
                ),
                cv2.IMREAD_COLOR
            )
        except Exception as e:
            print(e)

    def reset(self):
        self.image = None
        self.sam_model.reset()
        self.image_preprocess.reset()
        self.cls_model.reset()

    def predict(self):
        # Find Pill
        # detections = gdino_model.predict(
        #     image=self.image,
        #     classes=self.gdino_classes,
        #     box_threshold=0.25,
        #     text_threshold=0.15
        # )

        # # Segmentation Pill: Get Mask
        # self.sam_model.segment(
        #     image=self.image,
        #     xyxy=detections.xyxy
        # )
        # detections.mask = np.array(self.sam_model.masks)

        # # Preprocess for Classification
        # self.image_preprocess.get_masked_image(
        #     self.image, detections
        # )

        self.sam_model.segment_no_xyxy(
            self.image
        )

        self.image_preprocess.get_masked_image_no_detections(
            self.image,
            self.sam_model.masks
        )

        self.cls_model.predict(
            self.image_preprocess.masked_images
        )
