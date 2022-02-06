import flask
import flask_restful
import waitress

from gps_tracker import version
from gps_tracker.endpoints.health import Health
from gps_tracker.endpoints.location import request
from gps_tracker.settings import CONFIG

APP = flask.Flask(__name__)
API = flask_restful.Api(APP)
API_PATH: str = f"/api/v{version}"

API.add_resource(Health, f"{API_PATH}/health")


@APP.route(f"{API_PATH}/location", methods=["GET", "PUT", "PATCH", "POST", "DELETE"])
def location():
    resp = request()
    return resp


@APP.route("/<path:path>")
def default_resolve(path: str = ""):
    # eventually will build a 302 to /home once implemented
    return flask.make_response({"error": "This path does not exist"}, 404)


def serve() -> None:
    if CONFIG.flask_env == "PRODUCTION":
        waitress.serve(APP, host="0.0.0.0", port=int(CONFIG.port))
    else:
        APP.run(debug=True, host="0.0.0.0", port=int(CONFIG.port))


if __name__ == "__main__":
    serve()
