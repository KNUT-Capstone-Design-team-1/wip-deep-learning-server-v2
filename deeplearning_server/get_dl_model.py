import gdown
import os

import dotenv
env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

text_detect_model = os.getenv("TEXT_DETECT_URL")
pill_shape_model = os.getenv("PILL_SHAPE_URL")
text_recog_model = os.getenv("TEXT_RECOG_URL")

model_dir = os.getenv("MODEL_SAVE_DIR")

if (not os.path.isdir(model_dir)):
    os.mkdir(model_dir)

td_model_name = os.getenv("TEXT_DETECT_MODEL_NAME")
ps_model_name = os.getenv("PILL_SHAPE_MODEL_NAME")
tr_model_name = os.getenv("TEXT_RECOG_MODEL_NAME")

gdown.download(text_detect_model, model_dir+'/'+td_model_name, quiet=False)
gdown.download(pill_shape_model, model_dir+'/'+ps_model_name, quiet=False)
gdown.download(text_recog_model, model_dir+'/'+tr_model_name, quiet=False)
