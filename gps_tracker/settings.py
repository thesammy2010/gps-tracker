import os
import typing


class Config:
    _config: typing.Any = None
    port: str = ""
    discord_webhook: str = ""
    mongo_url: str = "mongodb://localhost:27017/defaultauthdb"
    mongo_data_collection: str = "example1"
    mongo_data_database: str = "example2"
    mongo_auth_collection: str = "example3"
    mongo_auth_database: str = "example4"
    environment: str = ""

    def __new__(cls) -> typing.Any:  # needs to be typed as a class instance
        if cls._config is not None:
            return cls._config
        cls._config = super().__new__(cls)
        cls._config._load_from_environment_variables()
        return cls._config

    def _load_from_environment_variables(self) -> None:
        options: typing.List[str] = [
            "port",
            "discord_webhook",
            "mongo_url",
            "mongo_data_collection",
            "mongo_data_database",
            "mongo_auth_collection",
            "mongo_auth_database",
            "environment"
        ]
        for option in options:
            self.__setattr__(option, os.getenv(option.upper(), self.__getattribute__(option)))


CONFIG = Config()
