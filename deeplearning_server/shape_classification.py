from pill_shape_model.models import ResNet18
import torchvision.transforms as transforms
import torch

import numpy as np
from PIL import Image


def transform_image(image_data):
    # 이미지 전처리
    my_transforms = transforms.Compose([
        transforms.Grayscale(3),
        transforms.Resize(224),
        transforms.ToTensor()])
    image = Image.fromarray(image_data, 'RGB')
    # image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return my_transforms(image).unsqueeze(0)


def detect_pill_shape(img_data):
    # 신경망 초기화
    model = ResNet18(2)

    # 학습된 모델 불러오기
    model.load_state_dict(torch.load('./deeplearning_server/weights/pill_shape_fine_tuned.pt', map_location='cpu'))
    model.eval()

    try:
        # 이미지 전처리
        inputs = transform_image(image_data=img_data)

        # 알약 모양 예측
        outputs = model(inputs)
        # 결과를 사용가능하게 변환
        _, predict = torch.max(outputs, 1)
        if int(predict.numpy()) == 0:
            pill_shape = "원형"
        else:
            pill_shape = "타원형"
        return pill_shape
    except:
        print("shape_classification error")
