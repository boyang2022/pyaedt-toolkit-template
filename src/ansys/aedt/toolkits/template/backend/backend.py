from ansys.aedt.toolkits.template.backend.common.backend_generic import app
from ansys.aedt.toolkits.template.backend.common.backend_generic import jsonify
from ansys.aedt.toolkits.template.backend.common.backend_generic import logger
from ansys.aedt.toolkits.template.backend.common.backend_generic import service
from ansys.aedt.toolkits.template.backend.common.backend_generic import settings
from ansys.aedt.toolkits.template.backend.common.multithreading_server import MultithreadingServer

# Toolkit services


@app.route("/create_geometry", methods=["POST"])
def create_geometry_call():
    logger.info("[POST] /create_geometry (create a box or sphere in HFSS)")

    response = service.create_geometry()
    if response:
        return jsonify("Geometry created"), 200
    else:
        return jsonify("Geometry not created"), 500


if __name__ == "__main__":
    app.debug = True
    server = MultithreadingServer()
    server.run(host=settings["url"], port=settings["port"], app=app)
