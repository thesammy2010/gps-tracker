import typing
from typing import Tuple
from unittest import mock

import pytest

from gps_tracker.auth import (decrypt_header, hash_password,
                              is_user_authenticated)


class TestAuth(object):
    user_data = {
        "user1": {
            "username": "username",
            "salt": "salt".encode("utf-8").hex(),
            "key": "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8",
            "authorised": True,
        },
        "user2": {
            "username": "username",
            "salt": "salt".encode("utf-8").hex(),
            "key": "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8",
            "authorised": False,
        },
    }

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            ("dXNlcm5hbWU6cGFzc3dvcmQ=", ("username", "password")),
            ("Zm9vOmJhcg==", ("foo", "bar")),
            ("dXNlcm5hbWVvbmx5", (None, None)),  # usernameonly
            ("dXNlcm5hbWU6", ("username", "")),  # username:
            ("", (None, None)),
            ("Ojo=", (None, None)),  # "::"
        ],
    )
    def test_decrypt_header(self, expected_value: Tuple[str, str], input_value: str) -> None:
        assert expected_value == decrypt_header(input_value)

    @pytest.mark.parametrize(
        "input_values,expected_value",
        [
            (("password123", "73616c74"), "4d648905df3786f5cb2c6d614fa01f4060da0d5a0cf3eecc11597ff084071ddb"),
            (("a different password", "73616c74"), "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8"),
        ],
    )
    def test_hash_password(self, expected_value: str, input_values: Tuple[str, str]) -> None:
        assert expected_value == hash_password(input_values[0], input_values[1])

    @pytest.mark.parametrize(
        "input_data,user,expected_message,expected_access,expected_code",
        [
            ({"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="}, "user1", "", True, 200),  # happy path
            (
                {"Authorisation": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                "user1",
                "Authorization header missing",
                False,
                400,  # misspelled header
            ),
            (
                {"Authorization": "dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                "user1",
                "Use basic authorisation method",
                False,
                400,  # Basic missing from header content
            ),
            ({"Authorization": "Basic"}, "user1", "Malformed credentials", False, 400),  # credentials malformed
            (
                {"Authorization": "Basic dXNlcm5hbWUxOmEgZGlmZmVyZW50IHBhc3N3b3Jk"},
                "user1",
                "Not Authorised",
                False,
                401,  # invalid username so user would not show up in database
            ),
            (
                {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQh"},
                "user1",
                "Not Authorised",
                False,
                401,  # invalid password
            ),
            (
                {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                "user2",
                "Access Denied",
                False,
                403,  # identity known but not authorised
            ),
        ],
    )
    @mock.patch("gps_tracker.auth.look_up_user")
    def test_is_user_authenticated(
        self,
        mocked_look_up_user: mock.MagicMock,
        expected_message: str,
        expected_access: bool,
        expected_code: int,
        input_data: typing.Dict[str, str],
        user: str,
    ):
        mocked_look_up_user.return_value = self.user_data[user]
        message, access, code = is_user_authenticated(headers=input_data)

        assert expected_message == message
        assert expected_access is access
        assert expected_code == code

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "input_data,expected_message,expected_access,expected_code",
        [
            ({"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="}, "", True, 200),
            (
                {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQx"},
                "Not Authorised",
                False,
                401,
            ),  # username:a different password1
            (
                {"Authorization": "Basic dXNlcm5hbWUyOmEgZGlmZmVyZW50IHBhc3N3b3Jk"},
                "Access Denied",
                False,
                403,
            ),  # username2:a different password
        ],
    )
    def test_is_user_authenticated_integration(
        self,
        expected_message: str,
        expected_access: bool,
        expected_code: int,
        input_data: typing.Dict[str, str],
    ):
        message, access, code = is_user_authenticated(headers=input_data)

        assert expected_message == message
        assert expected_access is access
        assert expected_code == code
