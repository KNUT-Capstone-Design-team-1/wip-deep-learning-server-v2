import gdown
from pathlib import Path

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("dl_server.get_dl_model")
logger.setLevel(logging.DEBUG)

model_dir = Path("./weights")

if not model_dir.exists():
    model_dir.mkdir(parents=True)

# gdino_url = ''
mobilesam_url = 'https://drive.google.com/uc?id=18qsUfxAeAVYkoJDSpRnZxJ1UrFsEXKh9'
cls_url = 'https://drive.google.com/uc?id=170N8pvLeqLugZC_Eo4u8WGiqR6ExcLnS'

# gdino_model_path = str(model_dir / 'pre_gdino_model.pth')
mobilesam_model_path = str(model_dir / 'mobile_sam.pt')
cls_model_path = str(model_dir / 'pill_cls_model.pt')

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
    mobilesam_model_path,
    quiet=False,
)

cls_file = gdown.download(
    cls_url,
    cls_model_path,
    quiet=False,
)


# if gdino_file is None:
#     logger.error("Gdino File Download Failed")

if mobilesam_file is None:
    logger.error("MobileSam File Download Failed")

if cls_file is None:
    logger.error("Cls File Download Failed")

logger.info("DL Models Download Complete!")
