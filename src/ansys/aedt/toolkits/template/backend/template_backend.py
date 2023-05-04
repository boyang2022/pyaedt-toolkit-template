import json
import logging

from flask import Flask
from flask import request
from template_service import get_version

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    return "I am healthy"


# This return the version of the backend service.
@app.route("/version", methods=["GET"])
def get_ver():
    logger.info("[GET] /version (get the version)")
    return json.dumps(str(get_version()))


@app.route("/launch_aedt", methods=["GET", "POST"])
def launch_aedt():
    if not request.method == "GET":
        # Load the configuration file
        config = request.json
        project_name = config["project_name"]
        design_name = config["design_name"]
        units = config["units"]

    return {"message": "AEDT launched successfully"}


if __name__ == "__main__":
    app.run(debug=True)
