import typing

import flask

from gps_tracker.auth import is_user_authenticated
from gps_tracker.discord import post_to_discord
from gps_tracker.mongo import get_latest_location_info, post_location_info


def validate_request(params: typing.Dict, data: typing.Dict) -> (str, bool, typing.Dict[str, typing.Any]):
    allowed_fields: typing.List[str] = [
        "latitude",
        "longitude",
        "device",
        "accuracy",
        "battery",
        "speed",
        "direction",
        "altitude",
        "provider",
        "activity",
        "appid",
        "version",
    ]
    numeric_fields: typing.List[str] = [
        "latitude",
        "longitude",
        "accuracy",
        "battery",
        "speed",
        "direction",
        "altitude",
    ]

    for field in data.keys():
        if field not in allowed_fields:
            return f"field <{field}> is not supported", False, {}

    if "appid" not in params:
        return "appid must be sent as a parameter in the request", False, {}

    if not data:
        return "payload must not be empty", False, {}

    for field in numeric_fields:
        if field in data:
            try:
                float(data.get(field))
            except (ValueError, TypeError):
                return (
                    f"field <{field}> of value <{data.get('value')}> of type <{type(data.get('value')).__name__}>"
                    " must be numeric",
                    False,
                    {},
                )

    data["appid"] = params["appid"]

    return "", True, {i: (float(j) if i in numeric_fields else j) for i, j in data.items() if i in allowed_fields}


def request() -> flask.Response:
    message, access, code = is_user_authenticated(flask.request.headers)
    if not access:
        # unauthorised
        return flask.make_response({"error": message}, code)

    match flask.request.method:
        case "GET":
            data, success, err = get_latest_location_info(query_params=flask.request.args)
            match (success, err):
                case (True, ""):
                    return flask.make_response(flask.jsonify(dict(data)), 200)
                case (False, "Internal Server Error: Code 50002"):
                    return flask.make_response({"error": err}, 500)
                case (False, _):
                    return flask.make_response({"error": err}, 400)

        case "POST" | "PUT":
            error, is_valid, data = validate_request(
                params=flask.request.args, data=flask.request.json or flask.request.form
            )
            if not is_valid:
                return flask.make_response({"error": error}, 400)

            req_id, mongo_post_success, err = post_location_info(data)
            if not flask.request.args.get("discord") is True:
                if mongo_post_success:
                    return flask.make_response({"request_id": req_id}, 200)
                else:
                    return flask.make_response({"error": err}, 500)

            data["_id"] = req_id
            discord_post_success = post_to_discord(location_data=data)

            match (mongo_post_success, discord_post_success):
                case (True, True):
                    return flask.make_response({"request_id": req_id}, 200)
                case (True, False):
                    return flask.make_response({"error": "failed to post result to discord"}, 500)
                case (False, True):
                    return flask.make_response({"error": "failed to record result in database"}, 500)
                case (False, False):
                    return flask.make_response(
                        {"errors": ["failed to post result to discord", "failed to record result in database"]}, 500
                    )
                case _:
                    return flask.make_response({"error": "Unknown internal error"}, 500)
        case _:
            return flask.make_response(
                '{"error": "HTTP Verb '
                + flask.request.method
                + ' is not supported, please use one of GET, POST, PUT"}',
                405,
            )
