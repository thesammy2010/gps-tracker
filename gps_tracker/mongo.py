import datetime
import typing

import bson
import pymongo

from gps_tracker.settings import CONFIG

MONGO_CLIENT: pymongo.MongoClient = pymongo.MongoClient(CONFIG.mongo_url)
MONGO_AUTH_CURSOR = MONGO_CLIENT[CONFIG.mongo_auth_database][CONFIG.mongo_auth_collection]
MONGO_DATA_CURSOR = MONGO_CLIENT[CONFIG.mongo_data_database][CONFIG.mongo_data_collection]


def look_up_user(username: str) -> typing.Dict[typing.Any, typing.Any]:
    data = MONGO_AUTH_CURSOR.find_one(filter={"username": username})
    # returns {user, key, salt, authorised}
    if data is None:
        return {}
    return dict(data)


def post_location_info(data: typing.Dict[str, typing.Any]) -> (str, bool):
    record = dict(data)
    record["_id"] = bson.ObjectId()
    record["collectedAt"] = datetime.datetime.now(tz=datetime.timezone.utc)
    result = MONGO_DATA_CURSOR.insert_one(document=record)
    return str(record["_id"]), bool(result)


def get_latest_location_info(device_id: str) -> typing.Dict[typing.Any, typing.Any]:
    # can be used to handle querying
    query_filter: typing.Dict[str, str] = {}
    if device_id:
        query_filter["device"] = device_id
    cur: pymongo.cursor.Cursor = MONGO_DATA_CURSOR.find(filter=query_filter).sort("_id", -1).limit(1)
    for idx, data in enumerate(cur):  # once the cursor is evaluated once, you lose the value
        record: typing.Dict = dict(data)
        record["_id"] = str(record.get("_id", ""))
        return record
    else:
        return {}


def ping() -> bool:
    return [
        MONGO_CLIENT[CONFIG.mongo_auth_database].command("ping"),
        MONGO_CLIENT[CONFIG.mongo_data_database].command("ping"),
    ].count({"ok": 1.0}) == 2
