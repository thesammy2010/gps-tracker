import typing
import datetime

import pymongo
from bson import ObjectId

from gps_tracker.settings import Config


mongo_client: pymongo.MongoClient = pymongo.MongoClient(Config.mongo_url)
MONGO_AUTH_CURSOR = mongo_client[Config.mongo_auth_database][Config.mongo_auth_collection]
MONGO_DATA_CURSOR = mongo_client[Config.mongo_data_database][Config.mongo_data_collection]


def look_up_user(username: str) -> typing.Dict[typing.Any, typing.Any]:
    data = MONGO_AUTH_CURSOR.find_one(filter={"username": username})
    # returns {user, key, salt}
    return dict(data)


def post_location_info(record: typing.Dict[str, typing.Any]) -> (bool, str):
    record["_id"] = ObjectId()
    record["collectedAt"] = datetime.datetime.now(tz=datetime.timezone.utc)
    result = MONGO_DATA_CURSOR.insert_one(document=record)
    return bool(result), str(record["_id"])


def get_latest_location_info(device_id: str) -> typing.Dict[typing.Any, typing.Any]:
    # can be used to handle querying
    query_filter = {}
    if device_id:
        query_filter["device"] = device_id
    cur: pymongo.cursor.Cursor = MONGO_DATA_CURSOR.find(filter=query_filter).sort("_id", -1).limit(1)
    record = list(cur)[0]
    return dict(record)
