from flask import Flask, request, jsonify
import json, base64, os
from PIL import Image
from io import BytesIO
import numpy as np
import wp_utils
import detect_text, text_recog, shape_classification

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# get_json 함수 호출 주소 및 형식 지정
@app.route("/data", methods=['POST'])
def get_json():
  # json 데이터 받기
  params = request.get_json()
  
  pill_img = decode_image(params)

  # 이미지 저장 확인
  if(pill_img is not None):
    crop_files = detect_text.detect_text_img(pill_img) # 이미지 안의 text 영역 crop
    pill_text = text_recog.img_text_recog(crop_files) # crop한 text 분석
    pill_shape = shape_classification.detect_pill_shape(pill_img) # 알약의 모양 분석
    
    # 알약의 특징 정보를 json 파일로 저장 
    json_data = wp_utils.make_json(pill_shape=pill_shape, pill_text=pill_text)
    
    # with open('pill_data.json', 'r') as pill_data:
    #   json_data = json.load(pill_data)
    
    # 메인서버로 알약 검색을 위한 json 데이터 반환
    return jsonify(json_data)
  
  else:
    print("image write failed")
    return "image write failed"

def decode_image(imjson):
  try:
    # base64 데이터를 이미지로 변환(decoding)
    pill_Image = Image.open(BytesIO(base64.b64decode(imjson['img_base64'])))
    pill_Image = np.array(pill_Image)
    
    return pill_Image
  
  except:
    print("No image")
    return None

if __name__ == '__main__':
  app.run(host="0.0.0.0", port="5000")
