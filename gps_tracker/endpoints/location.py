import flask

from gps_tracker.auth import is_user_authenticated
from gps_tracker.mongo import get_latest_location_info, post_location_info


def request() -> flask.Response:

    message, access, code = is_user_authenticated(flask.request.headers)
    if not access:
        # unauthorised
        return flask.make_response(message, code)

    match flask.request.method:
        case "GET":
            data = get_latest_location_info(device_id=flask.request.args.get("device_id", ""))
            flask.make_response(flask.jsonify(data), 200)
        case "POST", "PUT":
            # discord
            if flask.request.args.get("discord", True):
                # do discord stuff to post data once available in Mongo
                pass
            req_id, success = post_location_info(flask.request.form)
            if success:
                flask.make_response({"request_id": req_id}, 200)
            else:
                flask.make_response({"error": "failed to record result"}, 500)
        case "DELETE":
            # this is separate as I will eventually want to support it
            return flask.make_response(
                f'HTTP Verb %s is not yet supported for this API' % flask.request.method,
                405
            )
        case _:
            return flask.make_response(
                f'{"error": "HTTP Verb %s is not supported, please use one of [GET, POST, PUT]}' % flask.request.method,
                405
            )
