import flask
import flask_restful

from gps_tracker.mongo import ping


class Health(flask_restful.Resource):
    def get(self) -> flask.Response:
        if flask.request.args.get("db", False):
            db_healthy = ping()
            response = {"db": db_healthy}
            response_code = 200 if db_healthy else 500
            return flask.make_response(response, response_code)
        return flask.make_response("alive", 200)
