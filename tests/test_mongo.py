import datetime
import typing
from unittest import mock

import pytest

from gps_tracker.mongo import (  # isort: skip
    get_latest_location_info,
    look_up_user,
    ping,
    post_location_info,
    MONGO_DATA_CURSOR,
)


class TestMongo:
    @pytest.mark.parametrize(
        "username,expected_value",
        [
            (
                "username",
                {
                    "username": "username",
                    "salt": "73616c74",
                    "key": "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8",
                    "authorised": True,
                },
            ),
            (
                "username2",
                {
                    "username": "username2",
                    "salt": "73616c74",
                    "key": "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8",
                    "authorised": False,
                },
            ),
            ("username3", {}),
        ],
    )
    @pytest.mark.integration
    def test_look_up_user(self, username: str, expected_value: typing.Dict) -> None:
        result = look_up_user(username=username)
        if "_id" in result:
            del result["_id"]  # this is dynamic
        assert expected_value == result

    @mock.patch("gps_tracker.mongo.datetime")
    @pytest.mark.integration
    def test_post_location_info(self, mocked_time) -> None:
        frozen_time: datetime.datetime = datetime.datetime(2021, 11, 28)
        mocked_time.datetime.now.return_value = frozen_time
        data = {"device": "integration-test", "collectedAt": frozen_time}
        req_id, result = post_location_info(data)
        assert result

        # fetch data from mongo
        mongo_data = MONGO_DATA_CURSOR.find_one_and_delete(filter=data)
        del mongo_data["_id"]

        assert data == mongo_data

    @pytest.mark.integration
    def test_ping(self) -> None:
        assert ping()

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "device_id,expected_value",
        [
            (
                "",
                {
                    "latitude": "0",
                    "longitude": "1",
                    "device": "Android",
                    "accuracy": "3",
                    "battery": "4",
                    "speed": "5",
                    "direction": "6",
                    "altitude": "7",
                    "provider": "data",
                    "activity": "n/a",
                    "collectedAt": datetime.datetime(2021, 11, 5, 0, 0, 0),
                },
            ),
            ("unknown device", {}),
            (
                "Android",
                {
                    "latitude": "0",
                    "longitude": "1",
                    "device": "Android",
                    "accuracy": "3",
                    "battery": "4",
                    "speed": "5",
                    "direction": "6",
                    "altitude": "7",
                    "provider": "data",
                    "activity": "n/a",
                    "collectedAt": datetime.datetime(2021, 11, 5, 0, 0, 0),
                },
            ),
            (
                "iPhone",
                {
                    "latitude": "45",
                    "longitude": "30",
                    "device": "iPhone",
                    "accuracy": "20",
                    "battery": "95",
                    "speed": "2",
                    "direction": "12",
                    "altitude": "50",
                    "provider": "data",
                    "activity": "n/a",
                    "collectedAt": datetime.datetime(2021, 11, 4, 0, 0, 0),
                },
            ),
        ],
    )
    def test_get_latest_location_info(self, device_id: str, expected_value: typing.Dict) -> None:
        data = get_latest_location_info(device_id=device_id)
        if data.get("_id", None):
            del data["_id"]
        assert expected_value == data
