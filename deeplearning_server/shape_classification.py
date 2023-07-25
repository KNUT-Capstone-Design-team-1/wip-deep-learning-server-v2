import torchvision.transforms as transforms
import torch
from efficientnet_pytorch import EfficientNet

import numpy as np
from PIL import Image


class ShapeClassification:
    def __init__(self, model_path):
        # 신경망 초기화
        model_name = 'efficientnet-b7'

        # 학습된 모델 불러오기
        self.model = EfficientNet.from_pretrained(model_name, num_classes=2)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()

    def transform_image(self, image_data):
        # 이미지 전처리
        my_transforms = transforms.Compose([
            transforms.Grayscale(3),
            transforms.Resize(224),
            transforms.ToTensor()])
        image = Image.fromarray(image_data, 'RGB')
        # image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        return my_transforms(image).unsqueeze(0)

    def detect_pill_shape(self, img_data):
        try:
            # 이미지 전처리
            inputs = self.transform_image(image_data=img_data)

            # 알약 모양 예측
            outputs = self.model(inputs)
            # 결과를 사용가능하게 변환
            _, predict = torch.max(outputs, 1)
            if int(predict.numpy()) == 0:
                pill_shape = "원형"
            else:
                pill_shape = "타원형"
            return pill_shape
        except:
            print("shape_classification error")
