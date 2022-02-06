import datetime
import typing
from unittest import mock

import flask
import pytest

from gps_tracker.endpoints.location import validate_request
from gps_tracker.main import APP


class TestValidateRequest:
    valid_data: typing.Dict[str, str | datetime.datetime] = {
        "_id": "615b4e4b1ad5da6788c3ea6e",
        "id": "50e09373d0e1146ed58d05d70550bb279d9b9d9a760215c4278440204ddb6909",
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
        "collectedAt": "Fri, 05 Nov 2021 00:00:00 GMT",
    }

    @pytest.mark.parametrize(
        "params,data,expected1,expected2,expected3",
        [
            pytest.param({}, {}, "appid must be sent as a parameter in the request", False, {}),
            pytest.param({"app": "example"}, {}, "appid must be sent as a parameter in the request", False, {}),
            pytest.param({"appid": "test-data"}, {"_id": valid_data["_id"]}, "field <_id> is not supported", False, {}),
            pytest.param(
                {"appid": "test-data"},
                {"device": valid_data["device"]},
                "",
                True,
                {"device": valid_data["device"], "appid": "test-data"},
            ),
            pytest.param(
                {"appid": "test-data"},
                {"latitude": valid_data["latitude"]},
                "",
                True,
                {"latitude": 0.0, "appid": "test-data"},
            ),
            pytest.param(
                {"appid": "test-data"},
                {"latitude": None},
                "field <latitude> of value <None> of type <NoneType> must be numeric",
                False,
                {},
            ),
        ],
    )
    def test_validate_request(
        self, params: typing.Dict, data: typing.Dict, expected1: typing.Dict, expected2: bool, expected3: typing.Dict
    ) -> None:
        res1, res2, res3 = validate_request(params=params, data=data)
        assert expected1 == res1
        assert expected2 == res2
        assert expected3 == res3

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "params,headers,expected_response_code,expected_response_data",
        [
            (
                pytest.param(
                    "?device=test-don-",
                    {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                    400,
                    {"error": 'No record matches your filter: {"device": "test-don-"}'},
                )
            ),
            (
                pytest.param(
                    "?device=Android",
                    {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                    200,
                    valid_data,
                )
            ),
        ],
    )
    def test_request_get(
        self,
        params: str,
        headers: typing.Dict[str, str],
        expected_response_code: int,
        expected_response_data: typing.Dict,
    ) -> None:
        response = APP.test_client().get("/api/v1/location" + params, headers=headers)
        assert expected_response_code == response.status_code
        assert "application/json" == response.content_type
        print(response.json)
        print(expected_response_data)
        assert expected_response_data == response.json

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "params,headers,input_data,expected_response_code,expected_response_data,error",
        [
            (
                pytest.param(
                    "?appid=test-don-",
                    {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                    {},
                    400,
                    {"error": "payload must not be empty"},
                    True,
                )
            ),
            (
                pytest.param(
                    "",
                    {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                    {},
                    400,
                    {"error": "appid must be sent as a parameter in the request"},
                    True,
                )
            ),
        ],
    )
    def test_request_post(
        self,
        params: str,
        headers: typing.Dict[str, str],
        input_data: typing.Dict,
        expected_response_code: int,
        expected_response_data: typing.Dict,
        error: bool,
    ) -> None:
        response: flask.Response = APP.test_client().post("/api/v1/location" + params, headers=headers, json=input_data)
        assert expected_response_code == response.status_code
        assert "application/json" == response.content_type
        if error:
            assert expected_response_data == response.get_json()
        else:
            assert "_id" in response.json
            assert response.json.get("_id").__bool__()

    @pytest.mark.parametrize("method", ("PATCH", "DELETE"))
    @mock.patch("gps_tracker.endpoints.location.is_user_authenticated")
    def test_request_methods(self, patched_method: mock.MagicMock, method: str) -> None:
        patched_method.return_value = "", True, 200
        response: flask.Response = APP.test_client().__getattribute__(method.lower())("/api/v1/location", method=method)
        expected_result: str = '{"error": "HTTP Verb %s is not supported, please use one of GET, POST, PUT"}' % method
        assert expected_result.encode() == response.get_data()
        assert 405 == response.status_code
