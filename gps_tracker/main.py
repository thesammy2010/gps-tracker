import flask
import flask_restful
import waitress

from gps_tracker.endpoints.location import request
from gps_tracker.endpoints.health import Health
from gps_tracker.settings import CONFIG


APP = flask.Flask(__name__)
API = flask_restful.Api(APP)

API.add_resource(Health, "/health")


@APP.route("/location", methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def location():
    resp = request()
    # print(resp.data) for any debugging
    return resp


def serve() -> None:
    if CONFIG.flask_env == "PRODUCTION":
        waitress.serve(APP, host="0.0.0.0", port=CONFIG.port)
    else:
        APP.run(debug=True, host="0.0.0.0", port=CONFIG.port)


if __name__ == "__main__":
    serve()
