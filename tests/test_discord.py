import datetime
import typing
import unittest
from unittest import mock

import pytest
import requests

from gps_tracker.discord import (format_url, func_map, generate_content,
                                 post_to_discord)


class TestGenerateContent:
    @pytest.mark.parametrize(
        "key,input_value,expected_result",
        [
            ("_id", "1234", "1234"),
            ("accuracy", 1.23456, "1.23 m"),
            ("activity", "", ""),
            ("altitude", 150.123, "150.1 m"),
            ("battery", 22.0, "22 %"),
            ("collectedAt", datetime.datetime(2021, 10, 4), "2021-10-04 00:00:00"),
            ("latitude", 45.1234567890, "45.12346 °"),
            ("longitude", 45.1234567890, "45.12346 °"),
            ("provider", "network", "network"),
            ("speed", 23.45678, "23.46 m/s"),
            ("direction", 45.678, "45.7 °"),
        ],
    )
    def test_generate_func_maps(
        self, key: str, input_value: str | float | datetime.datetime, expected_result: str
    ) -> None:
        assert expected_result == func_map[key](input_value)

    @pytest.mark.parametrize(
        "input_data,expected_result",
        [
            ({"_id": "73616c74"}, [{"name": "🌐 Request ID", "value": "73616c74"}]),
            ({"accuracy": 1.23456}, [{"name": "🔍 Accuracy", "value": "1.23 m"}]),
            ({"activity": ""}, []),
            ({"altitude": 150.123}, [{"name": "⛰️ Altitude", "value": "150.1 m"}]),
            ({"battery": 22.0}, [{"name": "🔋 Battery", "value": "22 %"}]),
            ({"collectedAt": datetime.datetime(2021, 10, 4)}, [{"name": "⏱️ Time", "value": "2021-10-04 00:00:00"}]),
            ({"device": "iPhone"}, [{"name": "📱 Device", "value": "iPhone"}]),
            ({"latitude": 45.1234567890}, [{"name": "📡 Latitude", "value": "45.12346 °"}]),
            ({"longitude": 45.1234567890}, [{"name": "📡 Longitude", "value": "45.12346 °"}]),
            ({"direction": 45.678}, [{"name": "🧭 Direction", "value": "45.7 °"}]),
            ({"provider": "network"}, [{"name": "🛰️ GPS source", "value": "network"}]),
            ({"speed": 23.45678}, [{"name": "🏃 Speed", "value": "23.46 m/s"}]),
        ],
    )
    def test_generate_content(self, input_data: typing.Dict, expected_result: typing.List[typing.Dict]) -> None:
        assert expected_result == generate_content(input_data)


class TestDiscord(unittest.TestCase):
    def test_format_url(self) -> None:
        self.assertEqual("https://google.com/maps?q=1.234,5.678", format_url(latitude=1.234, longitude=5.678))

    @mock.patch("requests.request")
    def test_post_to_discord(self, mocked_reqs: mock.MagicMock) -> None:
        resp: requests.models.Response = requests.models.Response  # type: ignore
        resp.ok = True
        mocked_reqs.return_value = resp()

        input_data: typing.Dict[str, float] = {"latitude": 45.1234567890, "longitude": 45.1234567890}
        expected_json_payload: typing.Dict = {
            "content": None,
            "embeds": [
                {
                    "title": "Location",
                    "description": "Click here",
                    "url": "https://google.com/maps?q=45.123456789,45.123456789",
                    "color": 5814783,
                    "image": {"url": "https://images.app.goo.gl/w2giEUuRNdHahSvb6"},
                    "thumbnail": {"url": "https://images.app.goo.gl/w2giEUuRNdHahSvb6"},
                },
                {
                    "title": "Location Info",
                    "color": 15172872,
                    "fields": [
                        {"name": "📡 Latitude", "value": "45.12346 °"},
                        {"name": "📡 Longitude", "value": "45.12346 °"},
                    ],
                },
            ],
            "username": "GPS Tracking Service",
            "avatar_url": (
                "https://media.istockphoto.com/vectors/"
                "satellite-icon-black-minimalist-icon-isolated-on-white-background-vector-id867290448"
            ),
        }

        self.assertTrue(post_to_discord(location_data=input_data))
        mocked_reqs.assert_called_once_with(
            method="POST",
            url="https://discordapp.com/api/webhooks/",
            headers={"Content-Type": "application/json"},
            json=expected_json_payload,
        )
