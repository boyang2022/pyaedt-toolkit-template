from flask import Flask
from flask import jsonify
from flask import request

from ansys.aedt.toolkits.template.backend.common.logger_handler import logger
from ansys.aedt.toolkits.template.backend.service import ToolkitService

service = ToolkitService()
settings = service.get_properties()

app = Flask(__name__)


# Generic services


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    desktop_connected, msg = service.aedt_connected()
    if desktop_connected:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 200


@app.route("/get_status", methods=["GET"])
def get_status_call():
    logger.info("[GET] /get_status (check if the step is running)")
    exit_code, msg = service.get_thread_status()
    if exit_code <= 0:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/get_properties", methods=["GET"])
def get_properties_call():
    app.logger.info("[GET] /get_properties (get toolkit properties)")
    return jsonify(service.get_properties()), 200


@app.route("/set_properties", methods=["PUT"])
def set_properties_call():
    app.logger.info("[PUT] /set_properties (set toolkit properties)")

    body = request.json
    success, msg = service.set_properties(body)
    if success:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/installed_versions", methods=["GET"])
def installed_aedt_version_call():
    logger.info("[GET] /version (get the version)")
    return jsonify(service.installed_aedt_version()), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions_call():
    logger.info("[GET] /aedt_sessions (aedt sessions for specific version)")

    response = service.aedt_sessions()

    if isinstance(response, list):
        return jsonify(response), 200
    else:
        return jsonify(response), 500


@app.route("/launch_aedt", methods=["POST"])
def launch_aedt_call():
    logger.info("[POST] /launch_aedt (launch or connect AEDT)")

    response = service.launch_aedt()

    if response:
        return jsonify("AEDT launched"), 200
    else:
        return jsonify("Fail to launch to AEDT"), 500


@app.route("/connect_aedt", methods=["PUT"])
def connect_aedt_call():
    logger.info("[PUT] /connect_aedt (connect to an existing AEDT session)")

    response = service.connect_aedt()
    if response:
        return jsonify("AEDT session connected"), 200
    else:
        return jsonify("AEDT session not connected"), 500


@app.route("/close_aedt", methods=["POST"])
def close_aedt_call():
    logger.info("[POST] /close_aedt (close AEDT)")

    body = request.json
    aedt_keys = ["close_projects", "close_on_exit"]
    if not body:
        msg = "body is empty!"
        logger.error(msg)
        return jsonify(msg), 500
    elif not isinstance(body, dict) or not all(item in body for item in set(aedt_keys)):
        msg = "body not correct"
        logger.error(msg)
        return jsonify(msg), 500

    close_projects = body["close_projects"]
    close_on_exit = body["close_on_exit"]
    response = service.release_desktop(close_projects, close_on_exit)
    if response:
        return jsonify("AEDT correctly released"), 200
    else:
        return jsonify("AEDT is not connected"), 500


@app.route("/connect_design", methods=["POST"])
def connect_design_call():
    logger.info("[POST] /connect_design (connect or create a design)")

    body = request.json

    aedt_apps = [
        "Circuit",
        "Hfss",
        "Edb",
        "Emit",
        "Hfss",
        "Hfss3dLayout",
        "Icepak",
        "Maxwell2d",
        "Maxwell3d",
        "MaxwellCircuit",
        "Q2d",
        "Q3d",
        "Rmxprt",
        "Simplorer",
    ]
    if not body:
        msg = "body is empty!"
        logger.error(msg)
        return jsonify("body is empty!"), 500
    elif body["aedtapp"] not in aedt_apps:
        msg = "body not correct"
        logger.error(msg)
        return jsonify(msg), 500

    response = service.connect_design(body["aedtapp"])

    if response:
        return jsonify("Design connected"), 200
    else:
        return jsonify("Fail to connect to the design"), 500


@app.route("/save_project", methods=["POST"])
def save_project_call():
    logger.info("[POST] /save_project (Save AEDT project)")

    response = service.save_project()
    if response:
        return jsonify("Project saved"), 200
    else:
        return jsonify(response), 500
