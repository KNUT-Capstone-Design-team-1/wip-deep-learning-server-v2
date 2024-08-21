# DL Server Flask

## Information

- server.py : flask server file
- pill_predictor.py : pill detect and recognition, models load, base64 to image

#### utils

- image_preprocess.py : image process
- json_encoder.py : result to json

#### models

- sam_model.py : mobile segmentation model config
- yolo_model.py : yolov8 model config
- ~~gdino_model.py : grounding dino model config~~ **(beta / not service)**

---

## Model

### Pill segmentation

- Use [Mobile_SAM](https://github.com/ChaoningZhang/MobileSAM) pretrained model

### Pill classification

- Use [Yolov8](https://github.com/ultralytics/ultralytics) fine-tuning with custom data

---

## How to Start

### Models download

```
pip3 install -r ./requirements.txt
python3 ./get_dl_model.py
```

## Flask default

- port : 16262
  - if you want change port number update .env port number

## Train / Test Enviroment

- OS : Windows 10
- GPU : rtx 3060
- CUDA : 11.7
- python == 3.8.19
- pytorch == 2.0.0 / torchvision == 0.15.1
