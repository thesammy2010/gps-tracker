import typing
import datetime

import bson
import pymongo

from gps_tracker.settings import Config


mongo_client: pymongo.MongoClient = pymongo.MongoClient(Config.mongo_url)
MONGO_AUTH_CURSOR = mongo_client[Config.mongo_auth_database][Config.mongo_auth_collection]
MONGO_DATA_CURSOR = mongo_client[Config.mongo_data_database][Config.mongo_data_collection]


def look_up_user(username: str) -> typing.Dict[typing.Any, typing.Any]:
    data = MONGO_AUTH_CURSOR.find_one(filter={"username": username})
    # returns {user, key, salt}
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
    query_filter = {}
    if device_id:
        query_filter["device"] = device_id
    cur: pymongo.cursor.Cursor = MONGO_DATA_CURSOR.find(filter=query_filter).sort("_id", -1).limit(1)
    record = list(cur)[0]
    record["_id"] = str(record.get("_id", ""))
    return dict(record)
