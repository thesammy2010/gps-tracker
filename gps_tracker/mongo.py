import datetime
import json
import typing
import uuid

import bson
import pymongo

from gps_tracker import version
from gps_tracker.settings import CONFIG

MONGO_CLIENT: pymongo.MongoClient = pymongo.MongoClient(CONFIG.mongo_url, uuidRepresentation="standard")
MONGO_AUTH_CURSOR = MONGO_CLIENT[CONFIG.mongo_auth_database][CONFIG.mongo_auth_collection]
MONGO_DATA_CURSOR = MONGO_CLIENT[CONFIG.mongo_data_database][CONFIG.mongo_data_collection]


def look_up_user(username: str) -> typing.Dict[typing.Any, typing.Any]:
    data = MONGO_AUTH_CURSOR.find_one(filter={"username": username})
    # returns {user, key, salt, authorised}
    if data is None:
        return {}
    return dict(data)


def post_location_info(data: typing.Dict[str, typing.Any]) -> (str, bool, str):
    record = dict(data)
    record["_id"] = bson.ObjectId()
    record["id"] = uuid.uuid4()
    record["collectedAt"] = datetime.datetime.now(tz=datetime.timezone.utc)
    if "version" not in data:
        data["version"] = version
    try:
        result = MONGO_DATA_CURSOR.insert_one(document=record)
    except pymongo.errors.PyMongoError as e:
        return "", False, "Internal Server Error: Code 50001"
    return str(record["id"]), bool(result), ""


def get_latest_location_info(
    query_params: typing.Dict[str, typing.Any]
) -> (typing.Dict[typing.Any, typing.Any], bool, str):

    # handle uuid
    if "id" in query_params:
        query_params["id"] = uuid.UUID(query_params["id"])

    try:
        cur: pymongo.cursor.Cursor = MONGO_DATA_CURSOR.find(filter=query_params).sort("_id", -1).limit(1)
        for idx, data in enumerate(cur):  # once the cursor is evaluated once, you lose the value
            record: typing.Dict = dict(data)
            record["_id"] = str(record.get("_id", ""))
            return record, True, ""
        else:

            return {}, False, f"No record matches your filter: {json.dumps(dict(query_params))}"
    except pymongo.errors.PyMongoError as e:
        return {}, False, "Internal Server Error: Code 50002"


def ping() -> bool:
    return [
        MONGO_CLIENT[CONFIG.mongo_auth_database].command("ping"),
        MONGO_CLIENT[CONFIG.mongo_data_database].command("ping"),
    ].count({"ok": 1.0}) == 2
