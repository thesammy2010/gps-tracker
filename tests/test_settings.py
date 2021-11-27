import os
from unittest import TestCase, mock

import pytest

from gps_tracker.settings import Config


class TestSettings:
    def test_default_values(self):
        config: Config = Config()
        assert config.port == "5000"
        assert config.flask_env == "DEBUG"
        assert config.discord_webhook == "https://discordapp.com/api/webhooks/"
        assert config.mongo_url == "mongodb://user:passw@localhost:27017/api"
        assert config.mongo_auth_database == "api"
        assert config.mongo_auth_collection == "auths"
        assert config.mongo_data_database == "api"
        assert config.mongo_data_collection == "data"

    @pytest.mark.parametrize(
        "field_name,expected_output",
        [
            ("port", "1234"),  # mocking setting from env variable
            ("flask_env", "DEBUG"),  # this is a default variable
        ],
    )
    @mock.patch.dict(os.environ, {"PORT": "1234"})
    def test_config(self, field_name, expected_output) -> None:
        config: Config = Config()
        assert config.__getattribute__(field_name) == expected_output
