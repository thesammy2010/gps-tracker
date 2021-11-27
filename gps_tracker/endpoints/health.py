import flask
import flask_restful


class Health(flask_restful.Resource):
    def get(self) -> flask.Response:
        return flask.make_response("alive", 200)
