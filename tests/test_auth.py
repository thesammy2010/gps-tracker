import typing

import pytest

from unittest import mock

from typing import Tuple

from gps_tracker.auth import decrypt_header, hash_password, is_user_authenticated


class TestAuth(object):
    user_data = {
        "username": "username",
        "salt": "salt".encode("utf-8").hex(),
        "key": "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8"
    }

    @pytest.mark.parametrize(
        "input_value,expected_value",
        [
            (
                    "dXNlcm5hbWU6cGFzc3dvcmQ=",
                    ("username", "password")
            ),
            (
                    "Zm9vOmJhcg==",
                    ("foo", "bar")
            ),
            (
                    "dXNlcm5hbWVvbmx5",  # usernameonly
                    (None, None)
            ),
            (
                    "dXNlcm5hbWU6",  # username:
                    ("username", "")
            ),
            (
                    "",
                    (None, None)
            ),
            (
                    "Ojo=",  # "::"
                    (None, None)
            )
        ]
    )
    def test_decrypt_header(self, expected_value: Tuple[str, str], input_value: str) -> None:
        assert expected_value == decrypt_header(input_value)

    @pytest.mark.parametrize(
        "input_values,expected_value",
        [
            (
                    ("password123", "73616c74"),
                    "4d648905df3786f5cb2c6d614fa01f4060da0d5a0cf3eecc11597ff084071ddb"
            ),
            (
                    ("a different password", "73616c74"),
                    "2210d7f11fdaceae6882c765b5228c96cd854655d3782746c2617128a4e62ad8"
            )
        ]
    )
    def test_hash_password(self, expected_value: str, input_values: Tuple[str, str]) -> None:
        assert expected_value == hash_password(input_values[0], input_values[1])

    @pytest.mark.parametrize(
        "input_data,expected_message,expected_access,expected_code",
        [
            (
                {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                "", True, 200  # happy path
            ),
            (
                {"Authorisation": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                "Authorization header missing", False, 400  # misspelled header
            ),
            (
                {"Authorization": "dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQ="},
                "Use basic authorisation method", False, 400  # Basic missing from header content
            ),
            (
                {"Authorization": "Basic"},
                "Malformed credentials", False, 400  # credentials malformed
            ),
            (
                {"Authorization": "Basic dXNlcm5hbWUxOmEgZGlmZmVyZW50IHBhc3N3b3Jk"},
                "Not Authorised", False, 401  # invalid username so user would not show up in database
            ),
            (
                {"Authorization": "Basic dXNlcm5hbWU6YSBkaWZmZXJlbnQgcGFzc3dvcmQh"},
                "Access Denied", False, 403  # invalid password
            ),
        ]
    )
    @mock.patch("gps_tracker.auth.look_up_user")
    def test_is_user_authenticated(
            self,
            mocked_look_up_user: mock.MagicMock,
            expected_message: str,
            expected_access: bool,
            expected_code: int,
            input_data: typing.Dict[str, str]
    ):
        mocked_look_up_user.return_value = self.user_data
        message, access, code = is_user_authenticated(headers=input_data)

        assert expected_message == message
        assert expected_access is access
        assert expected_code == code
