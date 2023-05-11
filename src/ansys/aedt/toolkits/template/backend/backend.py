import logging

from flask import Flask
from flask import jsonify
from flask import request
import service_generic

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    desktop_connected, msg = service_generic.aedt_connected()
    if desktop_connected:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 200


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


@app.route("/installed_versions", methods=["GET"])
def installed_aedt_version_call():
    logger.info("[GET] /version (get the version)")
    return jsonify(service_generic.installed_aedt_version()), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions_call():
    logger.info("[GET] /aedt_sessions (aedt sessions for specific version)")

    response = service_generic.aedt_sessions()

    if isinstance(response, list):
        return jsonify(response), 200
    else:
        return jsonify(response), 500


@app.route("/launch_aedt", methods=["POST"])
def launch_aedt_call():
    logger.info("[POST] /launch_aedt (launch or connect AEDT)")

    response = service_generic.launch_aedt()

    if response:
        return jsonify(response), 200
    else:
        return jsonify("Fail to connect to AEDT"), 500


@app.route("/close_aedt", methods=["POST"])
def close_aedt_call():
    logger.info("[POST] /close_aedt (close AEDT)")

    body = request.json
    aedt_keys = ["close_projects", "close_on_exit"]
    if not body:
        return jsonify("body is empty!"), 500
    elif not isinstance(body, dict) or not all(item in body for item in set(aedt_keys)):
        return jsonify("body not correct"), 500

    close_projects = body["close_projects"]
    close_on_exit = body["close_on_exit"]
    response = service_generic.release_desktop(close_projects, close_on_exit)
    if response:
        return jsonify("AEDT correctly released"), 200
    else:
        return jsonify("AEDT is not connected"), 500


@app.route("/open_project", methods=["PUT"])
def open_project_call():
    logger.info("[PUT] /open_project (open an AEDT project)")

    response = service_generic.open_project()

    if response:
        return jsonify(response), 200
    else:
        return jsonify("Fail to connect to AEDT"), 500


if __name__ == "__main__":
    app.run(debug=service_generic.debug)
