import datetime
import typing
import uuid
from unittest import mock

import pytest

from gps_tracker.endpoints.location import validate_request

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
        err, valid, data = validate_request(
            params={"appid": "integration-test"},
            data={"device": "integration-test", "version": "1.0.0"},
        )
        assert valid, err
        req_id, result, err = post_location_info(data)
        assert result, err
        assert req_id

        mongo_data = MONGO_DATA_CURSOR.find_one(filter={"id": uuid.UUID(req_id)})
        print(mongo_data)
        del mongo_data["id"]
        del mongo_data["_id"]
        del mongo_data["collectedAt"]

        assert data == mongo_data

    @pytest.mark.integration
    def test_ping(self) -> None:
        assert ping()

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "query_params,expected_value",
        [
            (
                {},
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
                },
            ),
            ({"device": "unknown device"}, {}),
            (
                {"device": "Android"},
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
                },
            ),
            (
                {"device": "iPhone"},
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
                },
            ),
        ],
    )
    def test_get_latest_location_info(self, query_params: typing.Dict[str, str], expected_value: typing.Dict) -> None:
        (
            data,
            *_,
        ) = get_latest_location_info(query_params=query_params)

        for col in ["_id", "id", "collectedAt"]:
            if col in data:
                del data[col]

        if not query_params:
            assert data
        else:
            assert expected_value == data
