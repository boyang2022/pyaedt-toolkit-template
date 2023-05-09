import logging

from common.properties import properties
from flask import Flask
from flask import jsonify
from flask import request
import service_generic

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    return jsonify("I am healthy"), 200


@app.route("/installed_versions", methods=["GET"])
def installed_aedt_version_call():
    logger.info("[GET] /version (get the version)")
    return jsonify(service_generic.installed_aedt_version()), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions_call():
    logger.info("[GET] /get_aedt_sessions (get aedt sessions)")
    return jsonify(service_generic.aedt_sessions()), 200


@app.route("/set_properties", methods=["PUT"])
def set_properties_call():
    logger.info("[PUT] /set_properties (set toolkit properties)")

    body = request.json
    success, msg = service_generic.set_properties(body)
    if success:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/get_properties", methods=["GET"])
def get_properties_call():
    logger.info("[GET] /get_properties (get toolkit properties)")
    return jsonify(service_generic.get_properties()), 200


# @app.route("/new_aedt_instance", methods=["GET", "POST"])
# def new_aedt_instance():
#     if request.method == "POST":
#         body = request.json
#         properties.aedt_version = body["general"]["aedt_version"]
#         properties.non_graphical = body["general"]["non_graphical"]
#     logger.info("[POST] /new_aedt_instance (Open an AEDT new instance)")
#     return json.dumps("project {} must be loaded".format(new_aedt()))


if __name__ == "__main__":
    app.run(debug=properties.debug)
