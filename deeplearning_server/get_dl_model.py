import gdown
import os

text_detect_model = 'https://drive.google.com/uc?id=1Jk4eGD7crsqCCg9C9VjCLkMN3ze8kutZ'
pill_shape_model = 'https://drive.google.com/uc?id=12U-grcJXRO6YtLwp3GWBbe-FSWT8B4su'
text_recog_model = 'https://drive.google.com/uc?id=1yLixadZ_3Ls4x_TR0-8MG6-iQSEn5ZSG'

model_dir = './deeplearning_server/weights'

if(not os.path.isdir(model_dir)):
    os.mkdir(model_dir)

td_model_name = 'craft_mlt_25k.pth'
ps_model_name = 'pill_shape_fine_tuned.pt'
tr_model_name = 'pill_recog_model.pth'

gdown.download(text_detect_model, model_dir+'/'+td_model_name, resume=True)
gdown.download(pill_shape_model, model_dir+'/'+ps_model_name)
gdown.download(text_recog_model, model_dir+'/'+tr_model_name)
