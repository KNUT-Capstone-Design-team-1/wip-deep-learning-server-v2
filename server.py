import dotenv
import json
import os
import gc

from flask import Flask, request, jsonify

from utils.json_encoder import JsonEncoder

from pill_predictor import PillPredictor

import logging
import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("dl_server")

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

# 포트 번호 불러오기
port_num = os.getenv("DL_SERVER_PORT")

logger.info(f'port: {port_num}')

# flask 초기설정
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/recognition", methods=['POST'])
def get_pill():
    # json from request
    params = request.get_json()

    pill_predictor.set_image_form_json(params)
    del params

    if pill_predictor.image is not None:

        try:
            pill_predictor.predict()

        except Exception as e:
            logger.debug("Error: pill predict")
            return jsonify({"success": False, "message": error_msg["error.predict"]}), 200

        pill_json = json_encoder.make_json(
            pill_predictor.cls_model.item_seqs
        )

        pill_predictor.reset()

        gc.collect()

        logger.debug(pill_json)

        return jsonify(pill_json), 200
    else:
        logger.debug("No Image")
        return jsonify({"success": False, "message": error_msg["error.no-image"]}), 200


@app.errorhandler(500)
def error_500(e):
    logger.debug(e)
    return jsonify({"success": False, "message": error_msg["error.general"]}), 500


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"success": False, "message": error_msg["error.api-not-found"]}), 404


if __name__ == '__main__':
    try:
        pill_predictor = PillPredictor()

        logger.debug("Pill Shape Model Load Success!")

        json_encoder = JsonEncoder()

        # error-msg 사전 불러오기
        with open("error-msg.json", "r") as f:
            error_msg: dict = json.load(f)

    except Exception as e:
        logger.error(f'Failed Load Model: {e}')

    app.run(host="0.0.0.0", port=port_num)
