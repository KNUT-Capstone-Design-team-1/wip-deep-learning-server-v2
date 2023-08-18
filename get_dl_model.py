import dotenv
import gdown
import os

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("dl_server.get_dl_model")
logger.setLevel(logging.DEBUG)

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

text_detect_model = os.getenv("TEXT_DETECT_URL")
pill_shape_model = os.getenv("PILL_SHAPE_URL")
pill_pre_model = os.getenv("PILL_PRE_URL")
text_recog_model = os.getenv("TEXT_RECOG_URL")

model_dir = os.getenv("MODEL_SAVE_DIR")

if (not os.path.isdir(model_dir)):
    os.mkdir(model_dir)

td_model_name = os.getenv("TEXT_DETECT_MODEL_NAME")
ps_model_name = os.getenv("PILL_SHAPE_MODEL_NAME")
ps_pre_model_name = os.getenv("PILL_PRE_MODEL_NAME")
tr_model_name = os.getenv("TEXT_RECOG_MODEL_NAME")

text_detect_file = gdown.download(
    text_detect_model, model_dir+'/'+td_model_name, quiet=False)
pill_shape_file = gdown.download(
    pill_shape_model, model_dir+'/'+ps_model_name, quiet=False)
pill_pre_file = gdown.download(
    pill_pre_model, model_dir+'/'+ps_pre_model_name, quiet=False)
text_recog_file = gdown.download(
    text_recog_model, model_dir+'/'+tr_model_name, quiet=False)

if text_detect_file is None:
    logger.error("Text Detect Model File Download Failed")

if pill_shape_file is None:
    logger.error("Pill Shape Model File Download Failed")

if pill_pre_file is None:
    logger.error("Pill Shape Pre Model File Download Failed")

if text_recog_file is None:
    logger.error("Text Recog Model File Download Failed")

logger.info("DL Models Download Complete!")
