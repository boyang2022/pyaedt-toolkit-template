import json
import logging

from common.properties import properties
from flask import Flask
from flask import jsonify
from flask import request
import service

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    return jsonify("I am healthy"), 200


@app.route("/installed_versions", methods=["GET"])
def get_installed_versions():
    logger.info("[GET] /version (get the version)")
    return jsonify(str(service.get_installed_aedt_version())), 200


@app.route("/new_aedt_instance", methods=["GET", "POST"])
def new_aedt_instance():
    if request.method == "POST":
        body = request.json
        properties.aedt_version = body["general"]["aedt_version"]
        properties.non_graphical = body["general"]["non_graphical"]
    logger.info("[POST] /new_aedt_instance (Open an AEDT new instance)")
    return json.dumps("project {} must be loaded".format(new_aedt()))


if __name__ == "__main__":
    app.run(debug=properties.debug)
