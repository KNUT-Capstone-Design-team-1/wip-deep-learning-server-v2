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

model_dir = os.getenv("MODEL_SAVE_DIR")

if (not os.path.isdir(model_dir)):
    os.mkdir(model_dir)

# gdino_url = os.getenv("GDINO_URL")
mobilesam_url = os.getenv("MOBILESAM_URL")
cls_url = os.getenv("CLS_URL")

# gdino_model_name = os.getenv("GDINO_CKPT")
mobilesam_model_name = os.getenv("MOBILESAM_CKPT")
cls_model_name = os.getenv("CLS_CKPT")

# gdino_file = gdown.download(
#     gdino_url,
#     os.path.join(
#         model_dir,
#         gdino_model_name
#     ),
#     quiet=False
# )

mobilesam_file = gdown.download(
    mobilesam_url,
    os.path.join(
        model_dir,
        mobilesam_model_name
    ),
    quiet=False,
)

cls_file = gdown.download(
    cls_url,
    os.path.join(
        model_dir,
        cls_model_name
    ),
    quiet=False,
)


# if gdino_file is None:
#     logger.error("Gdino File Download Failed")

if mobilesam_file is None:
    logger.error("MobileSam File Download Failed")

if cls_file is None:
    logger.error("Cls File Download Failed")

logger.info("DL Models Download Complete!")
