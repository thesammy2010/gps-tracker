import flask
import flask_restful
import waitress

from gps_tracker.endpoints.location import request
from gps_tracker.endpoints.health import Health
from gps_tracker.settings import CONFIG


APP = flask.Flask(__name__)
API = flask_restful.Api(APP)

API.add_resource(Health, "/health")
# API.add_resource(Location, "/location", )


@APP.route("/location")
def location():
    return request()


def serve() -> None:
    if CONFIG.environment == "PRODUCTION":
        waitress.serve(APP, host="0.0.0.0", port=CONFIG.port)
    else:
        APP.run(debug=True, host="0.0.0.0", port=CONFIG.port)


if __name__ == "__main__":
    serve()
