import argparse
import os
import torch
from torch.autograd import Variable
import cv2
import numpy as np
from CRAFT_pytorch import craft_utils, imgproc
from CRAFT_pytorch.craft import CRAFT

import wp_utils

from collections import OrderedDict

'''
- trained_model  : 학습된 모델 지정
- text_threshold : text 영역 신뢰도, 지정된 정확도 이상의 text 영역 검출
- low_text       : text 영역의 점수, 지정된 점수를 기준으로 영역을 지정, 낮을수록 범위를 넓게 지정
- link_threshold : 단일 text간 연결 신뢰도, 지정된 정확도 이상의 text 영역 검출
- pill_folder    : 이미지 폴더
- canvas_size    : resize 이미지 최대 크기 전처리, mag_ratio * img(height or width)와 비교하여 더 작은 크기를 사용
- mag_ratio      : 이미지 배율, 보통 작은 이미지를 확대하기 위해 사용, 0이하면 이미지를 축소
'''


class DetectText:
    def __init__(self, model_path):
        torch.set_num_threads(2)
        self.trained_model = model_path
        self.text_threshold = 0.4
        self.low_text = 0.1
        self.link_threshold = 0.4
        # self.pill_folder = "./pill_image/"
        self.canvas_size = 1280
        self.mag_ratio = 0.2
        # 신경망 초기화
        self.net = CRAFT()

        # 학습된 모델 불러오기(cpu사용)
        self.net.load_state_dict(self.copyStateDict(
            torch.load(self.trained_model, map_location='cpu')))
        self.net.eval()

    # 모델의 module 파라미터만 불러오기
    def copyStateDict(self, state_dict):
        if list(state_dict.keys())[0].startswith("module"):
            start_idx = 1
        else:
            start_idx = 0
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = ".".join(k.split(".")[start_idx:])
            new_state_dict[name] = v
        return new_state_dict

    def detect_net(self, image):
        # 이미지 resize
        img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(
            image, self.canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio=self.mag_ratio)

        ratio_h = ratio_w = 1 / target_ratio

        # 이미지 전처리
        x = imgproc.normalizeMeanVariance(img_resized)
        x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
        x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]

        # 이미지 text 영역 예측
        with torch.no_grad():
            y, feature = self.net(x)

        # text 영역과 신뢰도(정확도), text 연결성과 신뢰도(정확도) 분할
        score_text = y[0, :, :, 0].cpu().data.numpy()
        score_link = y[0, :, :, 1].cpu().data.numpy()

        # 지정된 신뢰도(정확도)에 따른 text 영역 좌표 확인
        boxes, polys = craft_utils.getDetBoxes(
            score_text, score_link, self.text_threshold, self.link_threshold, self.low_text)

        # 입력된 이미지에 맞추어 text 영역 비율 조정
        boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
        polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
        for k in range(len(polys)):
            if polys[k] is None:
                polys[k] = boxes[k]

        return boxes, polys

    def crop_img(self, img, boxes):
        imgCrops = []
        dst = img.copy()
        for i, box in enumerate(boxes):
            # text 영역 좌표를 int32로 변환
            poly = np.array(box).astype(np.int32)
            # minAreaRect연산을 위한 shape 변환
            rectBox = box.astype(np.int32).reshape(4, 1, 2)
            # center 좌표 확인
            # (중심 뿐만아니라 각도도 반환하지만 기준점에 따라 달라지기 때문에 중심좌표만 사용)
            rect = cv2.minAreaRect(rectBox)
            rect_center = rect[0]
            try:
                # crop 이미지 수평화
                imgCrop = wp_utils.rotate_img(dst, poly, rect_center)
                imgCrops.append(imgCrop)
            except:
                print('error')
        return imgCrops

    def detect_text_img(self, pill_image):

        try:
            image = pill_image
            # text 영역 검출
            _, polys = self.detect_net(image)
            # 검출된 text영역에 맞게 crop
            crop_files = self.crop_img(image[:, :, ::-1], polys)

            return crop_files
        except:
            print('no image')
            return []
