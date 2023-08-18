import dotenv
from flask import Flask, request, jsonify
import json
import base64
import os
from PIL import Image
from io import BytesIO
import numpy as np
import wp_utils
from detect_text import DetectText
from text_recog import RecogText
from shape_classification import ShapeClassification

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("dl_server.dl_main")

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

# 모델들 파일 경로 불러오기
model_dir = os.getenv("MODEL_SAVE_DIR")

td_model_path = os.path.join(model_dir, os.getenv("TEXT_DETECT_MODEL_NAME"))
ps_model_path = os.path.join(model_dir, os.getenv("PILL_SHAPE_MODEL_NAME"))
tr_model_path = os.path.join(model_dir, os.getenv("TEXT_RECOG_MODEL_NAME"))

# 포트 번호 불러오기
port_num = os.getenv("DL_PORT_NUMBER")

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# get_json 함수 호출 주소 및 형식 지정


@app.route("/data", methods=['POST'])
def get_json():
    # json 데이터 받기
    params = request.get_json()

    pill_img = decode_image(params)

    # 이미지 저장 확인
    if (pill_img is not None):
        crop_files = detect_text.detect_text_img(
            pill_img)  # 이미지 안의 text 영역 crop
        pill_text = text_recog.img_text_recog(crop_files)  # crop한 text 분석
        pill_shape = shape_classification.detect_pill_shape(
            pill_img)  # 알약의 모양 분석

        # 알약의 특징 정보를 json 파일로 저장
        json_data = wp_utils.make_json(
            pill_shape=pill_shape, pill_text=pill_text)

        # with open('pill_data.json', 'r') as pill_data:
        #   json_data = json.load(pill_data)

        # 메인서버로 알약 검색을 위한 json 데이터 반환
        return jsonify(json_data)

    else:
        logger.debug("No Image")
        return jsonify({"is_success": False, "message": "Image Wirte Failed"}, 500)


def decode_image(imjson):
    try:
        # base64 데이터를 이미지로 변환(decoding)
        pill_Image = Image.open(
            BytesIO(base64.b64decode(imjson['img_base64'])))
        pill_Image = np.array(pill_Image)

        return pill_Image

    except:
        logger.debug("Image Write Failed")
        return None


@app.errorhandler(500)
def error_500():
    return jsonify({"is_success": False, "message": "Server not work"}, 500)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"is_success": False, "message": "page not found"}, 404)


if __name__ == '__main__':
    try:
        detect_text = DetectText(td_model_path)
        logger.debug("Text Detect Model Load Success!")
        text_recog = RecogText(tr_model_path)
        logger.debug("Text Recog Model Load Success!")
        shape_classification = ShapeClassification(ps_model_path)
        logger.debug("Pill Shape Model Load Success!")
    except Exception as e:
        logger.error(f'Failed Load Model {e}')
    app.logger.info("server start :: PORT=" + str(port_num))
    app.run(host="0.0.0.0", port=port_num)
